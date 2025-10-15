from typing import List, Dict, Any, Literal
import json
from repositories import MysqlRepository
from _types import ReportParams
from entities import RiskCalculator
from schemas import ReportMongoSchema

class ReportService:
    def __init__(self, repository: MysqlRepository, report_name: Literal["reba", "niosh", "kim_mho", "kim_pp", "strain_index"]):
        self.repository = repository
        self.report_name = report_name
        self._map_reports = {
            "reba": {
                'get': self.repository.get_reba,
                'get_realtime': self.repository.get_realtime_reba,
            },
            "niosh": {
                'get': self.repository.get_niosh,
                'get_realtime': self.repository.get_realtime_niosh,
            },
            "kim_mho": {
                'get': self.repository.get_kim_mho,
                'get_realtime': self.repository.get_realtime_kim_mho,
            },
            "kim_pp": {
                'get': self.repository.get_kim_push_pull,
                'get_realtime': self.repository.get_realtime_kim_push_pull,
            },
            "strain_index": {
                'get': self.repository.get_strain_index,
                'get_realtime': self.repository.get_realtime_strain_index,
            },
        }

    async def get_reports(self, params: ReportParams) -> List[Dict[str, Any]]:
        reports = await self._map_reports[self.report_name]['get'](params)
        return [self._mount_mongo_schema(report, self.report_name) for report in reports]

    async def get_realtime_reports(self) -> List[Dict[str, Any]]:
        reports = await self._map_reports[self.report_name]['get_realtime']()
        return [self._mount_mongo_schema(report, self.report_name) for report in reports]

    def _mount_mongo_schema(self, report: Dict[str, Any], report_name: str) -> Dict[str, Any]:
        data = RiskCalculator.calculate_risk(report_name, report)
        return ReportMongoSchema(
            report_id=data["id"],
            type=data["type"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            is_active=bool(data["is_active"]),
            risk=data["risk"],
            name=data.get("report_name") or data.get("name") or "",
            client=data["client"],
            file=json.loads(data["file"]) if isinstance(data["file"], str) else data["file"],
            company=json.loads(data["company"]) if isinstance(data["company"], str) else data["company"],
            organization=json.loads(data["organization"]) if isinstance(data["organization"], str) else data["organization"],
            workstation=json.loads(data["workstation"]) if isinstance(data["workstation"], str) else data["workstation"]
        )