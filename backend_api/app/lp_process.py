import re
from ultralytics import YOLO
import cv2
import numpy as np
import os
from pathlib import Path
from paddleocr import PaddleOCR


def load_models(lp_path):
    lp_model = YOLO(lp_path, task='detect')
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    _ = lp_model(dummy_img)
    reader = PaddleOCR(
	use_angle_cls=True,
        use_textline_orientation=True,
        lang='en',
        ocr_version='PP-OCRv3',
        cls=True,
    	warmup=True
    )

    print("Nạp model thành công.")
    return lp_model, reader



lp_model_path=Path("app") / "model" / "lp_detector_ncnn_model"

# Load models khi start app
lp_model, ocr_model = load_models(lp_model_path)

def crop_lp_from_image(lp_model, img):
    cropped_plates = []
    results = lp_model(img)[0]
    for box in results.boxes:
        coords = box.xyxy[0].tolist()
        x1, y1, x2, y2 = map(int, coords)
        cropped_license_plate = img[y1:y2, x1:x2]
        cropped_plates.append(cropped_license_plate)
    return cropped_plates


def ocr_plate(reader, cropped_lp_image):
    all_texts = []

    result = reader.ocr(cropped_lp_image, cls=True)

    if result and result[0]:
        for line in result[0]:
            raw_text = line[1][0]

            if raw_text:
                # Lọc bỏ ký tự đặc biệt
                filtered_text = re.sub(r'[^A-Za-z0-9]', '', raw_text)
                if filtered_text:
                    all_texts.append(filtered_text)

    return "".join(all_texts)
