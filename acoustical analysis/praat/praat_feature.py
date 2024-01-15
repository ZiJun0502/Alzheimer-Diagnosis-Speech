import math
import statistics
import numpy as np
import parselmouth
from parselmouth.praat import call


def get_intensity_attributes(sound, time_step=0., min_time=0., max_time=0., pitch_floor=75.,
                             interpolation_method='Parabolic', return_values=False,
                             replacement_for_nan=0.):
   
    # Get total duration of the sound
    duration = call(sound, 'Get end time')

    # Create Intensity object
    intensity = call(sound, 'To Intensity', pitch_floor, time_step, 'yes')

    attributes = dict()

    attributes['min_intensity'] = call(intensity, 'Get minimum',
                                       min_time, max_time,
                                       interpolation_method)

    attributes['relative_min_intensity_time'] = call(intensity, 'Get time of minimum',
                                                     min_time, max_time,
                                                     interpolation_method) / duration

    attributes['max_intensity'] = call(intensity, 'Get maximum',
                                       min_time, max_time,
                                       interpolation_method)

    attributes['relative_max_intensity_time'] = call(intensity, 'Get time of maximum',
                                                     min_time, max_time,
                                                     interpolation_method) / duration

    attributes['mean_intensity'] = call(intensity, 'Get mean',
                                        min_time, max_time)

    attributes['stddev_intensity'] = call(intensity, 'Get standard deviation',
                                          min_time, max_time)

    attributes['q1_intensity'] = call(intensity, 'Get quantile',
                                      min_time, max_time,
                                      0.25)

    attributes['median_intensity'] = call(intensity, 'Get quantile',
                                          min_time, max_time,
                                          0.50)

    attributes['q3_intensity'] = call(intensity, 'Get quantile',
                                      min_time, max_time,
                                      0.75)

    intensity_values = None

    if return_values:
        intensity_values = [call(intensity, 'Get value in frame', frame_no)
                            for frame_no in range(len(intensity))]
        # Convert NaN values to floats (default: 0)
        intensity_values = [value if not math.isnan(value) else replacement_for_nan
                            for value in intensity_values]

    return attributes,  intensity_values


def get_pitch_attributes(sound, pitch_type='preferred', time_step=0., min_time=0., max_time=0.,
                         pitch_floor=75., pitch_ceiling=600., unit='Hertz',
                         interpolation_method='Parabolic', return_values=False,
                         replacement_for_nan=0.):
    # Get total duration of the sound
    duration = call(sound, 'Get end time')

    # Create pitch object
    if pitch_type == 'preferred':
        pitch = call(sound, 'To Pitch', time_step, pitch_floor, pitch_ceiling)
    elif pitch_type == 'cc':
        pitch = call(sound, 'To Pitch (cc)', time_step, pitch_floor, pitch_ceiling)
    else:
        raise ValueError('Argument for @pitch_type not recognized!')

    attributes = dict()

    attributes['voiced_fraction'] = call(pitch, 'Count voiced frames') / len(pitch)

    attributes['min_pitch'] = call(pitch, 'Get minimum',
                                   min_time, max_time,
                                   unit,
                                   interpolation_method)

    attributes['relative_min_pitch_time'] = call(pitch, 'Get time of minimum',
                                                 min_time, max_time,
                                                 unit,
                                                 interpolation_method) / duration

    attributes['max_pitch'] = call(pitch, 'Get maximum',
                                   min_time, max_time,
                                   unit,
                                   interpolation_method)

    attributes['relative_max_pitch_time'] = call(pitch, 'Get time of maximum',
                                                 min_time, max_time,
                                                 unit,
                                                 interpolation_method) / duration

    attributes['mean_pitch'] = call(pitch, 'Get mean',
                                    min_time, max_time,
                                    unit)

    attributes['stddev_pitch'] = call(pitch, 'Get standard deviation',
                                      min_time, max_time,
                                      unit)

    attributes['q1_pitch'] = call(pitch, 'Get quantile',
                                  min_time, max_time,
                                  0.25,
                                  unit)

    attributes['median_intensity'] = call(pitch, 'Get quantile',
                                          min_time, max_time,
                                          0.50,
                                          unit)

    attributes['q3_pitch'] = call(pitch, 'Get quantile',
                                  min_time, max_time,
                                  0.75,
                                  unit)

    attributes['mean_absolute_pitch_slope'] = call(pitch, 'Get mean absolute slope', unit)
    attributes['pitch_slope_without_octave_jumps'] = call(pitch, 'Get slope without octave jumps')

    pitch_values = None

    if return_values:
        pitch_values = [call(pitch, 'Get value in frame', frame_no, unit)
                        for frame_no in range(len(pitch))]
        # Convert NaN values to floats (default: 0)
        pitch_values = [value if not math.isnan(value) else replacement_for_nan
                        for value in pitch_values]

    return attributes, pitch_values


