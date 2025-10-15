from datetime import datetime
from typing import Dict, Any

class ReportMongoSchema:
    def __init__(self, report_id: str, type: str, created_at: datetime, updated_at: datetime, 
                 is_active: bool, risk: str, name: str, client: str, file: Dict[str, Any],
                 company: Dict[str, Any], organization: Dict[str, Any], workstation: Dict[str, Any]):
        self.report_id = report_id
        self.type = type
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_active = is_active
        self.risk = risk
        self.name = name
        self.client = client
        self.file = file
        self.company = company
        self.organization = organization
        self.workstation = workstation
    
    def create(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "type": self.type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "risk": self.risk,
            "name": self.name,
            "client": self.client,
            "file": self.file,
            "company": self.company,
            "organization": self.organization,
            "workstation": self.workstation
        }