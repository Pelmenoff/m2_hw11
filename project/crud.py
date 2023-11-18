from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Contact
from datetime import datetime, timedelta


def create_contact(db: Session, contact_data: dict):
    db_contact = Contact(**contact_data)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Contact).offset(skip).limit(limit).all()


def get_contact_by_id(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()


def update_contact(db: Session, contact_id: int, contact_data: dict):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    for key, value in contact_data.items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(db_contact)
    db.commit()


def search_contacts(db: Session, query: str, skip: int = 0, limit: int = 10):
    return (
        db.query(Contact)
        .filter(
            or_(
                Contact.first_name.ilike(f"%{query}%"),
                Contact.last_name.ilike(f"%{query}%"),
                Contact.email.ilike(f"%{query}%"),
            )
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def upcoming_birthdays(db: Session):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    return db.query(Contact).filter(Contact.birthday.between(today, next_week)).all()
