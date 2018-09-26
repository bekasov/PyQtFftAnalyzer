from Repository.IDataRepository import *
import numpy as np
from typing import List, Any


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
        if len(line_data) < 2:
            return FftResult(np.array([]), np.array([]))

        measure_interval_in_sec = int((line_data[1].date_time - line_data[0].date_time).total_seconds())

        data_to_fft = np.array([td.value for td in line_data])

        # return FftResult(frequencies = np.array([1 / measure_interval_in_sec]), magnitudes = data_to_fft)

        number_of_measures = data_to_fft.size

        fftFreqs = np.fft.fftfreq(number_of_measures, d = measure_interval_in_sec)[1: number_of_measures // 2]
        fftMagnitudes = np.abs(np.fft.fft(data_to_fft) * 2 / number_of_measures)[1 : number_of_measures // 2]

        return FftResult(fftFreqs, fftMagnitudes)

    def find_maximums(self, data, min_delta_range_percent: float =0.1):
        real_min_delta = 0
        if min_delta_range_percent != 0:
            data_range = np.max(data) - np.min(data)
            real_min_delta = data_range * min_delta_range_percent

        sign = 0
        zero_sign_count = 0

        result_values: List[Any] = []
        result_indices: List[Any] = []

        def detector(i, _):
            nonlocal sign, zero_sign_count, data, result_values, result_indices, real_min_delta
            if i == 0:
                return

            if data[i] == data[i - 1]:
                zero_sign_count += 1
            else:
                if data[i] - data[i - 1] < real_min_delta:
                    max_ind = -1

                    if sign == 1:
                        max_ind = (i - (zero_sign_count // 2)) if zero_sign_count > 2 else (i - 1)

                    if i == 1:
                        max_ind = i - 1;

                    if max_ind > -1:
                        result_values.append(data[max_ind])
                        result_indices.append(max_ind)
                    sign = -1

                else:
                    sign = 1

                zero_sign_count = 0

        [detector(i, v) for i, v in enumerate(data)]
        return result_values, result_indices

    def find_maximums_rec(self, data, rec_num=2, min_delta_range_percent=0, previous_inds=[]):
        max_magnitudes, max_magnitudes_ind = self.find_maximums(data, min_delta_range_percent)

        if len(previous_inds) > 0:
            max_magnitudes_ind = [previous_inds[i] for i in max_magnitudes_ind]

        rec_num = rec_num - 1

        if rec_num == 0:
            return max_magnitudes, max_magnitudes_ind

        return self.find_maximums_rec(max_magnitudes, rec_num, min_delta_range_percent, max_magnitudes_ind)

