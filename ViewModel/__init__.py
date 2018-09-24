from Service.DataService import *
import Domain, typing, datetime


class PlotViewModel:
    service: DataService
    line: Domain.Transporter
    date_from: datetime
    date_to: datetime

    title: str

    fft: FftResult

    def __init__(self, service: DataService, line: Domain.Transporter, date_from: datetime, date_to: datetime):
        self.service = service
        self.line = line
        self.date_from = date_from
        self.date_to = date_to

        self.title = self.line._name_ + " (" + date_from.strftime("%Y-%m-%d %H:%M:%S") + " - " + date_to.strftime("%Y-%m-%d %H:%M:%S") + ")"

        self.fft = FftResult(np.array([]), np.array([]))

    def format_current_point_info(self, frequency: float, y: float):
        period_in_sec = (1 / frequency)
        return 'Период: {:01.1f} Сек ({:01.2f} Мин), f = {:01.6f} Hz, A = {:01.2f}'.format(period_in_sec, period_in_sec / 60, frequency, y)

    def load_data(self):
        self.fft = self.service.get_fft(self.line, self.date_from, self.date_to)


class AppViewModel:
    def __init__(self, service: DataService, dev_mode: bool):
        self.service = service

        self.title = 'Анализ спектров потребления транспортных линий'
        self.curve_combobox_label_text = 'Линия'
        self.add_button_text = 'Добавить график'
        self.add_button_tooltip = 'Добавить график <b>выбранной линии</b> для анализа'
        self.date_time_pickers_format = 'yyyy-MM-dd HH:mm:ss'

        self.current_line = Domain.Transporter.K427_1A

        current_date = datetime.datetime.now()
        self.date_from = current_date.date() + datetime.timedelta(days=-1)
        self.date_to = current_date

        if dev_mode:
            self.date_from = datetime.datetime(2018, 2, 24, 15, 52, 27)
            self.date_to = datetime.datetime(2018, 2, 25, 15, 52, 27)

    def get_line_names(self) -> List[typing.Tuple[str, Domain.Transporter]]:
        return [(key, Domain.Transporter.__members__.get(key)) for key in Domain.Transporter.__members__.keys()]

    def set_current_line(self, value: Domain.Transporter) -> None:
        self.current_line = value

    def set_current_dates_from_to(self, value: datetime, date_to: bool = False):
        if(date_to):
            self.date_to = value
        else:
            self.date_from = value

    def create_plot_view_model(self):
        return PlotViewModel(self.service, self.current_line, self.date_from, self.date_to)
