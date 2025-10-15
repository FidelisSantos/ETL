import asyncio
from datetime import datetime
from typing import List
from repositories import MysqlRepository, MongoRepository
from services import FileService
from _types import FileParams
from .base import BaseOrchestrator

class FilesOrchestrator(BaseOrchestrator):
    def __init__(self, mongo_repository: MongoRepository):
        super().__init__(mongo_repository)
        self.files_collection = "files"
        self.realtime_files_collection = "realtime_files"
    
    async def run_files_etl(self, repository_standard: MysqlRepository, repository_john_deere: MysqlRepository) -> None:
        last_file_control = await self.mongo_repository.get_last_file_control()
        
        default_start = datetime(2023, 1, 1, 0, 0, 0, 0)
        default_end = datetime(2023, 1, 1, 23, 59, 59, 999999)
        start_date, end_date = self._calculate_date_range(last_file_control, default_start, default_end)
        
        if self._should_skip_etl(end_date):
            self._log_with_timestamp("Difference less than 5 minutes. Skipping ETL.")
            return
        
        self._log_with_timestamp(f"Starting ETL files for the period of {start_date} to {end_date}")
        params = FileParams(start_date=start_date, end_date=end_date)
        
        all_files = await self._execute_all_files(params, repository_standard, repository_john_deere)
        
        await self._save_files(all_files, start_date, end_date)
    
    async def run_realtime_files_etl(self, repository_standard: MysqlRepository, repository_john_deere: MysqlRepository) -> None:
        self._log_with_timestamp("Starting ETL real time files")
        
        all_files = await self._execute_all_realtime_files(repository_standard, repository_john_deere)
        
        await self._save_realtime_files(all_files)
    
    async def _execute_all_files(self, params: FileParams, repo_standard: MysqlRepository, repo_john_deere: MysqlRepository) -> List:
        tasks = []
        
        tasks.append(self._run_files_for_client(params, repo_standard, "standard"))
        
        tasks.append(self._run_files_for_client(params, repo_john_deere, "john_deere"))
        
        results = await asyncio.gather(*tasks)
        
        standard_files = results[0]
        john_deere_files = results[1]
        
        self._log_with_timestamp(f"Files standard: {len(standard_files)}")
        self._log_with_timestamp(f"Files john_deere: {len(john_deere_files)}")
        
        all_files = standard_files + john_deere_files
        
        self._log_with_timestamp(f"Total files: {len(all_files)}")
        return all_files
    
    async def _execute_all_realtime_files(self, repo_standard: MysqlRepository, repo_john_deere: MysqlRepository) -> List:
        tasks = []
        
        tasks.append(self._run_realtime_files_for_client(repo_standard, "standard"))
        
        tasks.append(self._run_realtime_files_for_client(repo_john_deere, "john_deere"))
        
        results = await asyncio.gather(*tasks)
        
        standard_files = results[0]
        john_deere_files = results[1]
        
        self._log_with_timestamp(f"Realtime files standard: {len(standard_files)}")
        self._log_with_timestamp(f"Realtime files john_deere: {len(john_deere_files)}")
        
        all_files = standard_files + john_deere_files
        
        self._log_with_timestamp(f"Total realtime files: {len(all_files)}")
        return all_files
    
    async def _run_files_for_client(self, params: FileParams, repository: MysqlRepository, client_name: str) -> List:
        try:
            service = FileService(repository)
            return await service.get_files(params)
        except Exception as e:
            self._log_with_timestamp(f"Error in files for {client_name}: {e}")
            raise e
    
    async def _run_realtime_files_for_client(self, repository: MysqlRepository, client_name: str) -> List:
        try:
            service = FileService(repository)
            return await service.get_files_realtime()
        except Exception as e:
            self._log_with_timestamp(f"Error in realtime files for {client_name}: {e}")
            raise e
    
    async def _save_files(self, all_files: List, start_date: datetime, end_date: datetime) -> None:
        await self.mongo_repository.bulk_upsert_files(self.files_collection, all_files)
        
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "extracted_at": datetime.now(),
            "rows": len(all_files)
        }
        await self.mongo_repository.insert_file_control(data)
    
    async def _save_realtime_files(self, all_files: List) -> None:
        self._log_with_timestamp(f"Inserting {len(all_files)} realtime files")
        await self.mongo_repository.bulk_insert_realtime_files(self.realtime_files_collection, all_files)
