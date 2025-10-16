from typing import Dict, Any, List
import json
from repositories import MysqlRepository
from _types import BaseParams

class FileService:
    def __init__(self, repository: MysqlRepository):
        self.repository = repository

    async def get_files(self, params: BaseParams) -> List[Dict[str, Any]]:
        files = await self.repository.get_files(params)
        return [self._process_file_data(file) for file in files]

    async def get_files_realtime(self) -> List[Dict[str, Any]]:
        files = await self.repository.get_files_realtime()
        return [self._process_file_data(file) for file in files]

    def _process_file_data(self, file_data: Dict[str, Any]) -> Dict[str, Any]:
        processed = file_data.copy()
        json_fields = ['company', 'organization', 'workstation', 'user']

        for field in json_fields:
            value = processed.get(field)
            if isinstance(value, str):
                try:
                    processed[field] = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    processed[field] = None
            else:
                processed[field] = value if value is not None else {}

        return processed
