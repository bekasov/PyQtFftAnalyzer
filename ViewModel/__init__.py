from Service.DataService import *


class ViewModel:
    def __init__(self, service: DataService):
        self.service = service

        self.date_from = datetime.datetime(2018, 2, 25, 15, 52, 27)