def get_harmonics_to_noise_ratio_attributes(sound, harmonics_type='preferred', time_step=0.01,
                                            min_time=0., max_time=0., minimum_pitch=75.,
                                            silence_threshold=0.1, num_periods_per_window=1.0,
                                            interpolation_method='Parabolic', return_values=False,
                                            replacement_for_nan=0.):
    # Get total duration of the sound
    duration = call(sound, 'Get end time')

    # Create a Harmonicity object
    if harmonics_type == 'preferred':
        harmonicity = call(sound, "To Harmonicity (cc)",
                           time_step,
                           minimum_pitch,
                           silence_threshold, num_periods_per_window)
    elif harmonics_type == 'ac':
        harmonicity = call(sound, "To Harmonicity (ac)",
                           time_step,
                           minimum_pitch,
                           silence_threshold, num_periods_per_window)
    else:
        raise ValueError('Argument for @harmonics_type is not recognized!')

    attributes = dict()

    attributes['min_hnr'] = call(harmonicity, 'Get minimum',
                                 min_time, max_time,
                                 interpolation_method)

    attributes['relative_min_hnr_time'] = call(harmonicity, 'Get time of minimum',
                                               min_time, max_time,
                                               interpolation_method) / duration

    attributes['max_hnr'] = call(harmonicity, 'Get maximum',
                                 min_time, max_time,
                                 interpolation_method)

    attributes['relative_max_hnr_time'] = call(harmonicity, 'Get time of maximum',
                                               min_time, max_time,
                                               interpolation_method) / duration

    attributes['mean_hnr'] = call(harmonicity, 'Get mean',
                                  min_time, max_time)

    attributes['stddev_hnr'] = call(harmonicity, 'Get standard deviation',
                                    min_time, max_time)

    harmonicity_values = None

    if return_values:
        harmonicity_values = [call(harmonicity, 'Get value in frame', frame_no)
                              for frame_no in range(len(harmonicity))]
        # Convert NaN values to floats (default: 0)
        harmonicity_values = [value if not math.isnan(value) else replacement_for_nan
                              for value in harmonicity_values]

    return attributes, harmonicity_values


def get_glottal_to_noise_ratio_attributes(sound, horizontal_minimum=0., horizontal_maximum=0.,
                                          vertical_minimum=0., vertical_maximum=0.,
                                          minimum_frequency=500., maximum_frequency=4500.,
                                          bandwidth=1000., step=80.):
    # Create a Matrix object that represents GNE
    matrix = call(sound, "To Harmonicity (gne)",
                  minimum_frequency, maximum_frequency,
                  bandwidth, step)

    attributes = dict()

    attributes['min_gne'] = call(matrix, 'Get minimum')

    attributes['max_gne'] = call(matrix, 'Get maximum')

    attributes['mean_gne'] = call(matrix, 'Get mean...',
                                  horizontal_minimum, horizontal_maximum,
                                  vertical_minimum, vertical_maximum)

    attributes['stddev_gne'] = call(matrix, 'Get standard deviation...',
                                    horizontal_minimum, horizontal_maximum,
                                    vertical_minimum, vertical_maximum)

    attributes['sum_gne'] = call(matrix, 'Get sum')

    return attributes, None


def get_local_jitter(sound, min_time=0., max_time=0., pitch_floor=75., pitch_ceiling=600.,
                     period_floor=0.0001, period_ceiling=0.02, max_period_factor=1.3):
    # Create a PointProcess object
    point_process = call(sound, 'To PointProcess (periodic, cc)',
                         pitch_floor, pitch_ceiling)

    local_jitter = call(point_process, 'Get jitter (local)',
                        min_time, max_time,
                        period_floor, period_ceiling, max_period_factor)

    return local_jitter


def get_local_shimmer(sound, min_time=0., max_time=0., pitch_floor=75., pitch_ceiling=600.,
                      period_floor=0.0001, period_ceiling=0.02, max_period_factor=1.3,
                      max_amplitude_factor=1.6):
    # Create a PointProcess object
    point_process = call(sound, 'To PointProcess (periodic, cc)',
                         pitch_floor, pitch_ceiling)

    local_shimmer = call([sound, point_process], 'Get shimmer (local)',
                         min_time, max_time,
                         period_floor, period_ceiling, max_period_factor, max_amplitude_factor)

    return local_shimmer


