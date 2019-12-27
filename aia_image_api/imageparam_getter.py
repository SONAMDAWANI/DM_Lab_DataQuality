from PIL import Image
import numpy as np
import requests
from xml.etree import ElementTree as et
from io import BytesIO
from datetime import datetime
from arg_validation import arg_validators
from constants import URL_STRINGS
from constants.CONSTANTS import *

'''
This module is the core of this project, which contains all necessary functions
to get data from our Image Parameter dataset through the web API, http://dmlab.cs.gsu.edu/dmlabapi/.
'''


def get_aia_image_jpeg(starttime: datetime, aia_wave: AIA_WAVE, image_size: IMAGE_SIZE) -> Image:
    """
    queries the AIA image corresponding to the given start time, wave channel, and size.

    :param starttime: start time corresponding to the image.
    :param aia_wave: wavelength channel of the image. Either use the class 'constants.AIA_WAVE'
    to provide a valid wavelength, or pass a string from this list:
    ['94', '131', '171', '193', '211', '304', '335', '1600', '1700']
    :param image_size: size of the image. Either use the class 'constants.IMAGE_SIZE' to provide
    a valide size, or path a string from the list: ['2k', '512', '256']
    :return: the AIA image as a PIL.Image object
    """
    prepared_url = prepare_url_get_aia_image_jpeg(starttime, aia_wave, image_size)
    response = requests.get(prepared_url)
    img = Image.open(BytesIO(response.content))
    return img


def get_aia_imageparam_jpeg(starttime: datetime,
                            aia_wave: (AIA_WAVE, str),
                            image_size: (IMAGE_SIZE, str),
                            param_id: (IMAGE_PARAM, str)) -> Image:
    """
    queries the heatmap of the given image parameter when applied on the AIA image corresponding
    to the given start time, wave channel, and size.

    :param starttime: start time corresponding to the image.
    :param aia_wave: wavelength channel of the image. Either use the class `constants.AIA_WAVE`
    to provide a valid wavelength, or pass in a string from this list:
    ['94', '131', '171', '193', '211', '304', '335', '1600', '1700']
    :param image_size: size of the image. Either use the class `constants.IMAGE_SIZE` to provide
    a valid size, or pass in a string from the list: ['2k', '512', '256']
    :param param_id: id of the image parameters. Either use the class `constants.IMAGE_PARAM` to
    provide a valid id, or pass in a string from the list: ['1', '2', '3', '4', '5', '6', '7', '8',
    '9', '10]. To know which item corresponds to which parameter, see [dmlab.cs.gsu.aedu/dmlabapi/]
    :return: the heatmap of the given image parameter as a PIL.Image object.
    """
    prepared_url = prepare_url_get_aia_imageparam_jpeg(starttime, aia_wave, image_size, param_id)
    response = requests.get(prepared_url)
    img = Image.open(BytesIO(response.content))
    return img


def get_aia_imageparam_xml(starttime: datetime, aia_wave: (AIA_WAVE, str)) -> et:
    """
    queries the XML of 10 image parameters computed on the image corresponding
    to the given date and wavelength channel.

    Note: Use `convert_param_xml_to_ndarray` to convert the retrieved XML into a `numpy.ndarray`
    object.

    :param starttime: datetime corresponding to the requested image.
    :param aia_wave: wavelength channel corresponding to the requested image.
    :return: an `xml.etree.ElementTree.Element` instance, as the content of the
    retrieved XML.
    """
    prepared_url = prepare_url_get_aia_imageparam_xml(starttime, aia_wave)
    response = requests.get(prepared_url)
    xml_content = et.fromstring(response.content)
    return xml_content


def convert_param_xml_to_ndarray(xml_content: et) -> np.ndarray:
    """
    converts the content of a retrieved XML file into a `numpy.ndarray` type. The output dimension
    is 64 X 64 X 10 which is a data cube with 10 matrix for one image, each matrix for one image
    parameter.

    Note: For the order of image parameters and/or an example of a XNM file see:
    http://dmlab.cs.gsu.edu/dmlabapi/ .

    :param xml_content: the content of the retrieved XML file. See the output
                        of `get_aia_imageparam_xml` as an example.
    :return: an '`numpy.ndarray` of dimension (x:64) X (y:64) X (image_params:10)
    """
    mat = np.zeros((64, 64, 10))
    x, y, z = 0, 0, 0
    for cell in xml_content:
        x = np.int(cell[0].text)
        y = np.int(cell[1].text)
        params = cell[2]
        z = 0
        for val in params:
            mat[x][y][z] = np.float(val.text)
            z = z + 1
    return mat


