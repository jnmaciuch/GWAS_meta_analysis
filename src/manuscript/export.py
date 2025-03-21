from manuscript import inout
import numpy as np
import os
import datetime
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42  # edit-able in illustrator
mpl.rcParams['font.sans-serif'] = "Arial"
mpl.rcParams['font.family'] = 'sans-serif'


def _get_material_path(p='', date=False):
    """
    Returns the path for a material file.

    Parameters:
    - p (str): The extension of the material file.
    - date (bool): Whether to include the current date and time in the file name.

    Returns:
    - str: The path for the material file.
    """

    extension = p

    p = os.path.join(
        inout.get_internal_path(p='materials'),
        extension)

    if date:
        [fo, fn] = os.path.split(p)
        [fb, ext] = os.path.splitext(fn)
        dt = datetime.datetime.today().strftime('%y%m%d_%H%M')
        p = os.path.join(fo, fb + '_' + dt + ext)

    return p


def image(p='', date=False):
    """
    Save the current matplotlib figure as an image file.

    Parameters:
    - p (str): The file path to save the image. If not provided, the image will be saved in the current directory.
    - date (bool): If True, append the current date and time to the file name.

    Returns:
    None
    """

    import matplotlib as mp
    mpl.rcParams['pdf.fonttype'] = 42  # edit-able in illustrator

    p = _get_material_path(p)

    if date:
        [fo, fn] = os.path.split(p)
        [fb, ext] = os.path.splitext(fn)
        dt = datetime.datetime.today().strftime('%y%m%d_%H%M')
        p = os.path.join(fo, fb + '_' + dt + ext)

    inout.ensure_presence_of_directory(p)

    mpl.pyplot.savefig(p, bbox_inches='tight')


def raster_image(p, dpi, date=False):
    """
    Save a raster image using matplotlib.

    Parameters:
    - p (str): The file path to save the image.
    - dpi (int): The resolution of the image in dots per inch.
    - date (bool, optional): Whether to include the date in the file path. Defaults to False.

    Returns:
    None
    """

    import matplotlib as mpl
    mpl.rcParams['pdf.fonttype'] = 42  # edit-able in illustrator

    p = _get_material_path(p, date)
    inout.ensure_presence_of_directory(p)

    mpl.pyplot.savefig(p, dpi=dpi, bbox_inches='tight')


def full_frame(p='', df=None, date=False, index=False):
    """
    Export a DataFrame to a file in various formats.
    Parameters:
    - p (str): The file path to export the DataFrame. Default is an empty string.
    - df (pandas.DataFrame): The DataFrame to be exported. Default is None.
    - date (bool): Whether to append the current date and time to the file name. Default is False.
    - index (bool): Whether to include the DataFrame index in the exported file. Default is False.
    Raises:
    - EnvironmentError: If the file type is not supported.
    Returns:
    - None
    """

    p = _get_material_path(p)

    if p.endswith('.csv.gz'):
        p = p[:-3]
        compress = True
        file_format = 'csv'
    elif p.endswith('.csv'):
        compress = False
        file_format = 'csv'
    elif p.endswith('.xlsx'):
        file_format = 'xlsx'
    elif p.endswith('.parquet'):
        file_format = 'parquet'
    else:
        raise EnvironmentError(
            'No support for preseent file type.')

    if date:
        [fo, fn] = os.path.split(p)
        [fb, ext] = os.path.splitext(fn)
        dt = datetime.datetime.today().strftime('%y%m%d_%H%M')
        p = os.path.join(fo, fb + '_' + dt + ext)

    inout.ensure_presence_of_directory(p)

    if file_format == 'csv':
        if compress:
            p = p + '.gz'
            df.to_csv(p, compression='gzip', index=index)
        else:
            df.to_csv(p, index=index)
    elif file_format == 'xlsx':
        df.to_excel(p, index=index)

    elif file_format == 'parquet':
        if index == False:
            df.index = np.arange(0, len(df.index))
        df.to_parquet(p)
