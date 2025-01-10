from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from database import database, metadata, engine
from crud import create_user, get_users
from models import users  # Ensure this import is present
from dotenv import load_dotenv
import sqlalchemy

# Load environment variables from .env file if it exists
load_dotenv()

# Function to check if the table exists and create it if it does not
def ensure_table_exists(engine, table_name):
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table(table_name):
        metadata.create_all(engine)

# Ensure the users table exists
ensure_table_exists(engine, "users")

# Create FastAPI application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await database.connect()
    yield
    # Shutdown event
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Endpoint to create a user
@app.post("/users/")
async def add_user(name: str, email: str):
    try:
        user_id = await create_user(name, email)
        return {"id": user_id, "name": name, "email": email}
    except Exception as e:
        raise HTTPException(status_code=400, detail="User could not be created.")

# Endpoint to get all users
@app.get("/users/")
async def list_users():
    return await get_users()

@app.get("/db-test")
async def test_db():
    try:
        query = "SELECT 1"
        result = await database.fetch_one(query)
        return {"message": "Database connection successful", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")