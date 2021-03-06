# -*- coding: utf-8 -*-
"""
The following code is part of qudiamond-analysis under the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Copyright (c) 2021 Dinesh Pinto. See the LICENSE file at the
top-level directory of this distribution and at
<https://github.com/dineshpinto/qudiamond-analysis/>
"""
import datetime
import logging
import os
import pickle
import warnings
from typing import Tuple

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas
import pandas as pd
from dateutil import parser

# Start module level logger
logging.basicConfig(format='%(name)s :: %(levelname)s :: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


#
# Functions for resolving data paths.
#


def get_folderpath(folder_name: str) -> str:
    """
    Create absolute folder paths.

    Args:
        folder_name: string
            Folder from the "Data" directory on computer

    Returns: string
        Full filepath of the directory depending on the PC name

    """
    if os.environ['COMPUTERNAME'] == 'NBKK055':
        return os.path.join("C:/", "Nextcloud", "Data", folder_name)
    else:
        return os.path.join("Z:/", "Data", folder_name)


def get_qudiamond_folderpath(folder_name: str) -> str:
    """
    Create absolute folder paths.

    Args:
        folder_name: string
            Folder from the "Data" directory on computer

    Returns: string
        Full filepath of the directory depending on the PC name

    """
    folder_name += "\\"
    if os.environ['COMPUTERNAME'] == 'NBKK055':
        return os.path.join("\\\\kernix", "qudiamond", "Data", folder_name)
    else:
        return os.path.join("Z:/", "Data", folder_name)


def get_figure_folderpath(folder_name: str) -> str:
    if os.environ['COMPUTERNAME'] == 'NBKK055':
        return os.path.join("C:/", "Nextcloud", "Data_Analysis", folder_name)
    else:
        return os.path.join("Z:/", "Data_Analysis", folder_name)


def get_qudi_data_path(folder_name: str) -> str:
    folder_name += "\\"
    if os.environ['COMPUTERNAME'] == 'NBKK055':
        path = os.path.join("\\\\kernix", "qudiamond", "Data", folder_name)
        if os.path.exists(path):
            return path
        else:
            raise IOError("Connect to kernix")
    else:
        return os.path.join("Z:/", "Data", folder_name)


#
# Functions for reading and writing into .pys, .pkl & .csv files.
#


def load_pys(filename: str, folder: str = "") -> np.ndarray:
    """ Loads raw pys data files. Wraps around numpy.load. """
    # TODO: replace paths with os.join()
    path = "../raw_data/" + folder
    if filename.endswith('.pys'):
        return np.load(path + filename, encoding="bytes", allow_pickle=True)
    else:
        return np.load(path + filename + ".pys", encoding="bytes", allow_pickle=True)


def save_pys(dictionary: dict, filename: str, folder: str = ""):
    """ Saves processed pickle files for plotting/further analysis. """
    # TODO: replace paths with os.join()
    path = "../data/" + folder
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + filename + '.pys', 'wb') as f:
        pickle.dump(dictionary, f, 1)


def save_df(df: pandas.DataFrame, filename: str, folder: str = ""):
    """ Save Dataframe as csv. """
    # TODO: replace paths with os.join()
    path = "../data/" + folder
    if not os.path.exists(path):
        os.makedirs(path)
    df.to_csv(path + filename + ".csv", sep='\t', encoding='utf-8')


