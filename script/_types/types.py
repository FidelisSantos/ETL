from typing import TypedDict
import datetime

class BaseParams(TypedDict):
    start_date: datetime.datetime
    end_date: datetime.datetime