from typing import TypedDict
import datetime

class ReportParams(TypedDict):
    start_date: datetime.datetime
    end_date: datetime.datetime

class FileParams(TypedDict):
    start_date: datetime.datetime
    end_date: datetime.datetime