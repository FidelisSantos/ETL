from typing import Dict, Any, List
import json
from repositories import MysqlRepository
from _types import BaseParams

class ActionPlanService:
    def __init__(self, repository: MysqlRepository):
        self.repository = repository

    async def get_action_plan(self, params: BaseParams) -> List[Dict[str, Any]]:
        action_plan = await self.repository.get_action_plan(params)
        return [self._process_action_plan_data(action_plan) for action_plan in action_plan]

    async def get_action_plan_realtime(self) -> List[Dict[str, Any]]:
        action_plan = await self.repository.get_action_plan_realtime()
        return [self._process_action_plan_data(action_plan) for action_plan in action_plan]

    def _process_action_plan_data(self, action_plan_data: Dict[str, Any]) -> Dict[str, Any]:
        processed = action_plan_data.copy()
        json_fields = ['action_plan', 'file', 'company', 'organization', 'workstation']

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
