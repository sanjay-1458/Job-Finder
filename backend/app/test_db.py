import asyncio
import asyncpg

DATABASE_URL = (
    "postgresql://postgres.queupmjpvzbrerremgke:MyPassword12312121212121"
    "@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
)

async def test_connection():

    try:

        conn = await asyncpg.connect(
            DATABASE_URL,
            ssl="require"
        )

        print("Database connected successfully")

        version = await conn.fetchval(
            "SELECT version();"
        )

        print(version)

        await conn.close()

    except Exception as e:

        print("Connection failed")
        print(e)

asyncio.run(test_connection())