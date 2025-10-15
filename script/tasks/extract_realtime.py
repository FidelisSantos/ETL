import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from repositories import MysqlRepository, MongoRepository
from orchestrators import ReportsOrchestrator, FilesOrchestrator
from utils import env

async def main():
    mongo_repository = MongoRepository(uri=env.MONGO_URI, database=env.MONGO_DATABASE)
    reports_orchestrator = ReportsOrchestrator(mongo_repository)
    files_orchestrator = FilesOrchestrator(mongo_repository)
    
    async with MysqlRepository(url=env.STANDARD_MYSQL_URL, client="STANDARD") as repository_standard,\
        MysqlRepository(url=env.JOHN_DEERE_MYSQL_URL, client="JOHN_DEERE") as repository_john_deere:
        
        while True:
            try:
                await reports_orchestrator.run_realtime_reports_etl(repository_standard, repository_john_deere)
                
                await files_orchestrator.run_realtime_files_etl(repository_standard, repository_john_deere)
            except Exception as e:
                print(f"Error: {e}")
            
            await asyncio.sleep(5) 
        
        

if __name__ == "__main__":
    asyncio.run(main())
