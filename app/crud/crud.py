from sqlalchemy.orm import Session
from schemas.setting import SettingCreate
from models.setting import Setting


def get_settings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Setting).all()

def create_setting(db: Session, setting: SettingCreate):
    db_setting = Setting(name=setting.name, origin=setting.origin)
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting