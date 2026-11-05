"""Gradio web demo for object detection.  Run: python app.py"""

import gradio as gr
from ultralytics.utils import ASSETS

from detector import Detector

detector = Detector()


def run(image, conf, classes):
    if image is None:
        raise gr.Error("Please upload an image or take a photo first.")
    result = detector.detect(image, conf=conf, classes=classes or None)

    table = [[d.label, d.confidence, *d.box] for d in result.detections]
    summary = f"**{len(result.detections)} objects** found in {result.inference_ms} ms"
    if result.counts:
        summary += " — " + ", ".join(f"{n} × {label}" for label, n in result.counts.items())
    return result.annotated, summary, table


with gr.Blocks(title="Object Detection") as demo:
    gr.Markdown("# 🔍 Object Detection with YOLO\nDetects 80 everyday object types (people, vehicles, animals, …).")
    with gr.Row():
        with gr.Column():
            image_in = gr.Image(type="numpy", label="Input", sources=["upload", "webcam", "clipboard"])
            conf = gr.Slider(0.05, 0.95, value=0.25, step=0.05, label="Confidence threshold")
            classes = gr.Dropdown(detector.class_names, multiselect=True, label="Only detect (optional)")
            button = gr.Button("Detect", variant="primary")
        with gr.Column():
            image_out = gr.Image(label="Result")
            summary = gr.Markdown()
            table = gr.Dataframe(headers=["label", "confidence", "x1", "y1", "x2", "y2"], label="Detections")

    gr.Examples([[str(ASSETS / "bus.jpg")], [str(ASSETS / "zidane.jpg")]], inputs=image_in)
    button.click(run, [image_in, conf, classes], [image_out, summary, table])

if __name__ == "__main__":
    demo.launch()
