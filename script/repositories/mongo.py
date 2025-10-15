from typing import Any, Dict, List
import motor.motor_asyncio
from pymongo import UpdateOne

class MongoRepository:
    def __init__(self, uri: str, database: str):
        self.uri = uri
        self.database = database
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db = self.client[self.database]

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def _get_collection(self, collection: str):
        return self.db[collection]

    async def start_session(self):
        session = await self.client.start_session()
        return session

    async def insert_one(self, collection: str, data: Dict[str, Any]):
        col = self._get_collection(collection)
        result = await col.insert_one(data)
        return result.inserted_id

    async def insert_many(self, collection: str, data: List[Dict[str, Any]]):
        if not data:
            return []
        col = self._get_collection(collection)
        result = await col.insert_many(data)
        return result.inserted_ids

    async def bulk_upsert_reports(self, collection: str, reports: List[Any]):
        if not reports:
            return

        col = self._get_collection(collection)
        bulk_ops = []

        for report in reports:
            filter_query = {
                "report_id": report.report_id,
                "type": report.type,
                "created_at": report.created_at,
                "client": report.client
            }
            update_query = {"$set": report.create()}
            bulk_ops.append(UpdateOne(filter_query, update_query, upsert=True))

        if bulk_ops:
            await col.bulk_write(bulk_ops)

    
    async def bulk_insert_realtime_reports(self, collection: str, reports: List[Any]):
        if not reports:
            return

        col = self._get_collection(collection)
    
        await col.delete_many({})
        
        if reports:
            await col.insert_many([report.create() for report in reports])

    async def insert_report_control(self, data: Dict[str, Any]):
        col = self._get_collection("report_control")
        result = await col.insert_one(data)
        return result.inserted_id


    async def get_last_report_control(self) -> Dict[str, Any]:
        col = self._get_collection("report_control")
        result = await col.find_one(sort=[("extracted_at", -1)])
        return result

    async def bulk_upsert_files(self, collection: str, files: List[Any]):
        if not files:
            return

        col = self._get_collection(collection)
        bulk_ops = []

        for file in files:
            
            filter_query = {
                "file_id": file["file_id"],
                "created_at": file["created_at"]
            }

            update_query = {"$set": file}  
            bulk_ops.append(UpdateOne(filter_query, update_query, upsert=True))

        if bulk_ops:
            await col.bulk_write(bulk_ops)
    
    
    async def bulk_insert_realtime_files(self, collection: str, files: List[Any]):
        if not files:
            return

        col = self._get_collection(collection)
        await col.delete_many({})

        if files:
            await col.insert_many(files)
    
    async def insert_file_control(self, data: Dict[str, Any]):
        col = self._get_collection("file_control")
        result = await col.insert_one(data)
        return result.inserted_id
    
    async def get_last_file_control(self) -> Dict[str, Any]:
        col = self._get_collection("file_control")
        result = await col.find_one(sort=[("extracted_at", -1)])
        return result