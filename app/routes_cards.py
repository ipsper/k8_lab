from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from logger_config import logger

DATABASE_URL = "postgresql://user:your_password@192.168.1.120:5432/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Card table
class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for the request body
class CardCreate(BaseModel):
    title: str
    description: str

# Create a router for the cards endpoints
router = APIRouter()

# Endpoint to create a new card
@router.post("/cards/")
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    try:
        new_card = Card(title=card.title, description=card.description)
        db.add(new_card)
        db.commit()
        db.refresh(new_card)
        logger.info("Card added successfully", extra={"card": new_card})
        return {"message": "Card added successfully", "card": new_card}
    except Exception as e:
        db.rollback()
        logger.error("Error adding card", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Endpoint to read all cards from the database
@router.get("/cards/")
def read_cards(db: Session = Depends(get_db)):
    try:
        cards = db.query(Card).all()
        logger.info("Fetched all cards")
        return {"cards": cards}
    except Exception as e:
        logger.error("Error fetching cards", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")