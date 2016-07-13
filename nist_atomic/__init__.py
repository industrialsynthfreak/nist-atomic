"""This package provides console integration with spectral lines data of the
*NIST Atomic Spectra Database*.

:Authors: Violet Red
:Version: 1.0 2016/07/13

See full documentation at *docs/build/html/nist-atomic* folder or build it
yourself with Sphinx.

**Example:**

    To load data from the server:
    ::

        from nist_atomic.loader import Loader
        Loader.load({'H', 'he ii', 'Mn'})

    Data will be stored in a path specified in the .ini file. See `/examples/`
    folder for more examples.


**Info:**

    Atomic light emission and absorption spectra consist of many line series
    related to electron transitions from one state to another. They may be
    calculated directly, but the NIST database provides comprehensive set of
    data about wavelengths, relative intensities and other parameters for each
    element.


**Requirements:**

    Python3 tested only.
    All requirements are listed in *requirements.txt* file.

    - requests: http://docs.python-requests.org/en/latest/index.html
    - lxml: http://lxml.de

    Install them with `pip install -r requirements.txt` command.


**Links:**

    - The database itself: http://physics.nist.gov/PhysRefData/ASD/
    - More info about atomic spectra: http://physics.nist.gov/Pubs/AtSpec/node17.html

"""

import nist_atomic.loader as loader

__version__ = '1.0'
