from datetime import datetime
from constants.CONSTANTS import *
from aia_image_api import imageparam_getter as ipg
import numpy as np
from datetime import timedelta
import pandas as pd
import time
import plotly.express as px


def QualityChecker_single(dt_start, dt_stop, aia_wave, param_id, DatesDF,totalTime_get_aia_imageparam_xml):
    dt = dt_start
    correctImg = 1
    while dt < dt_stop:

        startTime_get_aia_imageparam_xml = time.time()
        xml = ipg.get_aia_imageparam_xml(dt, aia_wave)
        endTime_get_aia_imageparam_xml = time.time()
        totalTime_get_aia_imageparam_xml += endTime_get_aia_imageparam_xml - startTime_get_aia_imageparam_xml
        res = ipg.convert_param_xml_to_ndarray(xml)
        current_entropy_values = res[:, :, (int(param_id) - 1):int(param_id)].reshape(64, 64)

        if dt == dt_start:
            DatesDF.loc[len(DatesDF)] = [dt, 0, 1, aia_wave, param_id]
            last_entropy_values = current_entropy_values
            dt = dt + timedelta(minutes=6)
            continue

        diffmat_from_last = np.absolute(np.subtract(last_entropy_values, current_entropy_values))
        diffsum = np.sum(diffmat_from_last)

        if dt == dt_start + timedelta(minutes=6):
            threshold = diffsum * 1.5
            DatesDF.loc[len(DatesDF)] = [dt, diffsum, 1, aia_wave, param_id]
            last_entropy_values = current_entropy_values
            dt = dt + timedelta(minutes=6)
            continue

        if diffsum > threshold:
            if correctImg == 0:
                correctImg = 1
            else:
                correctImg = 0

        DatesDF.loc[len(DatesDF)] = [dt, diffsum, correctImg, aia_wave, param_id]
        last_entropy_values = current_entropy_values
        dt = dt + timedelta(minutes=6)
    return DatesDF, totalTime_get_aia_imageparam_xml


def QualityChecker(dt_start, dt_stop, aia_wave_array, param_id_array):
    '''
    dt_start: should be string in format YYYY-MM-DDTHH:MM:SS | example: 2012-04-12T16:10:00
    days2check: represents how many days from start date you want to check quality | example: 0.2, 1, 5, 30
    aia_wave_array: array of wave lengths for which we want to check the image correctness
    '''
    dt_start = datetime.strptime(dt_start, '%Y-%m-%dT%H:%M:%S')
    dt_stop = datetime.strptime(dt_stop, '%Y-%m-%dT%H:%M:%S')
    approxImg = divmod((dt_stop - dt_start).seconds, 360)[0]
    itr = len(aia_wave_array) * len(param_id_array)
    startTime_APItime = time.time()
    xml = ipg.get_aia_imageparam_xml(dt_start, aia_wave_array[0])
    endTime_APItime = time.time()
    API_ResponseTimeOneImg = (endTime_APItime-startTime_APItime)/60
    print('Going through approx ', approxImg, ' images ', itr, ' time(s).')
    print('Approx operation time: ', API_ResponseTimeOneImg * approxImg * itr, ' minutes')
    print('Operation will be completed by ',
          (datetime.now() + timedelta(minutes=API_ResponseTimeOneImg * approxImg * itr)).strftime(
              '%Y-%m-%d %H:%M:%S'))

    startTime_fullOperation = time.time()
    DatesDF = pd.DataFrame(columns=['date', 'diff from prev img', 'good', 'aia_wave', 'param_id'])
    totalTime_get_aia_imageparam_xml = 0
    for aia_wave in aia_wave_array:
        for param_id in param_id_array:
            if param_id == '6' or param_id == '10':
                print('Sorry! the project does not work for image param 6 and 10 (KURTOSIS and TAMURA_DIRECTIONALITY)')
                continue
            DatesDF, totalTime_get_aia_imageparam_xml = QualityChecker_single(dt_start, dt_stop, aia_wave,
                                                                              param_id, DatesDF,totalTime_get_aia_imageparam_xml)
    DatesDFplot = DatesDF[['date', 'good','aia_wave']].sort_values(by=['date']).reset_index(drop=True)
    fig = px.line(DatesDFplot, x='date', y='good', color='aia_wave', width=1000, height=400)
    fig.update_layout(title_text='Image Result \n 1 - Image is fine \n 0 - Image is Rotated')
    fig.show()

    improper_images_DatesDF = DatesDF[DatesDF['good'] == 0]
    filename = 'RotatedImages_from' + str(dt_start) + '_to_' + str(dt_stop) + '_wave_' + '_'.join(
        aia_wave_array) + '_param_' + '_'.join(param_id_array) + '.xlsx'
    improper_images_DatesDF[['date', 'aia_wave']].to_excel(filename, header=False, index=False)
    print('Excel downloaded with the name ', filename)

    endTime_fullOperation = time.time()
    Total_fullOperation = endTime_fullOperation - startTime_fullOperation
    print('Full operation time: ' + str(round(Total_fullOperation, 2)))
    print('Time taken by get_aia_imageparam_xml: ' + str(round(totalTime_get_aia_imageparam_xml, 2)) + ' (' +
          str(round(((totalTime_get_aia_imageparam_xml / Total_fullOperation) * 100), 2)) + '%)')
    return DatesDF


def getImagesinTimeRange(dt_start, dt_stop, aia_wave, image_size, param_id):
    dt = dt_start = datetime.strptime(dt_start, '%Y-%m-%dT%H:%M:%S')
    dt_stop = datetime.strptime(dt_stop, '%Y-%m-%dT%H:%M:%S')
    while dt < dt_stop:
        heatmap = ipg.get_aia_imageparam_jpeg(dt, aia_wave, image_size, param_id)
        heatmap.save('SunImages/' + str(dt) + '.png')
        dt = dt + timedelta(minutes=6)


def getImage(dt, aia_wave, image_size, param_id):
    dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S')
    heatmap = ipg.get_aia_imageparam_jpeg(dt, aia_wave, image_size, param_id)
    heatmap.save('SunImages/' + str(dt) + '.png')


def main():
    DatesDF = QualityChecker('2012-04-12T16:10:00', 0.15, [AIA_WAVE.AIA_171], [IMAGE_SIZE.P2000], ['1'])


if __name__ == '__main__':
    main()
