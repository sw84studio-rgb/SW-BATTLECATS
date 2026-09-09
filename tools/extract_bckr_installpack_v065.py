#!/usr/bin/env python3
"""SW BATTLECATS V065 - BCKR KR 15.5.0 InstallPack acquisition verifier.

Purpose
-------
Inspect an already-obtained XAPK/APKM/APKS/ZIP/APK or extracted directory,
identify nested InstallPack candidates, verify the exact KR 15.5.0 InstallPack
fingerprint, and optionally extract only assets/ from an EXACT fingerprint match.

Safety gates
------------
* No network download.
* No pack decryption.
* No web-app asset promotion.
* A nested APK is canonical only when its MD5 exactly matches EXPECTED_INSTALLPACK_MD5.
* Filename/size/largest-file heuristics are discovery hints only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import BinaryIO, Iterable

SCHEMA = "sw_battlecats_bckr_installpack_audit_v065"
EXPECTED_PACKAGE = "jp.co.ponos.battlecatskr"
EXPECTED_VERSION_NAME = "15.5.0"
EXPECTED_VERSION_CODE = 1505000
EXPECTED_INSTALLPACK_MD5 = "c6300411da318c0de775527c291af4a1"
EXPECTED_INSTALLPACK_DISPLAY_SIZE = "153.53 MB"
REFERENCE_XAPK_SHA256 = "bef92a009ee775e1c2844eca8ecb6814951a69d638dd8c99d745c841d9c23cb5"
REFERENCE_CERT_SHA1 = "0dc1accfc5ee10c7fb375a0126e01ffc3a8cc46a"
INTERESTING_EXTENSIONS = {
    ".pack", ".list", ".png", ".jpg", ".jpeg", ".webp", ".gif",
    ".imgcut", ".mamodel", ".maanim", ".csv", ".json"
}


def digest_path(path: Path, algos=("md5", "sha256"), chunk=1024 * 1024) -> dict[str, str]:
    hs = {name: hashlib.new(name) for name in algos}
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            for h in hs.values():
                h.update(b)
    return {name: h.hexdigest() for name, h in hs.items()}


def stream_copy_and_digest(src: BinaryIO, dst: Path, chunk=1024 * 1024) -> dict[str, object]:
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    size = 0
    with dst.open("wb") as out:
        while True:
            b = src.read(chunk)
            if not b:
                break
            out.write(b)
            md5.update(b)
            sha256.update(b)
            size += len(b)
    return {"size_bytes": size, "md5": md5.hexdigest(), "sha256": sha256.hexdigest()}


def is_zip(path: Path) -> bool:
    try:
        return zipfile.is_zipfile(path)
    except OSError:
        return False


def safe_asset_target(root: Path, member_name: str) -> Path | None:
    p = PurePosixPath(member_name)
    if p.is_absolute() or ".." in p.parts:
        return None
    parts = p.parts
    if not parts or parts[0].lower() != "assets":
        return None
    return root.joinpath(*parts)


def inventory_zip(path: Path) -> dict[str, object]:
    result: dict[str, object] = {
        "zip_readable": False,
        "entry_count": 0,
        "assets_entry_count": 0,
        "interesting_extension_counts": {},
        "interesting_entries_sample": [],
        "pack_like_entries": [],
    }
    if not is_zip(path):
        return result
    counts: Counter[str] = Counter()
    interesting: list[str] = []
    pack_like: list[str] = []
    with zipfile.ZipFile(path) as zf:
        infos = [i for i in zf.infolist() if not i.is_dir()]
        result["zip_readable"] = True
        result["entry_count"] = len(infos)
        result["assets_entry_count"] = sum(1 for i in infos if PurePosixPath(i.filename).parts and PurePosixPath(i.filename).parts[0].lower() == "assets")
        for info in infos:
            suffix = PurePosixPath(info.filename).suffix.lower()
            if suffix in INTERESTING_EXTENSIONS:
                counts[suffix] += 1
                if len(interesting) < 250:
                    interesting.append(info.filename)
            low = info.filename.lower()
            if suffix in {".pack", ".list"} or "imageserver" in low or "installpack" in low:
                if len(pack_like) < 250:
                    pack_like.append(info.filename)
    result["interesting_extension_counts"] = dict(sorted(counts.items()))
    result["interesting_entries_sample"] = interesting
    result["pack_like_entries"] = pack_like
    return result


def extract_assets(apk_path: Path, output_dir: Path) -> dict[str, object]:
    extracted = 0
    skipped_unsafe = 0
    bytes_written = 0
    output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(apk_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            target = safe_asset_target(output_dir, info.filename)
            if target is None:
                if PurePosixPath(info.filename).parts and PurePosixPath(info.filename).parts[0].lower() == "assets":
                    skipped_unsafe += 1
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst, length=1024 * 1024)
            extracted += 1
            bytes_written += info.file_size
    return {
        "output_dir": str(output_dir),
        "files_extracted": extracted,
        "bytes_written": bytes_written,
        "unsafe_asset_entries_skipped": skipped_unsafe,
    }


def scan_directory(root: Path) -> dict[str, object]:
    counts: Counter[str] = Counter()
    sample: list[str] = []
    pack_like: list[str] = []
    total = 0
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        total += 1
        rel = p.relative_to(root).as_posix()
        suffix = p.suffix.lower()
        if suffix in INTERESTING_EXTENSIONS:
            counts[suffix] += 1
            if len(sample) < 250:
                sample.append(rel)
        low = rel.lower()
        if suffix in {".pack", ".list"} or "imageserver" in low or "installpack" in low:
            if len(pack_like) < 250:
                pack_like.append(rel)
    return {
        "file_count": total,
        "interesting_extension_counts": dict(sorted(counts.items())),
        "interesting_entries_sample": sample,
        "pack_like_entries": pack_like,
    }


def audit_archive(path: Path, temp_root: Path, extract_assets_flag: bool, output_dir: Path) -> dict[str, object]:
    outer_hash = digest_path(path)
    outer = {
        "path": str(path),
        "size_bytes": path.stat().st_size,
        **outer_hash,
        "reference_apkpure_xapk_sha256_match": outer_hash["sha256"] == REFERENCE_XAPK_SHA256,
    }
    if not is_zip(path):
        return {
            "input_kind": "non_zip_file",
            "outer": outer,
            "candidate_apks": [],
            "exact_installpack_found": False,
            "note": "Input is not ZIP-readable. No candidate extraction attempted.",
        }

    candidates_meta: list[dict[str, object]] = []
    with zipfile.ZipFile(path) as zf:
        apk_infos = [i for i in zf.infolist() if not i.is_dir() and i.filename.lower().endswith(".apk")]
        if not apk_infos and path.suffix.lower() == ".apk":
            # Direct APK: audit itself as a candidate below outside the outer archive loop.
            apk_infos = []

        named = [i for i in apk_infos if "installpack" in PurePosixPath(i.filename).name.lower()]
        selected_names = {i.filename for i in named}
        if not named and apk_infos:
            # Discovery fallback only; never canonical without exact MD5.
            selected_names.add(max(apk_infos, key=lambda i: i.file_size).filename)

        for idx, info in enumerate(sorted(apk_infos, key=lambda i: i.file_size, reverse=True)):
            discovery_reason = []
            if "installpack" in PurePosixPath(info.filename).name.lower():
                discovery_reason.append("filename_contains_installpack")
            if info.filename in selected_names and not discovery_reason:
                discovery_reason.append("largest_nested_apk_fallback")
            if info.filename not in selected_names:
                # We still list all nested APKs, but only materialize/hash selected candidates.
                candidates_meta.append({
                    "archive_member": info.filename,
                    "declared_size_bytes": info.file_size,
                    "discovery_candidate": False,
                })
                continue

            temp_apk = temp_root / f"candidate_{idx}.apk"
            with zf.open(info) as src:
                dig = stream_copy_and_digest(src, temp_apk)
            exact = dig["md5"] == EXPECTED_INSTALLPACK_MD5
            inv = inventory_zip(temp_apk)
            row: dict[str, object] = {
                "archive_member": info.filename,
                "declared_size_bytes": info.file_size,
                "discovery_candidate": True,
                "discovery_reason": discovery_reason,
                **dig,
                "exact_installpack_match": exact,
                "canonical_status": "EXACT_INSTALLPACK_MATCH" if exact else "UNVERIFIED_CANDIDATE",
                "inventory": inv,
            }
            if exact and extract_assets_flag:
                row["asset_extraction"] = extract_assets(temp_apk, output_dir / "installpack_assets")
            candidates_meta.append(row)

    # If input itself is an APK, check its exact fingerprint and inventory as one candidate.
    if path.suffix.lower() == ".apk":
        exact = outer_hash["md5"] == EXPECTED_INSTALLPACK_MD5
        row = {
            "archive_member": path.name,
            "declared_size_bytes": path.stat().st_size,
            "discovery_candidate": True,
            "discovery_reason": ["direct_apk_input"],
            "size_bytes": path.stat().st_size,
            "md5": outer_hash["md5"],
            "sha256": outer_hash["sha256"],
            "exact_installpack_match": exact,
            "canonical_status": "EXACT_INSTALLPACK_MATCH" if exact else "UNVERIFIED_CANDIDATE",
            "inventory": inventory_zip(path),
        }
        if exact and extract_assets_flag:
            row["asset_extraction"] = extract_assets(path, output_dir / "installpack_assets")
        candidates_meta.append(row)

    exact_count = sum(1 for c in candidates_meta if c.get("exact_installpack_match") is True)
    return {
        "input_kind": "zip_or_apk_archive",
        "outer": outer,
        "nested_apk_count": sum(1 for c in candidates_meta),
        "candidate_apks": candidates_meta,
        "exact_installpack_found": exact_count == 1,
        "exact_installpack_match_count": exact_count,
        "provenance_gate_pass": exact_count == 1,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify BCKR KR 15.5.0 InstallPack without auto-promoting assets.")
    ap.add_argument("input", type=Path, help="XAPK/APKM/APKS/ZIP/APK file or extracted directory")
    ap.add_argument("--report", type=Path, default=None, help="JSON report path")
    ap.add_argument("--output-dir", type=Path, default=Path("bckr_v065_output"), help="Extraction output root")
    ap.add_argument("--extract-assets", action="store_true", help="Extract assets/ only when exact InstallPack MD5 matches")
    args = ap.parse_args()

    input_path = args.input.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    report_path = (args.report.expanduser().resolve() if args.report else output_dir / "V065_INSTALLPACK_AUDIT_REPORT.json")
    output_dir.mkdir(parents=True, exist_ok=True)

    identity = {
        "package": EXPECTED_PACKAGE,
        "version_name": EXPECTED_VERSION_NAME,
        "version_code": EXPECTED_VERSION_CODE,
        "installpack_expected_md5": EXPECTED_INSTALLPACK_MD5,
        "installpack_reference_display_size": EXPECTED_INSTALLPACK_DISPLAY_SIZE,
        "reference_apkpure_xapk_sha256": REFERENCE_XAPK_SHA256,
        "reference_signing_cert_sha1": REFERENCE_CERT_SHA1,
        "canonical_gate": "InstallPack APK MD5 exact match required",
    }
    report: dict[str, object] = {
        "schema": SCHEMA,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "identity": identity,
        "policy": {
            "network_download_performed": False,
            "decryption_performed": False,
            "automatic_web_asset_promotion": False,
            "filename_or_size_only_never_canonical": True,
            "asset_extraction_requires_exact_installpack_md5": True,
        },
        "input": str(input_path),
    }

    if not input_path.exists():
        report["error"] = "input_not_found"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"ERROR: input not found: {input_path}", file=sys.stderr)
        return 2

    if input_path.is_dir():
        report["result"] = {
            "input_kind": "directory",
            "directory_inventory": scan_directory(input_path),
            "exact_installpack_found": False,
            "provenance_gate_pass": False,
            "note": "Directory inventory alone cannot prove the InstallPack APK MD5 identity.",
        }
    else:
        with tempfile.TemporaryDirectory(prefix="swbc_v065_") as td:
            report["result"] = audit_archive(input_path, Path(td), args.extract_assets, output_dir)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "report": str(report_path),
        "exact_installpack_found": report["result"].get("exact_installpack_found", False),
        "provenance_gate_pass": report["result"].get("provenance_gate_pass", False),
        "assets_extracted": bool(args.extract_assets and report["result"].get("provenance_gate_pass", False)),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
