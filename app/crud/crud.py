from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
# SCHEMAS
from schemas.sensor import SensorCreate, SensorList
from schemas.setting import SettingCreate
from schemas.waypoint import WaypointCreate, AbstractWaypoint
from schemas.waypoint_session import WaypointSessionCreate, WaypointSessionUpdate
# MODELS
from models.sensor import Sensor
from models.setting import Setting
from models.waypoint import Waypoint
from models.waypoint_session import WaypointSession
# SPECIAL FUNCTIONS
from api.endpoints.videos import save_img

""" SETTING """

def get_settings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Setting).offset(skip).limit(limit).all()

def create_setting(db: Session, setting: SettingCreate):
    db_setting = Setting(name=setting.name, origin=setting.origin)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting


""" WAYPOINT """


def get_waypoint(db: Session, waypoint_id: int):
    return db.query(Waypoint).filter(Waypoint.id == waypoint_id).first()


def get_waypoints(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Waypoint).offset(skip).limit(limit).all()


def get_waypoints_by_session_id(db: Session, session_id: str):
    return db.query(Waypoint).filter(Waypoint.session_id == session_id).all()


def create_waypoint(db: Session, sess_id: str, lat: float, lng: float, sensors):
    # Special function to save and get img name
    # Could also try via requests to prevent circle deps. if it happens
    img_name = save_img()
    db_waypoint = Waypoint(
        img_name=img_name,
        session_id=sess_id,
        latitude=lat,
        longitude=lng)
    db.add(db_waypoint)
    sensor_data = []
    for sensor in sensors:
        new_sensor = Sensor(name=sensor["name"], value=sensor["value"])
        new_sensor.owner = db_waypoint
        sensor_data.append(new_sensor)
    db.add_all(sensor_data)
    db.commit()
    return db_waypoint


def update_waypoint(db: Session, setting: SettingCreate):
    pass


def delete_waypoints_by_session_id(db: Session, session_id: str):
    waypoints = db.query(Waypoint).filter(
        Waypoint.session_id == session_id).all()
    if not waypoints:
        code = 404
    else:
        code = 200
        for waypoint in waypoints:
            db.delete(waypoint)
    db.commit()
    return {"code": code}


""" WAYPOINT SESSIONS """

def get_waypoint_session(db: Session, session_id: str):
    return db.query(WaypointSession).filter(WaypointSession.session_id == session_id).one_or_none()

def get_waypoint_sessions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(WaypointSession).offset(skip).limit(limit).all()

def get_complete_waypoint_sessions(db: Session, is_complete: bool):
    return db.query(WaypointSession).filter(WaypointSession.is_complete == is_complete).all()

def create_waypoint_session(db: Session, waypoint_session: WaypointSessionCreate):
    db_wp_session = WaypointSession(session_id=waypoint_session.session_id)
    db.add(db_wp_session)
    db.commit()
    db.refresh(db_wp_session)
    return db_wp_session

def update_waypoint_session(db: Session, waypoint_session: WaypointSessionUpdate):
        # get the existing data
    db_wp_session = db.query(WaypointSession).filter(WaypointSession.session_id == waypoint_session.session_id).first()
    if db_wp_session is None:
        return None

    # Update model class variable from requested fields 
    for updateKey, updateValue in vars(waypoint_session).items():
        setattr(db_wp_session, updateKey, updateValue) if updateValue else None

    db.add(db_wp_session)
    db.commit()
    db.refresh(db_wp_session)
    return db_wp_session

# def utc2local(utc):
#     # Use this before displaying to client
#     epoch = time.mktime(utc.timetuple())
#     offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)
#     return utc + offset
