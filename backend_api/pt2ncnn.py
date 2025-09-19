from pathlib import Path
from ultralytics import YOLO

lp_model_path =Path("app") / "model" / "lp_detector.pt"

model=YOLO(lp_model_path)
model.export(format="ncnn")
