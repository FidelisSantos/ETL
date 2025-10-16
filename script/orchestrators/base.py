from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from repositories import MongoRepository
from utils import env

class BaseOrchestrator:
    """Classe base para orquestradores ETL"""
    
    def __init__(self, mongo_repository: MongoRepository):
        self.mongo_repository = mongo_repository
    
    def _calculate_date_range(self, last_control: Optional[Dict], default_start: datetime, default_end: datetime) -> tuple[datetime, datetime]:
        """Calcula o range de datas baseado no último controle"""
        diff_type = env.DIFF_TYPE
        offset = int(env.OFFSET)
        if last_control:
            start_date = last_control["end_date"] + timedelta(seconds=1)
            end_date = last_control["end_date"] + timedelta(**{diff_type: offset})
        else:
            start_date = default_start
            end_date = default_end
        
        return start_date, end_date
    
    def _should_skip_etl(self, end_date: datetime, minutes_threshold: int = 5) -> bool:
        """Verifica se deve pular o ETL baseado no tempo"""
        now = datetime.now()
        return (now - end_date) < timedelta(minutes=minutes_threshold)
    
    def _log_with_timestamp(self, message: str) -> None:
        """Log com timestamp formatado"""
        print(f"[{datetime.now()}] {message}")