def load_pkl(filename: str, folder: str = ""):
    """ Loads processed pickle files for plotting/further analysis. """
    # TODO: replace paths with os.join()
    path = "../data/" + folder
    with open(path + filename + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_pkl(obj: object, filename: str, folder: str = ""):
    """ Saves processed pickle files for plotting/further analysis. """
    # TODO: replace paths with os.join()
    path = "../data/" + folder
    if not os.path.exists(path):
        os.makedirs(path)

    with open(path + filename + '.pkl', 'wb') as f:
        pickle.dump(obj, f)


#
# Functions for reading and writing figures.
#


def save_figures(filename: str, folder: str = "", overwrite: bool = True):
    """ Saves figures from matplotlib plot data. """
    path = get_figure_folderpath(folder)
    if not os.path.exists(path):
        os.makedirs(path)

    logger.info(f"Saving '{filename}' to '{path}'")

    exts = [".pdf", ".svg", ".png"]

    if filename.endswith(".pys"):
        filename, _ = os.path.splitext(filename)

    if not overwrite:
        for ext in exts:
            figure_path = os.path.join(path, filename + ext)
            if os.path.isfile(figure_path):
                raise IOError(f"{figure_path} already exists")

    for ext in exts:
        if ext == ".png":
            dpi = 600
        else:
            dpi = 1000
        figure_path = os.path.join(path, filename + ext)
        plt.savefig(figure_path, dpi=dpi, bbox_inches="tight",
                    metadata={"Title": "{}".format(filename)})


def savefig(filename: str = None, folder: str = None, **kwargs):
    """
    General function to save figures. Wraps around matplotlib.pyplot.savefig().

    Args:
        filename: string
            name of file to save on disk
                without extension saves ".jpg"  and ".svg"
                with extension only saves specific extension
        folder: string
            name of folder location to save on disk. Creates sub-directory "figures/" if it does not exist.
        **kwargs: matplotlib.plot(**kwargs)
    """
    warnings.warn("savefig() is deprecated; use save_figures().", DeprecationWarning)

    if folder is None:
        folder = "../figures/"
    else:
        folder += r"figures\\"
        if not os.path.exists(folder):
            os.makedirs(folder)

    if filename is None:
        filename = "image"

    # Extract just the filename without extension
    fname, ext = os.path.splitext(filename)

    if not ext:
        # If no extension given, use some sane defaults
        extensions = [".jpg", ".svg"]
    else:
        extensions = [ext]

    for extension in extensions:
        try:
            if not kwargs:
                # Sane defaults for saving
                plt.savefig(folder + fname + extension, dpi=600, bbox_inches="tight")
            else:
                plt.savefig(folder + fname + extension, **kwargs)
        except AttributeError:
            # Happens when using JupyterLab with ipympl, can be safely ignored
            pass


#
# Functions for reading Nanonis data files
#


def extract_data_from_dat(filename: str, folder: str = "") -> pandas.DataFrame:
    """ Extract data from a Nanonis dat file. """
    if not filename.endswith(".dat"):
        filename += ".dat"

    skiprows = 0
    with open(folder + filename) as dat_file:
        for num, line in enumerate(dat_file, 1):
            if "[DATA]" in line:
                # Find number of rows to skip when extracting data
                skiprows = num
                break
            if "#=====" in line:
                skiprows = num
                break

    df = pd.read_table(folder + filename, sep="\t", skiprows=skiprows)
    return df


def extract_parameters_from_dat(filename: str, folder: str = "") -> dict:
    """ Extract parameters from a Nanonis dat file. """
    if not filename.endswith(".dat"):
        filename += ".dat"

    d = {}
    with open(folder + filename) as dat_file:
        for line in dat_file:
            if line == "\n":
                # Break when reaching empty line
                break
            elif "User" in line or line.split("\t")[0] == "":
                # Cleanup excess parameters and skip empty lines
                pass
            else:
                label, value, _ = line.split("\t")
                try:
                    # Convert strings to numbers where possible
                    value = float(value)
                except ValueError:
                    pass
                if "Oscillation Control>" in label:
                    label = label.replace("Oscillation Control>", "")
                d[label] = value
    return d


def read_dat(filename: str, folder: str = "") -> Tuple[dict, pandas.DataFrame]:
    """
    Convenience function to extract both parameters and data from a DAT file.

    Args:
        filename: string
            Name of DAT filename stored on disk
        folder:
            Folderpath on disk on disk


    Returns:
        parameters : dict
            header parameters extracted from DAT file
        data : dict
            data columns extracted from DAT file
    """
    parameters = extract_parameters_from_dat(filename, folder=folder)
    data = extract_data_from_dat(filename, folder=folder)
    return parameters, data


#
# Functions for reading Pfeiffer pressure monitor data
#


def channel_to_gauge_names(channel_names: list) -> list:
    """ Replace the channel names with gauge locations. """
    gauges = {"CH 1": "Main", "CH 2": "Prep", "CH 3": "Backing"}
    return [gauges.get(ch, ch) for ch in channel_names]


def convert_tpg_to_mpl_time(df: pandas.DataFrame) -> np.ndarray:
    """ Read DataFrame extracted using read_tpg_data and add in matplotlib datetimes using "Date" and "Time" cols. """
    datetimes = df["Date"] + " " + df["Time"]
    # Convert raw dates and times to datetime Series, then to an matplotlib Series
    dt_series_datetime = [datetime.datetime.strptime(str(dt), '%d-%b-%y %H:%M:%S.%f') for dt in datetimes]
    # noinspection PyUnresolvedReferences
    dt_series_mpl = matplotlib.dates.date2num(dt_series_datetime)
    return dt_series_mpl


def read_tpg_data(filename: str, folder: str = None) -> pandas.DataFrame:
    """
     Read data stored by Pfeiffer vacuum monitoring software.

    Args:
        filename: string
            name of ".txt" file on disk
        folder: string
            location of file on disk

    Returns:
        df : pandas.DataFrame
            DataFrame with all .txt columns and converted matplotlib timestamps

    """
    if not filename.endswith(".txt"):
        filename += ".txt"

    # Extract only the header to check which gauges are connected
    file_header = pd.read_csv(folder + filename, sep="\t", skiprows=1, nrows=1)
    header = channel_to_gauge_names(file_header)

    # Create DataFrame with new header
    df = pd.read_csv(folder + filename, sep="\t", skiprows=5, names=header)

    # Save matplotlib datetimes for plotting
    df["MPL_datetimes"] = convert_tpg_to_mpl_time(df)
    return df


#
# Functions for reading LakeShore temperature monitor data
#


def read_tm224_data(filename: str, folder: str = None) -> pandas.DataFrame:
    """
     Read data stored by Lakeshore TM224 temperature monitor software.

    Args:
        filename: string
            name of ".xls" file on disk
        folder: string
            location of file on disk

    Returns:
        df : pandas.DataFrame
            DataFrame with all .xls columns and converted matplotlib timestamps
    """
    if not filename.endswith(".xls"):
        filename += ".xls"

    # Extract only the timestamp
    timestamp = pd.read_excel(folder + filename, skiprows=1, nrows=1, usecols=[1], header=None)[1][0]
    # Parse datetime object from timestamp
    timestamp_dt = parser.parse(timestamp, tzinfos={"CET": 0 * 3600})

    # Create DataFrame
    df = pd.read_excel(folder + filename, skiprows=3)

    # Add matplotlib datetimes to DataFrame
    time_array = []
    for milliseconds in df["Time"]:
        time_array.append(timestamp_dt + datetime.timedelta(milliseconds=milliseconds))
    # noinspection PyUnresolvedReferences
    df["MPL_datetimes"] = matplotlib.dates.date2num(time_array)

    return df


#
# Functions for reading OceanOptics spectrometer data
#


def read_spectrometer_data(filename: str, folder: str = "") -> pandas.DataFrame:
    """
    Read spectrometer data from OceanOptics spectrometer.

    Args:
        filename: string
            name of ".txt" file on disk
        folder: string
            location of file on disk

    Returns:
        df : pandas.DataFrame
            DataFrame with all .xls columns and converted matplotlib timestamps
    """

    if not filename.endswith(".txt"):
        filename += ".txt"

    df = pd.read_csv(folder + filename, sep="\t", skiprows=14, names=["wavelength", "intensity"])

    return df


#
# Functions for reading qudi-hira data
#


def read_qudi_parameters(filename: str, folder: str = "") -> dict:
    """ Extract parameters from a qudi dat file. """
    if not filename.endswith(".dat"):
        filename += ".dat"

    params = {}
    with open(folder + filename) as dat_file:
        for line in dat_file:
            if line == '#=====\n':
                break
            else:
                # Remove # from beginning of lines
                line = line[1:]
                if ":" in line:
                    label, value = line.split(":")
                    if value != "\n":
                        params[label] = float(value)

    return params


#
# Miscellaneous functions
#

def get_filenames_matching(text_to_match: str, folder: str) -> list:
    """
    Return all filenames in a folder matching a text string.
    This is generally to be used with pd.concat in a loop, doing this is very expensive and slow.

    Args:
        text_to_match: text string to match filenames with
        folder: folder to search in

    Returns:
        object: list
            List of filenames matching text string provided
    """
    files_found = []
    for file in os.listdir(folder):
        if text_to_match in file:
            files_found.append(file)
    print(files_found)
    return files_found
