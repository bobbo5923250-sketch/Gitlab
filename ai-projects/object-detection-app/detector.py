"""Thin wrapper around a pretrained YOLO model.

Keeping the model logic here (separate from the UI) makes it reusable from the
web app, the batch CLI and the tests.
"""

from collections import Counter
from dataclasses import dataclass

import numpy as np
from ultralytics import YOLO

DEFAULT_WEIGHTS = "yolo11n.pt"  # downloaded automatically on first use (~6 MB)


@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple[int, int, int, int]  # x1, y1, x2, y2 in pixels


@dataclass
class DetectionResult:
    annotated: np.ndarray  # RGB image with boxes drawn
    detections: list[Detection]
    inference_ms: float

    @property
    def counts(self) -> dict[str, int]:
        return dict(Counter(d.label for d in self.detections).most_common())


class Detector:
    def __init__(self, weights: str = DEFAULT_WEIGHTS) -> None:
        self.model = YOLO(weights)

    @property
    def class_names(self) -> list[str]:
        return list(self.model.names.values())

    def detect(
        self,
        image: np.ndarray | str,
        conf: float = 0.25,
        classes: list[str] | None = None,
    ) -> DetectionResult:
        """Run detection on an RGB numpy image or an image path.

        Args:
            image: RGB array (H, W, 3) or path to an image file.
            conf: Minimum confidence to keep a box.
            classes: Optional list of class names to keep, e.g. ["person", "car"].
        """
        class_ids = None
        if classes:
            name_to_id = {name: i for i, name in self.model.names.items()}
            class_ids = [name_to_id[c] for c in classes if c in name_to_id]

        # Ultralytics expects BGR for numpy input (OpenCV convention)
        source = image[..., ::-1] if isinstance(image, np.ndarray) else image
        result = self.model.predict(source, conf=conf, classes=class_ids, verbose=False)[0]

        detections = [
            Detection(
                label=self.model.names[int(cls)],
                confidence=round(float(score), 3),
                box=tuple(int(v) for v in xyxy),
            )
            for xyxy, score, cls in zip(result.boxes.xyxy.tolist(), result.boxes.conf.tolist(), result.boxes.cls.tolist())
        ]
        return DetectionResult(
            annotated=result.plot()[..., ::-1],  # BGR -> RGB for display
            detections=detections,
            inference_ms=round(result.speed["inference"], 1),
        )
