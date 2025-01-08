from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.database import database, metadata, engine
from app.crud import create_user, get_users

# Initiera metadata (skapa tabeller)
metadata.create_all(engine)

# Skapa FastAPI-applikationen
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    await database.connect()
    yield
    # Shutdown event
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# Endpoint för att skapa en användare
@app.post("/users/")
async def add_user(name: str, email: str):
    try:
        user_id = await create_user(name, email)
        return {"id": user_id, "name": name, "email": email}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Användaren kunde inte skapas.")

# Endpoint för att hämta alla användare
@app.get("/users/")
async def list_users():
    return await get_users()