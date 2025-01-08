from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

# Exempel: User-tabellen
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(100)),
    Column("email", String(100), unique=True),
)