# --------------------------------------------------
#
#          QUERY PREPARATION METHODS
# --------------------------------------------------

def prepare_url_get_aia_image_jpeg(starttime: datetime,
                                   aia_wave: (AIA_WAVE, str),
                                   image_size: (IMAGE_SIZE, str)) -> str:
    """
    prepares the query url to communicate with the web api for getting the AIA image corresponding
    to the given start time, wavelength channel, and size.

    :param starttime: start time corresponding to the image.
    :param aia_wave: wavelength channel of the image. Either use the class `constants.AIA_WAVE`
                     to provide a valid wavelength, or pass in a string from this list: ['94',
                     '131', '171', '193', '211', '304', '335', '1600', '1700']
    :param image_size: size of the image. Either use the class `constants.IMAGE_SIZE` to provide
                       a valid size, or pass in a string from the list: ['2k', '512', '256']
    :return: the prepared query as str.
    """
    time_str = datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S')
    arg_validators.validate_aia_wave(aia_wave)
    arg_validators.validate_image_size(image_size)

    prepared_url = URL_STRINGS.aia_image_jpeg_url.format(image_size, aia_wave, time_str)
    return prepared_url


def prepare_url_get_aia_imageparam_jpeg(starttime: datetime,
                                        aia_wave: (AIA_WAVE, str),
                                        image_size: (IMAGE_SIZE, str),
                                        param_id: (IMAGE_PARAM, str)) -> str:
    """
    prepares the query url to communicate with the web api for getting the heatmap (JPEG)
    of the given image parameter computed on the 4KX4K AIA image corresponding to the given
    start time, wavelength channel.
    
    :param starttime: start time corresponding to the image.
    :param aia_wave: wavelength channel of the image. Either use the class `constants.AIA_WAVE`
           to provide a valid wavelength, or pass in a string from this list: ['94', '131',
           '171', '193', '211', '304', '335', '1600', '1700']
    :param image_size: size of the output image (heatmap). Either use the class
           `constants.IMAGE_SIZE` to provide a valid size, or pass in a string from the list: [
           '2k', '512', '256']
    :param param_id: id of the image parameters. Either use the class
                     `constants.IMAGE_PARAM` to provide a valid id, or pass in a string from the
                     list: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10]. To know which item
                     corresponds to which parameter, see [dmlab.cs.gsu.aedu/dmlabapi/]
    :return: the prepared query as str.
    """
    time_str = datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S')
    arg_validators.validate_aia_wave(aia_wave)
    arg_validators.validate_image_size(image_size)
    arg_validators.validate_image_parameter(param_id)

    prepared_url = URL_STRINGS.aia_imageparam_jpeg_url.format(image_size, aia_wave, time_str,
                                                              param_id)
    return prepared_url


def prepare_url_get_aia_imageparam_xml(starttime: datetime,
                                       aia_wave: (AIA_WAVE, str)) -> str:
    """
    prepares the query url to communicate with the web api for getting the XML of all 10
    image parameters computed on the 4KX4K AIA image corresponding to the given start time,
    wavelength channel.

    :param starttime: start time corresponding to the image.
    :param aia_wave: wavelength channel of the image. Either use the class `constants.AIA_WAVE`
                     to provide a valid wavelength, or pass in a string from this list: ['94',
                     '131', '171', '193', '211', '304', '335', '1600', '1700']
    :return: the prepared query as str.
    """
    time_str = datetime.strftime(starttime, '%Y-%m-%dT%H:%M:%S')
    arg_validators.validate_aia_wave(aia_wave)
    prepared_url = URL_STRINGS.aia_imageparam_xml_url.format(aia_wave, time_str)
    return prepared_url


def main():
    """
    This is only to provide an example of how the methods can be used.

    """
    dt = datetime.strptime('2012-02-13T20:10:00', '%Y-%m-%dT%H:%M:%S')
    aia_wave = AIA_WAVE.AIA_171
    image_size = IMAGE_SIZE.P2000
    param_id = IMAGE_PARAM.ENTROPY

    # img = get_aia_image_jpeg(dt, aia_wave, image_size)
    # img.show()

    # heatmap = get_aia_imageparam_jpeg(dt, aia_wave, image_size, param_id)
    # heatmap.show()

    # xml = get_aia_imageparam_xml(dt, aia_wave)
    # res = convert_param_xml_to_ndarray(xml)
    # print(res.reshape(64 * 64 * 10).tolist())


if __name__ == '__main__':
    main()
