from Repository.IDataRepository import *


class DataService:
    def __init__(self, repo: IDataRepository):
        self.repo = repo

    def GetTransporterLoad(self, transporter: Domain.Transporter, date_from: datetime, date_to: datetime) -> List[int]:
        pass