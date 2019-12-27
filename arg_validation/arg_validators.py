from datetime import datetime
from constants.CONSTANTS import *

"""
The following methods can be used to validate the given arguments to make sure that
valid arguments are being provided. This may be used only if the user is providing
the methods' arguments as 'str' which needs varification, and not using the classes
in 'constants.CONSTANTS'.

This is only to facilitate (and not necessary for) using the API methods. The following
methods, validate all of the needed arguments which are:
    1. Images' date time
    2. Images' wavelength channel
    3. Heatmaps' size 
    4. Parameters' id
    
Author: Azim Ahmadzadeh [aahmadzadeh@cs.gsu.edu], Georgia State University, 2019
"""


def validate_date(date_str: str):
    """
    validates the format of the date. The accepted format is '%Y-%m-%dT%H:%M:%S'.

    :param date_str: datetime as 'str'.
    :return: True if the string matches the acceptable format, and  False otherwise.
    """
    try:
        datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        raise ValueError("Incorrect datetime format! Follow this patter: ['%Y-%m-%dT%H:%M:%S']")


def validate_aia_wave(aia_wave: str):
    """
    Validates the given wavelength channel. It has to be one of the ones in
    'constants.CONSTANTS.AIA_WAVE'.

    :param aia_wave: wavelength channel as 'str'
    :return: True if the string matches the acceptable format, and  False otherwise.
    """
    all_aia_waves = {value: name for name, value in vars(AIA_WAVE).items() if name.isupper()}
    if aia_wave not in all_aia_waves:
        raise ValueError("Invalid aia_wave! Use class AIA_WAVE to provide a valid wave. (Optional)")


def validate_image_size(image_size: str):
    """
    Validates the given image size. It has to be one of the ones in
    'constants.CONSTANTS.IMAGE_SIZE'.

    :param image_size:
    :return: True if the string matches the acceptable format, and  False otherwise.
    """
    all_image_sizes = {value: name for name, value in vars(IMAGE_SIZE).items() if name.isupper()}
    if image_size not in all_image_sizes:
        raise ValueError(
            "Invalid image_size! Use class IMAGE_SIZE to provide a valid size. (Optional)")


def validate_image_parameter(param_id: str):
    """
    Validates the given parameter id. It has to be one of the ones in
    'constants.CONSTANTS.IMAGE_PARAM'.

    :param param_id:
    :return: True if the string matches the acceptable format, and  False otherwise.
    """
    all_param_ids = {value: name for name, value in vars(IMAGE_PARAM).items() if name.isupper()}
    if param_id not in all_param_ids:
        raise ValueError(
            "Invalid param_id! Use class IMAGE_PARAM to provide a valid id. (Optional)")
