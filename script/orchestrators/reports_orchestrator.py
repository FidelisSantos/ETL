import asyncio
from datetime import datetime
from typing import List
from repositories import MysqlRepository, MongoRepository
from services import ReportService
from _types import ReportParams
from .base import BaseOrchestrator

class ReportsOrchestrator(BaseOrchestrator):
    def __init__(self, mongo_repository: MongoRepository):
        super().__init__(mongo_repository)
        self.report_types = ["reba", "kim_mho", "kim_pp", "niosh", "strain_index"]
        self.reports_collection = "reports"
        self.realtime_reports_collection = "realtime_reports"
    
    async def _run_report(self, report_type: str, params: ReportParams, repository: MysqlRepository) -> List:
        try:
            service = ReportService(repository, report_type)
            return await service.get_reports(params)
        except Exception as e:
            self._log_with_timestamp(f"Error in {report_type}: {e}")
            raise e
    
    async def _run_realtime_report(self, report_type: str, repository: MysqlRepository) -> List:
        try:
            service = ReportService(repository, report_type)
            return await service.get_realtime_reports()
        except Exception as e:
            self._log_with_timestamp(f"Error in {report_type}: {e}")
            raise e
    
    async def run_reports_etl(self, repository_standard: MysqlRepository, repository_john_deere: MysqlRepository) -> None:
        last_report_control = await self.mongo_repository.get_last_report_control()
        
        default_start = datetime(2023, 1, 1, 0, 0, 0, 0)
        default_end = datetime(2023, 2, 28, 23, 59, 59, 999999)
        start_date, end_date = self._calculate_date_range(last_report_control, default_start, default_end)
        
        if self._should_skip_etl(end_date):
            self._log_with_timestamp("Difference less than 5 minutes. Skipping ETL.")
            return
        
        self._log_with_timestamp(f"Starting ETL reports for the period of {start_date} to {end_date}")
        params = ReportParams(start_date=start_date, end_date=end_date)
        
        all_reports = await self._execute_all_reports(params, repository_standard, repository_john_deere)
        
        
        await self._save_reports(all_reports, start_date, end_date)
    
    async def run_realtime_reports_etl(self, repository_standard: MysqlRepository, repository_john_deere: MysqlRepository) -> None:
        self._log_with_timestamp("Starting ETL real time reports")
        
        all_reports = await self._execute_all_realtime_reports(repository_standard, repository_john_deere)
        
        await self._save_realtime_reports(all_reports)
    
    async def _execute_all_reports(self, params: ReportParams, repo_standard: MysqlRepository, repo_john_deere: MysqlRepository) -> List:
        tasks = []
        
        for report_type in self.report_types:
            tasks.append(self._run_report(report_type, params, repo_standard))
        
        for report_type in self.report_types:
            tasks.append(self._run_report(report_type, params, repo_john_deere))
        
        results = await asyncio.gather(*tasks)
        
        standard_reports = results[:5] 
        john_deere_reports = results[5:] 
        
        for i, report_type in enumerate(self.report_types):
            self._log_with_timestamp(f"Reports {report_type} standard: {len(standard_reports[i])}")
            self._log_with_timestamp(f"Reports {report_type} john_deere: {len(john_deere_reports[i])}")
        
        all_reports = []
        for reports in results:
            all_reports.extend(reports)
        
        self._log_with_timestamp(f"Total reports: {len(all_reports)}")
        return all_reports
    
    async def _execute_all_realtime_reports(self, repo_standard: MysqlRepository, repo_john_deere: MysqlRepository) -> List:
        tasks = []
        
        for report_type in self.report_types:
            tasks.append(self._run_realtime_report(report_type, repo_standard))
        
        for report_type in self.report_types:
            tasks.append(self._run_realtime_report(report_type, repo_john_deere))
        
        results = await asyncio.gather(*tasks)
        
        standard_reports = results[:5] 
        john_deere_reports = results[5:] 
        
        for i, report_type in enumerate(self.report_types):
            self._log_with_timestamp(f"Realtime reports {report_type} standard: {len(standard_reports[i])}")
            self._log_with_timestamp(f"Realtime reports {report_type} john_deere: {len(john_deere_reports[i])}")
        
        all_reports = []
        for reports in results:
            all_reports.extend(reports)
        
        self._log_with_timestamp(f"Total realtime reports: {len(all_reports)}")
        return all_reports
    
    async def _save_reports(self, all_reports: List, start_date: datetime, end_date: datetime) -> None:
        await self.mongo_repository.bulk_upsert_reports(self.reports_collection, all_reports)
        
        data = {
            "start_date": start_date,
            "end_date": end_date,
            "extracted_at": datetime.now(),
            "rows": len(all_reports)
        }
        await self.mongo_repository.insert_report_control(data)
    
    async def _save_realtime_reports(self, all_reports: List) -> None:
        self._log_with_timestamp(f"Inserting {len(all_reports)} realtime reports")
        await self.mongo_repository.bulk_insert_realtime_reports(self.realtime_reports_collection, all_reports)
