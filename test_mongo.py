import asyncio, os, traceback
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "backend", ".env"))
from motor.motor_asyncio import AsyncIOMotorClient

async def test():
    try:
        url = os.getenv("MONGODB_URL")
        print(f"URL: {url[:40]}...")
        client = AsyncIOMotorClient(url, serverSelectionTimeoutMS=15000)
        await client.admin.command("ping")
        print("SUCCESS: Connected to MongoDB Atlas!")
        dbs = await client.list_database_names()
        print(f"Databases: {dbs}")
        client.close()
    except Exception as e:
        traceback.print_exc()

asyncio.run(test())
