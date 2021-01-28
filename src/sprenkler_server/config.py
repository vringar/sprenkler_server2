from dataclasses import dataclass, field
from typing import Dict, List, NewType, Literal
import calendar
import datetime  # required for eval DON'T DELETEs
from datetime import time, timedelta
from datetime import datetime as datetime_type
from dataclasses_json import DataClassJsonMixin
from dataclasses_json import config as dcc

weekday = NewType(
    "weekday",
    Literal[
        calendar.MONDAY,
        calendar.TUESDAY,
        calendar.WEDNESDAY,
        calendar.THURSDAY,
        calendar.FRIDAY,
        calendar.SATURDAY,
        calendar.SUNDAY,
    ],
)
ValveStatus = Literal["open", "closed"]


@dataclass
class TimeSlice(DataClassJsonMixin):
    t: time = field(
        metadata=dcc(
            encoder=time.isoformat,
            decoder=time.fromisoformat,
        ),
    )
    td: timedelta = field(
        metadata=dcc(
            encoder=lambda x: repr(x),
            decoder=lambda x: eval(x),
        ),
    )


@dataclass
class ValveConfig(DataClassJsonMixin):
    id: int
    schedule: Dict[weekday, List[TimeSlice]]

    def get_valve_status(self, t: datetime_type) -> ValveStatus:
        wd = calendar.weekday(t.year, t.month, t.day)
        times = self.schedule[wd]
        for start_time, length in times:
            start_datetime = t.replace(hour=start_time.hour, minute=start_time.minute)
            if start_datetime < t < start_datetime + length:
                return "open"

        return "closed"


@dataclass
class ControllerConfig(DataClassJsonMixin):
    valves: List[ValveConfig]
    global_disable: bool = False
