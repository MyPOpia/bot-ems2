# database.py
import asyncpg
import os

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        await self.create_table()

    async def create_table(self):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ems_profiles (
                    discord_id BIGINT PRIMARY KEY,
                    nom TEXT,
                    prenom TEXT,
                    heures_service DOUBLE PRECISION DEFAULT 0
                );
            """)

    async def create_profile(self, discord_id, nom, prenom):
        async with self.pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO ems_profiles (discord_id, nom, prenom)
                VALUES ($1, $2, $3)
                ON CONFLICT (discord_id) DO NOTHING;
            """, discord_id, nom, prenom)

    async def has_profile(self, discord_id):
        async with self.pool.acquire() as conn:
            result = await conn.fetchval("""
                SELECT COUNT(*) FROM ems_profiles WHERE discord_id = $1;
            """, discord_id)
            return result > 0

    async def get_profile(self, discord_id):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow("""
                SELECT * FROM ems_profiles WHERE discord_id = $1;
            """, discord_id)

db = Database()
