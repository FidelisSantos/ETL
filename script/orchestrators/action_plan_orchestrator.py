import asyncio
from datetime import datetime
from typing import List
from repositories import MysqlRepository, MongoRepository
from services import ActionPlanService
from _types import BaseParams
from .base import BaseOrchestrator

class ActionPlanOrchestrator(BaseOrchestrator):
    def __init__(self, mongo_repository: MongoRepository):
        super().__init__(mongo_repository)
        self.action_plans_collection = "action_plans"
        self.realtime_action_plans_collection = "realtime_action_plans_actions"
        self.action_plans_control_collection = "action_plans_control"
    
    async def run_action_plans_etl(self, repository_standard: MysqlRepository, repository_john_deere: MysqlRepository) -> None:
        last_action_plan_control = await self.mongo_repository.base_get_last_control(self.action_plans_control_collection)
        
        default_start = datetime(2023, 1, 1, 0, 0, 0, 0)
        default_end = datetime(2023, 1, 1, 23, 59, 59, 999999)
        start_date, end_date = self._calculate_date_range(last_action_plan_control, default_start, default_end)
        
        if self._should_skip_etl(end_date):
            self._log_with_timestamp("Action plans: Difference less than 5 minutes. Skipping ETL.")
            return
        
        self._log_with_timestamp(f"Starting ETL action plans for the period of {start_date} to {end_date}")
        params = BaseParams(start_date=start_date, end_date=end_date)
        
        all_action_plans = await self._execute_all_action_plans(params, repository_standard, repository_john_deere)
        
        await self._save_action_plans(all_action_plans, start_date, end_date)
    
    async def run_realtime_action_plans_etl(self, repository_standard: MysqlRepository, repository_john_deere: MysqlRepository) -> None:
        self._log_with_timestamp("Starting ETL real time action plans")
        
        all_action_plans = await self._execute_all_realtime_action_plans(repository_standard, repository_john_deere)
        
        await self._save_realtime_action_plans(all_action_plans)
    
    async def _execute_all_action_plans(self, params: BaseParams, repo_standard: MysqlRepository, repo_john_deere: MysqlRepository) -> List:
        tasks = []
        
        tasks.append(self._run_action_plans_for_client(params, repo_standard, "standard"))
        
        tasks.append(self._run_action_plans_for_client(params, repo_john_deere, "john_deere"))
        
        results = await asyncio.gather(*tasks)
        
        standard_action_plans = results[0]
        john_deere_action_plans = results[1]
        
        self._log_with_timestamp(f"Action plans standard: {len(standard_action_plans)}")
        self._log_with_timestamp(f"Action plans john_deere: {len(john_deere_action_plans)}")
        
        all_action_plans = standard_action_plans + john_deere_action_plans
        
        self._log_with_timestamp(f"Total action plans: {len(all_action_plans)}")
        return all_action_plans
    
    async def _execute_all_realtime_action_plans(self, repo_standard: MysqlRepository, repo_john_deere: MysqlRepository) -> List:
        tasks = []
        
        tasks.append(self._run_realtime_action_plans_for_client(repo_standard, "standard"))
        
        tasks.append(self._run_realtime_action_plans_for_client(repo_john_deere, "john_deere"))
        
        results = await asyncio.gather(*tasks)
        
        standard_action_plans = results[0]
        john_deere_action_plans = results[1]
        
        self._log_with_timestamp(f"Realtime action plans standard: {len(standard_action_plans)}")
        self._log_with_timestamp(f"Realtime action plans john_deere: {len(john_deere_action_plans)}")
        
        all_action_plans = standard_action_plans + john_deere_action_plans
        
        self._log_with_timestamp(f"Total realtime action plans: {len(all_action_plans)}")
        return all_action_plans
    
    async def _run_action_plans_for_client(self, params: BaseParams, repository: MysqlRepository, client_name: str) -> List:
        try:
            service = ActionPlanService(repository)
            return await service.get_action_plan(params)
        except Exception as e:
            self._log_with_timestamp(f"Error in action plans for {client_name}: {e}")
            raise e
    
    async def _run_realtime_action_plans_for_client(self, repository: MysqlRepository, client_name: str) -> List:
        try:
            service = ActionPlanService(repository)
            return await service.get_action_plan_realtime()
        except Exception as e:
            self._log_with_timestamp(f"Error in realtime action plans for {client_name}: {e}")
            raise e
    
    async def _save_action_plans(self, all_action_plans: List, start_date: datetime, end_date: datetime) -> None:
        await self.mongo_repository.bulk_upsert_action_plans(self.action_plans_collection, all_action_plans)
        
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "extracted_at": datetime.now(),
            "rows": len(all_action_plans)
        }
        await self.mongo_repository.base_insert_control(self.action_plans_control_collection, data)
    
    async def _save_realtime_action_plans(self, all_action_plans: List) -> None:
        self._log_with_timestamp(f"Inserting {len(all_action_plans)} realtime action plans")
        await self.mongo_repository.base_bulk_insert_realtime(self.realtime_action_plans_collection, all_action_plans)
