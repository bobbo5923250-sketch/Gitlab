import numpy as np
import pytest
from PIL import Image
from ultralytics.utils import ASSETS

from detector import Detector


@pytest.fixture(scope="module")
def detector():
    return Detector()


def test_detects_people_and_bus(detector):
    result = detector.detect(str(ASSETS / "bus.jpg"))
    assert result.counts.get("person", 0) >= 3
    assert "bus" in result.counts
    assert result.annotated.shape[2] == 3


def test_numpy_input_matches_path_input(detector):
    rgb = np.array(Image.open(ASSETS / "bus.jpg").convert("RGB"))
    assert detector.detect(rgb).counts == detector.detect(str(ASSETS / "bus.jpg")).counts


def test_class_filter(detector):
    result = detector.detect(str(ASSETS / "bus.jpg"), classes=["bus"])
    assert set(result.counts) == {"bus"}


def test_high_threshold_keeps_fewer_boxes(detector):
    low = detector.detect(str(ASSETS / "bus.jpg"), conf=0.1)
    high = detector.detect(str(ASSETS / "bus.jpg"), conf=0.8)
    assert len(high.detections) <= len(low.detections)
    assert all(d.confidence >= 0.8 for d in high.detections)
