"""
00_sanitize_labels.py
=====================
Sanitize YOLO label files by clamping bbox values into [0, 1].
"""

from pathlib import Path


ROOT = Path(__file__).parent
SPLITS = ("train", "val", "test")


def _clamp01(v: float) -> float:
    return max(0.0, min(1.0, v))


def _sanitize_file(path: Path) -> tuple[int, int]:
    changed = 0
    invalid = 0
    out_lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 5:
            invalid += 1
            continue
        cls_id, sx, sy, sw, sh = parts
        try:
            x = float(sx)
            y = float(sy)
            w = float(sw)
            h = float(sh)
        except ValueError:
            invalid += 1
            continue
        cx = _clamp01(x)
        cy = _clamp01(y)
        cw = _clamp01(w)
        ch = _clamp01(h)
        if (cx, cy, cw, ch) != (x, y, w, h):
            changed += 1
        out_lines.append(f"{cls_id} {cx:.6f} {cy:.6f} {cw:.6f} {ch:.6f}")
    path.write_text("\n".join(out_lines) + ("\n" if out_lines else ""), encoding="utf-8")
    return changed, invalid


def main() -> None:
    print("=" * 60)
    print("  YOLO Label Sanitizer")
    print("=" * 60)
    total_files = 0
    total_changed = 0
    total_invalid = 0
    for split in SPLITS:
        label_dir = ROOT / split / split / "labels"
        if not label_dir.exists():
            continue
        for path in sorted(label_dir.glob("*.txt")):
            total_files += 1
            changed, invalid = _sanitize_file(path)
            total_changed += changed
            total_invalid += invalid
    print(f"  Files scanned : {total_files}")
    print(f"  Boxes clamped : {total_changed}")
    print(f"  Rows dropped  : {total_invalid}")
    print("=" * 60)


if __name__ == "__main__":
    main()
