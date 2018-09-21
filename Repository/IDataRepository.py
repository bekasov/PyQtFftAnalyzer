import datetime
from typing import List

import Domain


class TransporterData:
    date_time: datetime
    value:  float

    def __init__(self, date_time: datetime, value:  float):
        self.date_time = date_time
        self.value = value



class IDataRepository:
    def get_transporter_load(self, transporter: Domain.Transporter, date_from: datetime, date_to: datetime) \
            -> List[TransporterData]:
        pass
