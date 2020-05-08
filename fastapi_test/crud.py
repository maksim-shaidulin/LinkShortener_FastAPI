from sqlalchemy.orm import Session

import models
import schemas


def get_links(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Link).offset(skip).limit(limit).all()


def create_link(db: Session, link: schemas.LinkCreate):
    db_link = models.Link(link.full_link)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link


def delete_link(db: Session, short_link: str) -> models.Link:
    db_link = db.query(
        models.Link).filter(
        models.Link.short_link == short_link).first()
    if db_link:
        db.query(
            models.Link).filter(
            models.Link.short_link == short_link).delete()
        db.commit()
    return db_link


def get_by_short_link(db: Session, short_link: str):
    return db.query(
        models.Link).filter(
        models.Link.short_link == short_link).first()


def get_by_full_link(db: Session, full_link: str):
    return db.query(
        models.Link).filter(
        models.Link.full_link == full_link).first()
