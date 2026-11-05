"""Batch-detect every image in a folder and write a CSV report.

Example:
    python detect_folder.py photos/ --out results/ --conf 0.3 --classes person car
"""

import argparse
import csv
from pathlib import Path

from PIL import Image

from detector import Detector

IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", type=Path, help="Folder of images")
    parser.add_argument("--out", type=Path, default=Path("results"))
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--classes", nargs="*", help="Only keep these class names")
    args = parser.parse_args()

    images = sorted(p for p in args.input.iterdir() if p.suffix.lower() in IMAGE_TYPES)
    if not images:
        raise SystemExit(f"No images found in {args.input}")

    args.out.mkdir(parents=True, exist_ok=True)
    detector = Detector()
    rows = []
    for path in images:
        result = detector.detect(str(path), conf=args.conf, classes=args.classes)
        Image.fromarray(result.annotated).save(args.out / path.name)
        rows += [[path.name, d.label, d.confidence, *d.box] for d in result.detections]
        print(f"{path.name}: {result.counts or 'nothing'} ({result.inference_ms} ms)")

    with open(args.out / "detections.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image", "label", "confidence", "x1", "y1", "x2", "y2"])
        writer.writerows(rows)
    print(f"\n{len(rows)} detections in {len(images)} images -> {args.out / 'detections.csv'}")


if __name__ == "__main__":
    main()
