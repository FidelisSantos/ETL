import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from repositories import MysqlRepository, MongoRepository
from orchestrators import ReportsOrchestrator, FilesOrchestrator
from utils import env

async def main():
    print("Starting ETL extract process...")
    print(f"MONGO_URI: {env.MONGO_URI}")
    print(f"STANDARD_MYSQL_URL: {env.STANDARD_MYSQL_URL}")
    print(f"JOHN_DEERE_MYSQL_URL: {env.JOHN_DEERE_MYSQL_URL}")
    
    try:
        mongo_repository = MongoRepository(uri=env.MONGO_URI, database=env.MONGO_DATABASE)
        print("MongoDB repository created successfully")
        
        reports_orchestrator = ReportsOrchestrator(mongo_repository)
        files_orchestrator = FilesOrchestrator(mongo_repository)
        print("Orchestrators created successfully")
        
        async with MysqlRepository(url=env.STANDARD_MYSQL_URL, client="STANDARD") as repository_standard,\
            MysqlRepository(url=env.JOHN_DEERE_MYSQL_URL, client="JOHN_DEERE") as repository_john_deere:
            
            print("MySQL repositories connected successfully")
            
            while True:
                try:
                    print("Running reports ETL...")
                    await reports_orchestrator.run_reports_etl(repository_standard, repository_john_deere)
                    print("Reports ETL completed")
                
                    print("Running files ETL...")
                    await files_orchestrator.run_files_etl(repository_standard, repository_john_deere)
                    print("Files ETL completed")
                    
                except Exception as e:
                    print(f"Error in ETL process: {e}")
                    import traceback
                    traceback.print_exc()
                
                print("Waiting 5 seconds before next iteration...")
                await asyncio.sleep(5)
                
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc() 

if __name__ == "__main__":
    asyncio.run(main())
