from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from crud import (
    create_contact,
    get_contacts,
    get_contact_by_id,
    update_contact,
    delete_contact,
    search_contacts,
    upcoming_birthdays,
)
from database import SessionLocal, engine
from datetime import date
from models import Contact
from pydantic import BaseModel, EmailStr


class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int
    birthday: date
    additional_data: str


class Contact(ContactCreate):
    id: int

    class Config:
        orm_mode = True


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contacts/", response_model=Contact)
def create_new_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact.dict())


@app.get("/contacts/", response_model=list[Contact])
def get_all_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_contacts(db, skip=skip, limit=limit)


@app.get("/contacts/{contact_id}", response_model=Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    return get_contact_by_id(db, contact_id)


@app.put("/contacts/{contact_id}", response_model=Contact)
def update_existing_contact(
    contact_id: int, contact_data: dict, db: Session = Depends(get_db)
):
    return update_contact(db, contact_id, contact_data)


@app.delete("/contacts/{contact_id}", response_model=Contact)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    return delete_contact(db, contact_id)


@app.get("/contacts/search/", response_model=list[Contact])
def search_contacts_api(
    query: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return search_contacts(db, query, skip=skip, limit=limit)


@app.get("/contacts/upcoming_birthdays/", response_model=list[Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return upcoming_birthdays(db)
