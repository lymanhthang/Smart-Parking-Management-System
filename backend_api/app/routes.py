from flask import Blueprint, render_template, Response, request, jsonify
import cv2
import numpy as np
import base64
import re
import time
from datetime import datetime
from app.dao import (
    save_parking_record, 
    is_parking, 
    update_parking_record, 
    get_occupied_spots_count,
    get_today_revenue,
    get_daily_entries_last_n_days,
    get_daily_revenue_last_n_days,
    get_monthly_revenue_last_n_months
)
from .lp_process import lp_model, ocr_model, crop_lp_from_image, ocr_plate

main = Blueprint('main', __name__)

TOTAL_SPOTS = 50


@main.route('/check', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running!"}), 200


@main.route('/capture', methods=['POST'])
def capture():
    try:
        data = request.get_json()
        img_data = data.get('image', '')
        img_str = re.search(r'base64,(.*)', img_data).group(1)
        img_bytes = base64.b64decode(img_str)
        img_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({"status": "error", "message": "Không thể giải mã ảnh."}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Dữ liệu ảnh không hợp lệ: {e}"}), 400

    t_start = time.time()
    cropped_plates = crop_lp_from_image(lp_model, img)
    results = []

    for plate_img in cropped_plates:
        recognized_text = ocr_plate(ocr_model, plate_img)
        if not recognized_text:
            continue

        lp_record = None
        if not is_parking(recognized_text):
            lp_record = save_parking_record(recognized_text)
        else:
            lp_record = update_parking_record(recognized_text)

        if lp_record:
            duration_str = '---'
            if lp_record.CheckInTime and lp_record.CheckOutTime:
                delta = lp_record.CheckOutTime - lp_record.CheckInTime
                hours, remainder = divmod(delta.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                duration_str = f"{int(hours)} giờ {int(minutes)} phút"

            plate_data = {
                "plate_text": str(lp_record.vehicle.LicensePlate),
                "check_in_time": lp_record.CheckInTime.isoformat() if lp_record.CheckInTime else '---',
                "check_out_time": lp_record.CheckOutTime.isoformat() if lp_record.CheckOutTime else '---',
                "duration": duration_str,
                "parking_fee": str(lp_record.ParkingFee) if lp_record.ParkingFee is not None else '---',
                "status": str(lp_record.status.StatusName)
            }
            results.append(plate_data)

    t_end = time.time()
    
    occupied_count = get_occupied_spots_count()
    available_count = TOTAL_SPOTS - occupied_count

    print(f"Các biển số đã xử lý: {results}")
    print(f"Thời gian xử lý: {t_end - t_start:.2f} giây")

    return jsonify({
        "status": "success",
        "plates": results,
        "total_spots": TOTAL_SPOTS,
        "available_spots": available_count,
        "occupied_spots": occupied_count
    })



@main.route('/api/parking-status', methods=['GET'])
def get_parking_status_api():
    occupied_count = get_occupied_spots_count()
    return jsonify({
        "total_spots": TOTAL_SPOTS,
        "occupied_spots": occupied_count,
        "available_spots": TOTAL_SPOTS - occupied_count
    })

@main.route('/api/today-revenue', methods=['GET'])
def get_today_revenue_api():
    revenue = get_today_revenue()
    return jsonify({"revenue": revenue})

@main.route('/api/daily-entries', methods=['GET'])
def get_daily_entries_api():
    result = get_daily_entries_last_n_days(days=7)
    return jsonify(result)

@main.route('/api/daily-revenue', methods=['GET'])
def get_daily_revenue_api():
    result = get_daily_revenue_last_n_days(days=7)
    return jsonify(result)

@main.route('/api/monthly-revenue', methods=['GET'])
def get_monthly_revenue_api():
    result = get_monthly_revenue_last_n_months(months=6)
    return jsonify(result)