def get_spectrum_attributes(sound, band_floor=200., band_ceiling=1000., low_band_floor=0.,
                            low_band_ceiling=500., high_band_floor=500., high_band_ceiling=4000.,
                            power=2., moment=3., return_values=False, replacement_for_nan=0.):
    # Create a Spectrum object
    spectrum = call(sound, 'To Spectrum',
                    'yes')

    attributes = dict()

    attributes['band_energy'] = call(spectrum, 'Get band energy',
                                     band_floor, band_ceiling)
    attributes['band_density'] = call(spectrum, 'Get band density',
                                      band_floor, band_ceiling)
    attributes['band_energy_difference'] = call(spectrum, 'Get band energy difference',
                                                low_band_floor, low_band_ceiling,
                                                high_band_floor, high_band_ceiling)
    attributes['band_density_difference'] = call(spectrum, 'Get band density difference',
                                                 low_band_floor, low_band_ceiling,
                                                 high_band_floor, high_band_ceiling)

    attributes['center_of_gravity_spectrum'] = call(spectrum, 'Get centre of gravity',
                                                    power)
    attributes['stddev_spectrum'] = call(spectrum, 'Get standard deviation',
                                         power)
    attributes['skewness_spectrum'] = call(spectrum, 'Get skewness',
                                           power)
    attributes['kurtosis_spectrum'] = call(spectrum, 'Get kurtosis',
                                           power)

    attributes['central_moment_spectrum'] = call(spectrum, 'Get central moment',
                                                 moment, power)

    spectrum_values = None

    if return_values:
        spectrum_values = [call(spectrum, 'Get real value in bin', bin_no)
                           for bin_no in range(len(spectrum))]
        # Convert NaN values to floats (default: 0)
        spectrum_values = [val if not math.isnan(val) else replacement_for_nan
                           for val in spectrum_values]

    return attributes, spectrum_values


def get_formant_attributes(sound, time_step=0., pitch_floor=75., pitch_ceiling=600.,
                           max_num_formants=5., max_formant=5500.,
                           window_length=0.025, pre_emphasis_from=50.,
                           unit='Hertz', interpolation_method='Linear', replacement_for_nan=0.):
    # Create PointProcess object
    point_process = call(sound, "To PointProcess (periodic, cc)", pitch_floor, pitch_ceiling)

    # Create Formant object
    formant = call(sound, "To Formant (burg)", time_step, max_num_formants, max_formant,
                   window_length, pre_emphasis_from)

    # Get number of points in PointProcess
    num_points = call(point_process, "Get number of points")
    if num_points == 0:
        return dict(), None

    f1_list, f2_list, f3_list, f4_list = [], [], [], []

    # Measure formants only at glottal pulses
    for point in range(1, num_points+1):
        t = call(point_process, "Get time from index", point)
        f1 = call(formant, "Get value at time", 1, t, unit, interpolation_method)
        f2 = call(formant, "Get value at time", 2, t, unit, interpolation_method)
        f3 = call(formant, "Get value at time", 3, t, unit, interpolation_method)
        f4 = call(formant, "Get value at time", 4, t, unit, interpolation_method)
        f1_list.append(f1 if not math.isnan(f1) else replacement_for_nan)
        f2_list.append(f2 if not math.isnan(f2) else replacement_for_nan)
        f3_list.append(f3 if not math.isnan(f3) else replacement_for_nan)
        f4_list.append(f4 if not math.isnan(f4) else replacement_for_nan)

    attributes = dict()

    # Calculate mean formants across pulses
    attributes['f1_mean'] = statistics.mean(f1_list)
    attributes['f2_mean'] = statistics.mean(f2_list)
    attributes['f3_mean'] = statistics.mean(f3_list)
    attributes['f4_mean'] = statistics.mean(f4_list)

    # Calculate median formants across pulses
    attributes['f1_median'] = statistics.median(f1_list)
    attributes['f2_median'] = statistics.median(f2_list)
    attributes['f3_median'] = statistics.median(f3_list)
    attributes['f4_median'] = statistics.median(f4_list)

    # Formant Dispersion (Fitch, W. T. (1997). Vocal tract length and formant frequency
    # dispersion correlate with body size in rhesus macaques. The Journal of the Acoustical
    # Society of America, 102(2), 1213-1222.)
    attributes['formant_dispersion'] = (attributes['f4_median'] -
                                        attributes['f1_median']) / 3

    # Average Formant (Pisanski, K., & Rendall, D. (2011). The prioritization of voice
    # fundamental frequency or formants in listeners’ assessments of speaker size, masculinity,
    # and attractiveness. The Journal of the Acoustical Society of America, 129(4), 2201-2212.)
    attributes['average_formant'] = (attributes['f1_median'] +
                                     attributes['f2_median'] +
                                     attributes['f3_median'] +
                                     attributes['f4_median']) / 4

    # MFF (Smith, D. R., & Patterson, R. D. (2005). The interaction of glottal-pulse rate and
    # vocal-tract length in judgements of speaker size, sex, and age. The Journal of the
    # Acoustical Society of America, 118(5), 3177-3186.)
    attributes['mff'] = (attributes['f1_median'] *
                         attributes['f2_median'] *
                         attributes['f3_median'] *
                         attributes['f4_median']) ** 0.25

    # Fitch VTL (Fitch, W. T. (1997). Vocal tract length and formant frequency dispersion
    # correlate with body size in rhesus macaques. The Journal of the Acoustical Society of
    # America, 102(2), 1213-1222.)
    attributes['fitch_vtl'] = ((1 * (35000 / (4 * attributes['f1_median']))) +
                               (3 * (35000 / (4 * attributes['f2_median']))) +
                               (5 * (35000 / (4 * attributes['f3_median']))) +
                               (7 * (35000 / (4 * attributes['f4_median'])))) / 4

    # Delta F (Reby, D., & McComb, K.(2003). Anatomical constraints generate honesty: acoustic
    # cues to age and weight in the roars of red deer stags. Animal Behaviour, 65, 519e-530.)
    xy_sum = ((0.5 * attributes['f1_median']) +
              (1.5 * attributes['f2_median']) +
              (2.5 * attributes['f3_median']) +
              (3.5 * attributes['f4_median']))
    x_squared_sum = (0.5 ** 2) + (1.5 ** 2) + (2.5 ** 2) + (3.5 ** 2)
    attributes['delta_f'] = xy_sum / x_squared_sum

    # VTL(Delta F) Reby, D., & McComb, K.(2003).Anatomical constraints generate honesty: acoustic
    # cues to age and weight in the roars of red deer stags. Animal Behaviour, 65, 519e-530.)
    attributes['vtl_delta_f'] = 35000 / (2 * attributes['delta_f'])

    return attributes, None


