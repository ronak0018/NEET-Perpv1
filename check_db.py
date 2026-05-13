import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    c = AsyncIOMotorClient("mongodb+srv://ronakmeandeveloper_db_user:OtNMxQE3DdzdWwyo@cluster0.ic6ndjr.mongodb.net/?retryWrites=true&w=majority")
    print("Databases:", await c.list_database_names())
    print("neetpg collections:", await c["neetpg"].list_collection_names())
    print("neetpg questions:", await c["neetpg"].questions.count_documents({}))
    c.close()

asyncio.run(main())
