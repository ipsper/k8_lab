from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from logger_config import logger
from routes_cards import router as cards_router  # Import the cards router

DATABASE_URL = "postgresql://user:your_password@192.168.1.120:5432/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Definiera tabeller
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(TIMESTAMP, server_default=func.now())  # Add created_at column
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)


# Initiera databasen
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency för att få en databas-session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    name: str
    email: str

# Lägg till en ny användare
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = User(name=user.name, email=user.email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info("User added successfully", extra={"user": new_user})
        return {"message": "User added successfully", "user": new_user}
    except Exception as e:
        db.rollback()
        logger.error("Error adding user", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

# Läs alla användare från databasen
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        logger.info("Fetched all users")
        return {"users": users}
    except Exception as e:
        logger.error("Error fetching users", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    
# Include the cards router
app.include_router(cards_router)