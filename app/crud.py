from app.database import database
from app.models import users

# Skapa en användare
async def create_user(name: str, email: str):
    query = users.insert().values(name=name, email=email)
    return await database.execute(query)

# Hämta alla användare
async def get_users():
    query = users.select()
    return await database.fetch_all(query)
