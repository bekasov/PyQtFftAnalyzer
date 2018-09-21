from Repository.IDataRepository import *
import numpy as np


class FftResult:
    frequencies: np.ndarray
    magnitudes: np.ndarray
    def __init__(self, frequencies: np.ndarray, magnitudes: np.ndarray):
        self.frequencies = frequencies
        self.magnitudes = magnitudes


class DataService:
    def __init__(self, repo: IDataRepository):
        self.repo = repo

    def get_fft(self, transporter: Domain.Transporter, date_from: datetime, date_to: datetime) -> FftResult:
        line_data = self.repo.get_transporter_load(transporter, date_from, date_to)
        if (len(line_data) < 2):
            return FftResult(np.array([]), np.array([]))

        measure_interval_in_sec = int((line_data[1].date_time - line_data[0].date_time).total_seconds())

        data_to_fft = np.array([td.value for td in line_data])
        number_of_measures = data_to_fft.size

        fftFreqs = np.fft.fftfreq(number_of_measures, d = measure_interval_in_sec)[1: number_of_measures // 2]
        fftMagnitudes = np.abs(np.fft.fft(data_to_fft) * 2 / number_of_measures)[1 : number_of_measures // 2]

        return FftResult(fftFreqs, fftMagnitudes)
