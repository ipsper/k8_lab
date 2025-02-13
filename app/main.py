from fastapi import FastAPI
from routes_cards import router as cards_router  # Import the cards router
from routes_users import router as users_router  # Import the cards router

app = FastAPI()

# Include the cards router
app.include_router(cards_router)
app.include_router(users_router)