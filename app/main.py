from fastapi import FastAPI, HTTPException

import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Database configuration
DB_NAME = os.getenv("POSTGRES_DB", "mydatabase")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")  # Kubernetes-tjänstens namn
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# FastAPI instance
app = FastAPI()

# Funktion för att ansluta till databasen
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Routes
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgreSQL"}

@app.get("/db-test")
def test_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return {"db_test": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database test failed: {str(e)}")

# Lägg till en användare
@app.post("/users/")
def create_user(name: str, email: str):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;", (name, email))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"id": user_id, "name": name, "email": email}
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

# Läs alla användare
@app.get("/users/")
def get_users():
    conn = get_db_connection()
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users;")
        users = cur.fetchall()
        cur.close()
        conn.close()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

# Ta bort en användare
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
        deleted_user = cur.fetchone()
        if not deleted_user:
            raise HTTPException(status_code=404, detail="User not found")
        conn.commit()
        cur.close()
        conn.close()
        return {"message": f"User with id {user_id} has been deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
