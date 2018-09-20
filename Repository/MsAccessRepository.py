from Repository.IDataRepository import *


class MsAccessRepository(IDataRepository):
    def __init__(self):
        self._columns = ['К408А', 'К408Б', 'К409А', 'К409Б', 'К427_1А', 'К427_1Б', 'К427_2А', 'К427_2Б', 'К502_1', 'К502_2']

    def GetTransporterLoad(self, transporter: Domain.Transporter, date_from: datetime, date_to: datetime) -> List[int]:
        pass