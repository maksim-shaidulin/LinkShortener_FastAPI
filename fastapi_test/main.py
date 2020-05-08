import uvicorn
from typing import List

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
root_api_path = '/api/v1/link/'


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get(root_api_path, response_model=List[schemas.Link])
def read_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    links = crud.get_links(db, skip=skip, limit=limit)
    return links


@app.get(root_api_path + '{short_link}', response_model=schemas.Link)
def read_link(short_link: str, db: Session = Depends(get_db)):
    link = crud.get_by_short_link(db, short_link)
    return link


@app.post(root_api_path, response_model=schemas.Link)
def create_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    db_link = crud.get_by_full_link(db, full_link=link.full_link)
    if db_link:
        return db_link
    return crud.create_link(db=db, link=link)


@app.delete(root_api_path + '{short_link}', response_model=schemas.Link)
def delete_link(short_link: str, db: Session = Depends(get_db)):
    return crud.delete_link(db, short_link)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
