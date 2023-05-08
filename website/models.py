from . import db
from sqlalchemy.sql import func

# create a database model


class Temperature(db.Model):
    __tablename__ = "CM_HAM_DO_AI1/Temp_value"
    time = db.Column(db.DateTime(timezone=False), primary_key=True)
    value = db.Column(db.Float)


class pH(db.Model):
    __tablename__ = "CM_HAM_PH_AI1/pH_value"
    time = db.Column(db.DateTime(timezone=False), primary_key=True)
    value = db.Column(db.Float)


class Distilled_Oxygen(db.Model):
    __tablename__ = "CM_PID_DO/Process_DO"
    time = db.Column(db.DateTime(timezone=False), primary_key=True)
    value = db.Column(db.Float)


class Pressure(db.Model):
    __tablename__ = "CM_PRESSURE/Output"
    time = db.Column(db.DateTime(timezone=False), primary_key=True)
    value = db.Column(db.Float)