def get_speaking_rate(sound, text):
    # Get total duration of the sound
    duration = call(sound, 'Get end time')

    # Approximate speaking rate as #words / duration
    return len(text.split()) / duration


def get_lfcc(sound, lpc_method='autocorrelation', prediction_order=16, window_length=0.025,
             time_step=0.005, pre_emphasis_frequency=50., num_coefficients=12):
    if lpc_method not in ['autocorrelation', 'covariance', 'burg', 'maple']:
        raise ValueError('Argument for @method is not recognized!')

    # Create LPC object
    if lpc_method != 'maple':
        lpc = call(sound, 'To LPC (%s)' % lpc_method, prediction_order,
                   window_length, time_step, pre_emphasis_frequency)
    else:
        lpc = call(sound, 'To LPC (%s)' % lpc_method, prediction_order,
                   window_length, time_step, pre_emphasis_frequency, 1e-6, 1e-6)

    # Create LFCC object
    lfcc = call(lpc, 'To LFCC', num_coefficients)
    num_frames = call(lfcc, 'Get number of frames')

    lfcc_matrix = np.zeros((num_frames, num_coefficients))

    for frame_no in range(1, num_frames + 1):
        for coefficient_no in range(1, num_coefficients + 1):
            coefficient_value = call(lfcc, 'Get value in frame', frame_no, coefficient_no)
            lfcc_matrix[frame_no - 1, coefficient_no - 1] = coefficient_value

    return lfcc_matrix


def get_mfcc(sound, num_coefficients=12, window_length=0.015, time_step=0.005,
             first_filter_frequency=100., distance_between_filters=100., maximum_frequency=0.):
    # Create MFCC object
    mfcc = call(sound, 'To MFCC', num_coefficients, window_length, time_step,
                first_filter_frequency, distance_between_filters, maximum_frequency)
    num_frames = call(mfcc, 'Get number of frames')

    mfcc_matrix = np.zeros((num_frames, num_coefficients))

    for frame_no in range(1, num_frames+1):
        for coefficient_no in range(1, num_coefficients+1):
            coefficient_value = call(mfcc, 'Get value in frame', frame_no, coefficient_no)
            mfcc_matrix[frame_no-1, coefficient_no-1] = coefficient_value

    return mfcc_matrix


def get_delta(matrix, step_size=2):
    num_frames, num_coefficients = matrix.shape[0], matrix.shape[1]

    delta = np.zeros((num_frames, num_coefficients))

    for frame_no in range(num_frames):
        numerator, denominator = 0., 0.

        for step_no in range(step_size):
            start_coefficients, end_coefficients = matrix[0, :], matrix[num_frames - 1, :]
            if frame_no - step_no >= 0:
                start_coefficients = matrix[frame_no - step_no, :]
            if frame_no + step_no < num_frames:
                end_coefficients = matrix[frame_no + step_no, :]

            numerator += step_no * (end_coefficients - start_coefficients)
            denominator += step_no ** 2

        denominator *= 2
        delta[frame_no, :] = numerator / denominator

    return delta