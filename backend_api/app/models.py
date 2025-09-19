import hashlib
from app import db
from datetime import datetime


class Status(db.Model):
    __tablename__ = 'Status'

    StatusID = db.Column(db.Integer, primary_key=True)
    StatusName = db.Column(db.String(50), nullable=False, unique=True)
    
    records = db.relationship('ParkingRecord', backref='status', lazy=True)

    def __repr__(self):
        return f"<Status {self.StatusID} - {self.StatusName}>"

class Vehicle(db.Model):
    __tablename__ = 'Vehicles'

    VehicleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    LicensePlate = db.Column(db.String(20), nullable=False, unique=True)
    VehicleType = db.Column(db.String(50), nullable=True)
    FirstSeen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    records = db.relationship('ParkingRecord', backref='vehicle', lazy=True)

    def __repr__(self):
        return f"<Vehicle {self.VehicleID} - {self.LicensePlate}>"


class ParkingRecord(db.Model):
    __tablename__ = 'ParkingRecords'

    RecordID = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    
    VehicleID = db.Column(db.Integer, db.ForeignKey('Vehicles.VehicleID'), nullable=False)
    
    StatusID = db.Column(db.Integer, db.ForeignKey('Status.StatusID'), nullable=False)

    CheckInTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    CheckOutTime = db.Column(db.DateTime, nullable=True)
    ParkingFee = db.Column(db.Numeric(10, 2), nullable=True)

    def __repr__(self):
        return f"<ParkingRecord {self.RecordID} - Vehicle: {self.vehicle.LicensePlate}>"