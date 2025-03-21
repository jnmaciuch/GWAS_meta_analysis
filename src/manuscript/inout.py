import os
import pandas as pd

from pathlib import Path


def get_internal_path(p=None):
    """
    Returns the internal path based on the specified extension.
    Args:
        p (str, optional): The extension to be appended to the internal path. Defaults to None.
    Returns:
        str: The internal path with the specified extension.
    Raises:
        ValueError: If the base folder specified in the settings file does not exist.
    """

    extension = p

    if extension is not None:
        extension = _adjust_to_current_file_separator(extension)

    settings = _settings_from_file()

    base_folder = settings['internal_path']

    if not os.path.exists(base_folder):
        raise ValueError(
            'Could not find input folder {}. Please ensure that specified.'.format(
                base_folder))

    if extension is not None:
        extension = str.replace(extension, '\\', os.path.sep)
        extension = str.replace(extension, '/', os.path.sep)

        outpath = os.path.join(base_folder, extension)
    else:
        outpath = os.path.join(base_folder)

    return outpath


def ensure_presence_of_directory(directory_path=None):
    """
    Ensure the presence of a directory at the specified path.
    Args:
        directory_path (str): The path of the directory to ensure the presence of.
    Raises:
        ValueError: If no input is specified for `directory_path`.
    """

    if directory_path is None:
        raise ValueError('No input specfied for ensure_presence_of_directory')

    directory_path_n, ext = os.path.split(directory_path)

    if '.' in ext:
        directory_path = directory_path_n

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def _settings_from_file():
    """
    Reads the settings from a CSV file and returns them as a dictionary.
    Returns:
        dict: A dictionary containing the settings read from the CSV file.
    Raises:
        EnvironmentError: If the directory reserved for settings or the CSV file is not found.
        EnvironmentError: If the CSV file does not have the expected format.
        EnvironmentError: If there are duplicated keys in the CSV file.
    """

    home = str(Path.home())

    path_to_settings = os.path.join(
        str(Path.home()), 'Documents', 'data_paths')

    if not os.path.exists(path_to_settings):
        raise EnvironmentError(rf"""
            Could not find directory reserved for settings:
            {path_to_settings}
        """)

    path_to_settings = os.path.join(
        path_to_settings,
        'allele_frequency.csv'
    )

    if not os.path.exists(path_to_settings):
        raise EnvironmentError(rf"""
            Could not find sfpq.csv file:
            {path_to_settings}
            This file needs to be UTF-8 formatted
            csv file with two columns: key, value
            Also see readme of repository for
            further guidance.
        """)

    settings = pd.read_csv(
        path_to_settings
    )

    if not all(settings.columns[:2] == ['key', 'value']):
        raise EnvironmentError(rf"""
            allele_frequency.csv must start with the two
            columns: key and value.
            
            {path_to_settings}
        """)

    settings = settings.drop_duplicates()

    if any(settings['key'].duplicated()):
        raise EnvironmentError(rf"""
            At least one key within allele_frequency.csv is
            duplicated and therefore ambiguous
            
            {path_to_settings}
        """)

    settings = settings.set_index(
        'key',
        verify_integrity=True
    )['value'].to_dict()

    return settings


def _adjust_to_current_file_separator(x):
    '''
    Replaces backslashes and forward slashes
    by file separtor used on current operating
    system.
    '''
    x = x.replace('\\', os.path.sep)
    x = x.replace('/', os.path.sep)

    return x
