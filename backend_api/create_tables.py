from app import app, db
from datetime import datetime
from app.models import ParkingRecord


with app.app_context():
    db.drop_all()
    db.create_all()

    print("Đã tạo bảng thành công!")