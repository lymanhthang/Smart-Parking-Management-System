from app import db
from datetime import datetime, timedelta
from app.models import Vehicle, ParkingRecord, Status
from math import ceil
from sqlalchemy import func, cast, Date, extract



def save_parking_record(license_plate):
    if is_parking(license_plate):
        print(f"Lỗi: Xe {license_plate} đã có trong bãi.")
        return None

    vehicle = Vehicle.query.filter_by(LicensePlate=license_plate).first()
    if not vehicle:
        vehicle = Vehicle(LicensePlate=license_plate)
        db.session.add(vehicle)

    record = ParkingRecord(
        vehicle=vehicle,
        StatusID=1
    )
    db.session.add(record)
    db.session.commit()
    
    return record

def is_parking(license_plate):
    record = ParkingRecord.query.join(Vehicle).filter(
        Vehicle.LicensePlate == license_plate,
        ParkingRecord.StatusID == 1
    ).first()
    
    return record is not None

def update_parking_record(license_plate):
    record = ParkingRecord.query.join(Vehicle).filter(
        Vehicle.LicensePlate == license_plate,
        ParkingRecord.StatusID == 1 
    ).first()
    
    if record:
        check_out_time = datetime.utcnow()
        record.CheckOutTime = check_out_time
        
        duration = check_out_time - record.CheckInTime
        hours = duration.total_seconds() / 3600
        
        fee = ceil(hours) * 5000
        
        record.ParkingFee = fee
        record.StatusID = 2  

        db.session.commit()
        
        return record
    
    return None


def get_parking_stats():
    occupied_count = ParkingRecord.query.filter_by(StatusID=1).count()
    return occupied_count


def get_occupied_spots_count() -> int:
    # print(f"So lượng xe đang đỗ: {ParkingRecord.query.filter_by(StatusID=1).count()}")
    return ParkingRecord.query.filter_by(StatusID=1).count()


def get_today_revenue() -> float:
    """Tính tổng doanh thu từ các xe đã rời bãi trong ngày hôm nay."""
    today = datetime.utcnow().date()
    
    total_revenue = db.session.query(
        func.sum(ParkingRecord.ParkingFee)
    ).filter(
        cast(ParkingRecord.CheckOutTime, Date) == today,
        ParkingRecord.StatusID == 2
    ).scalar()
    # print(f"Doanh thu hôm nay: {total_revenue or 0}")
    return float(total_revenue or 0)


def get_daily_entries_last_n_days(days: int = 7) -> dict:
    labels = []
    data = []
    today = datetime.utcnow().date()
    
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%d/%m'))
        
        count = ParkingRecord.query.filter(
            cast(ParkingRecord.CheckInTime, Date) == day
        ).count()
        data.append(count)
    # print("Daily entries for last", days, "days:")
    # print({"labels": labels, "data": data})
    return {"labels": labels, "data": data}


def get_daily_revenue_last_n_days(days: int = 7) -> dict:
    labels = []
    data = []
    today = datetime.utcnow().date()
    
    for i in range(days - 1, -1, -1):
        day = today - timedelta(days=i)
        labels.append(day.strftime('%d/%m'))
        
        daily_sum = db.session.query(
            func.sum(ParkingRecord.ParkingFee)
        ).filter(
            cast(ParkingRecord.CheckOutTime, Date) == day
        ).scalar() or 0
        
        data.append(float(daily_sum))
    # print("Daily revenue for last", days, "days:")
    # print({"labels": labels, "data": data})
    return {"labels": labels, "data": data}


def get_monthly_revenue_last_n_months(months: int = 6) -> dict:
    query_results = db.session.query(
        extract('year', ParkingRecord.CheckOutTime).label('year'),
        extract('month', ParkingRecord.CheckOutTime).label('month'),
        func.sum(ParkingRecord.ParkingFee).label('total_revenue')
    ).filter(
        ParkingRecord.CheckOutTime >= (datetime.utcnow() - timedelta(days=months * 30))
    ).group_by('year', 'month').order_by('year', 'month').all()
    
    revenue_dict = {(r.year, r.month): float(r.total_revenue) for r in query_results}

    labels = []
    data = []
    current_date = datetime.utcnow()
    for i in range(months - 1, -1, -1):
        target_month = current_date.month - i
        target_year = current_date.year
        if target_month <= 0:
            target_month += 12
            target_year -= 1
        
        labels.append(f"Thg {target_month}/{target_year}")
        data.append(revenue_dict.get((target_year, target_month), 0))
    # print("Monthly revenue for last", months, "months:")
    # print({"labels": labels, "data": data})
    return {"labels": labels, "data": data}