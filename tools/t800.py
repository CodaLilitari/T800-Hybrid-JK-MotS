#!/usr/bin/env python3
"""Build/install the T-800 MP skin from your own JK/MotS installation.

Python 3.10+; standard library only. Reads the licensed game archives locally.
Generated KEY/registry/string copies belong in your local installation, never
in a source release. Original archives and executables are never modified.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import struct
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MOD_NAME = "T800HybridR4"
RECEIPT = "t800-install-receipt.json"
MATERIALS = ("h8tr4.mat", "h8ar4.mat", "h8hdp1.mat", "h8lg4.mat", "h8eye.mat")
PALETTE_HASH = "c7dfb4c72f34068e23a6c048853cf8b4afb86b78350af2c173e5e8e409603dd2"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_digest(path):
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def relative_parts(name):
    parts = name.replace("\\", "/").split("/")
    if not parts or any(not p or p in (".", "..") or ":" in p or "\x00" in p for p in parts):
        raise ValueError("Unsafe relative member path: " + repr(name))
    return parts


def child(root, name):
    result = root
    for part in relative_parts(name):
        result = result / part
        if result.exists() or result.is_symlink():
            if is_link(result):
                raise ValueError("Links/reparse points are not accepted: " + str(result))
    return result


def named_child(root, name):
    matches = [p for p in root.iterdir() if p.name.casefold() == name.casefold()]
    if len(matches) != 1 or is_link(matches[0]):
        raise ValueError("Missing, ambiguous, or linked game component: " + name)
    return matches[0]


class Gob:
    def __init__(self, path):
        self.path, self.entries = path, {}
        size = path.stat().st_size
        with path.open("rb") as stream:
            header = stream.read(12)
            if len(header) != 12:
                raise ValueError("Truncated archive header: " + path.name)
            magic, version, index = struct.unpack("<4sII", header)
            if magic != b"GOB " or version != 20 or not 12 <= index <= size - 4:
                raise ValueError("Invalid GOB/GOO header: " + path.name)
            stream.seek(index)
            count = struct.unpack("<I", stream.read(4))[0]
            if count > 100000 or index + 4 + count * 136 > size:
                raise ValueError("Invalid archive index: " + path.name)
            for _ in range(count):
                offset, length, raw_name = struct.unpack("<II128s", stream.read(136))
                name = raw_name.split(b"\0", 1)[0].decode("ascii").replace("/", "\\").lower()
                relative_parts(name)
                if name in self.entries or offset < 12 or offset + length > size:
                    raise ValueError("Duplicate or truncated archive member: " + name)
                self.entries[name] = (offset, length)

    def read(self, name):
        offset, size = self.entries[name.replace("/", "\\").lower()]
        with self.path.open("rb") as stream:
            stream.seek(offset)
            data = stream.read(size)
        if len(data) != size:
            raise ValueError("Short archive read: " + name)
        return data


def read_base(archives, name):
    for archive in archives:
        if name.replace("/", "\\").lower() in archive.entries:
            return archive.read(name), archive.path.name
    raise ValueError("Required game resource missing: " + name)


def model_rows(data):
    text = data.decode("latin1")
    headers = list(re.finditer(r"(?im)^numModels:\s*(\d+)", text))
    if len(headers) != 1:
        raise ValueError("models.dat must have one model count")
    rows = []
    for line in text.splitlines():
        match = re.match(r"^\s*(\d+):\s*(\S+)\s+(\S+)(?:\s+(\d+))?", line)
        if match:
            rows.append((int(match[1]), match[2], match[3], int(match[4]) if match[4] else None))
    if [r[0] for r in rows] != list(range(int(headers[0][1]))):
        raise ValueError("models.dat has inconsistent indices/count")
    return rows


def string_records(data):
    records = []
    for line in data.decode("latin1").splitlines():
        if re.match(r"^END\b", line, re.I):
            break
        if line.lstrip().startswith('"'):
            match = re.match(r'^\s*"([^"\r\n]+)"\s+(-?\d+)\s+"(.*)"', line)
            if not match:
                raise ValueError("Unrecognized string table row")
            records.append((match[1], int(match[2]), match[3]))
    if not records:
        raise ValueError("Empty string table")
    return records


def patch_registries(archives, game):
    models, model_source = read_base(archives, "misc/models.dat")
    strings, string_source = read_base(archives, "ui/jkstrings.uni")
    rows, records = model_rows(models), string_records(strings)
    if any(r[1].lower() == "t800hy4.3do" for r in rows) or any(r[0].upper() == "T800HY4" for r in records):
        raise ValueError("Game archives already contain T800; use unmodified retail resources")
    updated = re.sub(rb"(?im)^(numModels:\s*)\d+", lambda m: m[1] + str(len(rows) + 1).encode(), models, count=1)
    updated += ("\r\n# T-800 Hybrid r4 retail integration\r\n%d: t800hy4.3do ky.snd" % len(rows)).encode()
    updated += (b" 1" if game == "mots" else b"") + b"\r\n"
    if len(re.findall(rb"(?im)^MSGS\s+\d+", strings)) != 1:
        raise ValueError("String table must have one MSGS count")
    uni = re.sub(rb"(?im)^(MSGS\s+)\d+", lambda m: m[1] + str(len(records) + 1).encode(), strings, count=1)
    ends = list(re.finditer(rb"(?im)^END\b", uni))
    if len(ends) != 1:
        raise ValueError("String table must have one END marker")
    i = ends[0].start()
    uni = uni[:i] + b'"T800HY4" 0 "T-800 Hybrid"\r\n' + uni[i:]
    if model_rows(updated)[:-1] != rows or string_records(uni)[:-1] != records:
        raise ValueError("Preservation check failed for registry/string records")
    return {"misc\\models.dat": updated, "ui\\jkstrings.uni": uni}, {
        "model_archive": model_source, "string_archive": string_source,
        "stock_models": len(rows), "output_models": len(rows) + 1,
        "stock_strings": len(records), "output_strings": len(records) + 1,
        "stock_rows_and_strings_preserved": True,
    }


def pad_key(data):
    matches = list(re.finditer(rb"(?im)^(\s*JOINTS[ \t]+)(\d+)(?=[ \t\r\n#]|$)", data))
    if len(matches) != 1:
        raise ValueError("KEY must have one JOINTS declaration")
    match = matches[0]
    before, after = int(match[2]), max(24, int(match[2]))
    nodes = [int(n) for n in re.findall(rb"(?im)^\s*NODE[ \t]+(\d+)", data)]
    if any(n < 0 or n >= before for n in nodes):
        raise ValueError("KEY has node outside declared allocation")
    result = data[:match.start(2)] + str(after).encode() + data[match.end(2):]
    return result, before != after


def asset_bytes(relative):
    manifest = json.loads((ROOT / "tools" / "asset-hashes.json").read_text(encoding="utf-8"))
    data = child(ROOT, relative).read_bytes()
    if manifest.get(relative) != digest(data):
        raise ValueError("Release asset is missing from manifest or has changed: " + relative)
    return data


def collect(game_root, game, materials, pose):
    resource = named_child(game_root, "resource")
    names = ("Res2.gob", "Res1hi.gob") if game == "jk" else ("JKMRES.GOO", "JKMSNDLO.GOO")
    archives = [Gob(named_child(resource, n)) for n in names]
    members, registry = patch_registries(archives, game)
    key_count = changed = 0
    for archive in archives:
        for name in sorted(archive.entries):
            if not name.endswith(".key") or name in members:
                continue
            if not name.startswith("3do\\key\\"):
                raise ValueError("Unexpected KEY resource location: " + name)
            members[name], modified = pad_key(archive.read(name))
            key_count += 1
            changed += modified
    if not key_count:
        raise ValueError("No animation resources found")
    palette, _ = read_base(archives, "misc/cmp/dflt.cmp")
    if materials == "indexed" and (palette[:4] != b"CMP " or digest(palette[64:832]) != PALETTE_HASH):
        raise ValueError("The game's default palette differs from the supplied indexed textures")
    members["3do\\t800hy4.3do"] = asset_bytes("assets/models/" + pose + "/t800hy4.3do")
    for name in MATERIALS:
        members["mat\\" + name] = asset_bytes("assets/materials/" + game + "/" + materials + "/" + name)
    report = {
        "schema": 1, "target": game, "variant": materials, "pose": pose, "scope": "multiplayer",
        "generated_from_locally_owned_game_data": True,
        "redistribute_generated_output": False,
        "archives": [{"name": a.path.name, "sha256": file_digest(a.path)} for a in archives],
        "registries": registry, "keys": {"count": key_count, "padded": changed, "only_JOINTS_allocation_changed": True},
        "aliases": [], "runtime_tested_by_this_build": False,
        "members": {n: {"bytes": len(d), "sha256": digest(d)} for n, d in sorted(members.items())},
    }
    return members, report


def outside_source(destination):
    resolved = destination.resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise ValueError("Generated game data must be outside this source/release directory")
    return resolved


def write_payload(destination, members, report):
    for name, data in members.items():
        path = child(destination, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        if file_digest(path) != digest(data):
            raise ValueError("Written file failed verification: " + name)
    (destination / "BUILD_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


def game_executable(game_root, game):
    names = ("jk.exe", "jediknight.exe") if game == "jk" else ("jkm.exe",)
    for path in game_root.iterdir():
        if path.name.lower() in names and path.is_file() and not is_link(path):
            return path
    raise ValueError("Original game executable not found")


def build(args, install=False):
    game_root = args.game_directory.resolve(strict=True)
    destination = outside_source(game_root / MOD_NAME if install else args.output)
    if destination.exists():
        raise ValueError("Destination already exists; uninstall its verified receipt before switching: " + str(destination))
    executable = game_executable(game_root, args.game) if install else None
    members, report = collect(game_root, args.game, args.materials, args.pose)
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".T800HybridR4-stage-", dir=destination.parent))
    try:
        write_payload(stage, members, report)
        if install:
            records = [{"relative": name, "sha256": digest(data)} for name, data in sorted(members.items())]
            records.append({"relative": "BUILD_REPORT.json", "sha256": file_digest(stage / "BUILD_REPORT.json")})
            receipt = {
                "schema": 1, "game": args.game, "materials": args.materials, "pose": args.pose,
                "destination": str(destination), "executable": str(executable),
                "created_utc": datetime.now(timezone.utc).isoformat(), "files": records,
            }
            (stage / RECEIPT).write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        if destination.exists():
            raise ValueError("Destination appeared during build; refusing to replace it")
        stage.rename(destination)
    except Exception:
        print("Uncommitted staging files preserved at: " + str(stage), file=sys.stderr)
        raise
    print(("Installed" if install else "Built") + " and verified %d resource files: " % len(members) + str(destination))
    if install:
        print('Launch from the game folder: "%s" -path %s' % (executable, MOD_NAME))


def verified_receipt(game_root):
    destination = game_root.resolve(strict=True) / MOD_NAME
    if is_link(destination):
        raise ValueError("Installation directory is a link/reparse point")
    receipt_path = child(destination, RECEIPT)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig"))
    if receipt.get("schema") != 1 or receipt.get("destination") != str(destination) or receipt.get("game") not in ("jk", "mots"):
        raise ValueError("Installation receipt identity mismatch")
    records, seen = receipt.get("files"), set()
    if not isinstance(records, list) or not records:
        raise ValueError("Empty/invalid installation receipt")
    owned = []
    for row in records:
        name, expected = row["relative"], row["sha256"]
        normalized = "\\".join(relative_parts(name)).casefold()
        if normalized == RECEIPT.casefold() or normalized in seen or not re.fullmatch(r"[a-fA-F0-9]{64}", expected):
            raise ValueError("Duplicate or invalid receipt entry")
        seen.add(normalized)
        path = child(destination, name)
        if not path.is_file() or file_digest(path) != expected.lower():
            raise ValueError("Changed or missing installed file; preserving installation: " + str(path))
        owned.append(path)
    return destination, receipt_path, owned


def uninstall(args):
    destination, receipt_path, owned = verified_receipt(args.game_directory)
    # Validate every owned file before deleting any. Extra user files are kept.
    for path in owned:
        path.unlink()
    receipt_path.unlink()
    directories = {p.parent for p in owned}
    for path in tuple(directories):
        directories.update(p for p in path.parents if p != destination and destination in p.parents)
    for path in sorted(directories, key=lambda p: len(p.parts), reverse=True):
        if path != destination and path.exists() and not is_link(path) and not any(path.iterdir()):
            path.rmdir()
    if not any(destination.iterdir()):
        destination.rmdir()
    print("Removed verified T800 files; unrelated files preserved.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="command", required=True)
    for action in ("build", "install"):
        command = actions.add_parser(action)
        command.add_argument("--game", required=True, choices=("jk", "mots"))
        command.add_argument("--game-directory", required=True, type=Path)
        command.add_argument("--pose", choices=("original", "holding-curl"), default="original")
        command.add_argument("--materials", choices=("indexed", "rgb565"), default="indexed")
        if action == "build":
            command.add_argument("--output", required=True, type=Path, help="New local output directory outside this release")
    for action in ("verify", "uninstall"):
        command = actions.add_parser(action)
        command.add_argument("--game-directory", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command in ("build", "install"):
            build(args, install=args.command == "install")
        elif args.command == "uninstall":
            uninstall(args)
        else:
            destination, _, owned = verified_receipt(args.game_directory)
            print("Verified %d installed files: " % len(owned) + str(destination))
    except (OSError, ValueError, KeyError, struct.error) as error:
        print("T800: " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
