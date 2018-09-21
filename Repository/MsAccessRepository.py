import pyodbc

from Repository.IDataRepository import *


class MsAccessRepository(IDataRepository):
    def __init__(self, connect_string: str):
        self._connect_string = connect_string
        self._columns = ['К408А', 'К408Б', 'К409А', 'К409Б', 'К427_1А', 'К427_1Б', 'К427_2А', 'К427_2Б', 'К502_1', 'К502_2']

        self._connection = None
        self._cursor = None

    def get_transporter_load(self, transporter: Domain.Transporter, date_from: datetime, date_to: datetime) \
            -> List[TransporterData]:
        self._open()

        sql = "SELECT ДатаИВремя, " + self._columns[transporter.value] \
              +  " FROM Мощность WHERE ДатаИВремя BETWEEN ? AND ? ORDER BY ДатаИВремя ASC;"
        params = (date_from, date_to)
        rows = self._cursor.execute(sql, params).fetchall()
        self._close()

        return [TransporterData(date_time, value) for date_time, value in rows]

    def _open(self) -> None:
        self._connection = pyodbc.connect(self._connect_string)
        self._cursor = self._connection.cursor() # -> pyodbc.Cursor

    def _close(self) -> None:
        self._cursor.close()
        self._connection.close()

    @staticmethod
    def create_connect_string(db_file_full_path: str) -> str:
        driver_name = [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')][0]
        return 'DRIVER={};DBQ={}'.format(driver_name, db_file_full_path)
