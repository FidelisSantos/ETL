import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from repositories import MysqlRepository, MongoRepository
from orchestrators import ReportsOrchestrator, FilesOrchestrator, ActionPlanOrchestrator
from utils import env

async def main():
    mongo_repository = MongoRepository(uri=env.MONGO_URI, database=env.MONGO_DATABASE)
    reports_orchestrator = ReportsOrchestrator(mongo_repository)
    files_orchestrator = FilesOrchestrator(mongo_repository)
    action_plan_orchestrator = ActionPlanOrchestrator(mongo_repository)
    
    async with MysqlRepository(url=env.STANDARD_MYSQL_URL, client="STANDARD") as repository_standard,\
        MysqlRepository(url=env.JOHN_DEERE_MYSQL_URL, client="JOHN_DEERE") as repository_john_deere:
        
        while True:
            try:
                print("Starting Realtime ETL cycle...", flush=True)
                await reports_orchestrator.run_realtime_reports_etl(repository_standard, repository_john_deere)
                print("Realtime Reports ETL completed", flush=True)
                
                await files_orchestrator.run_realtime_files_etl(repository_standard, repository_john_deere)
                print("Realtime Files ETL completed", flush=True)
                
                await action_plan_orchestrator.run_realtime_action_plans_etl(repository_standard, repository_john_deere)
                print("Realtime Action Plans ETL completed", flush=True)
                
                print("Realtime ETL cycle completed successfully", flush=True)
            except Exception as e:
                print(f"Error in Realtime ETL cycle: {e}", flush=True)
            
            sleep_time = int(env.JOB_REALTIME_SLEEP_SECONDS)
            print(f"Extract realtime: Sleeping for {sleep_time} seconds", flush=True)
            await asyncio.sleep(sleep_time) 
        
        

if __name__ == "__main__":
    asyncio.run(main())
