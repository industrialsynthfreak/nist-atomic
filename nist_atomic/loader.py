"""This module provides a loader class for working with NIST atomic database
query form. It depends on requests and lxml packages.
"""

import os
import configparser
import logging

import requests

from lxml import html


class Loader:
    """This class handles NIST atomic database form and loads a query results.

    This class doesn't need to be instantiated.

    .. py:attribute:: nist_db_URL

       URL to the database query form.

    .. py:attribute:: log_path

       Path to the loader's log.

    .. py:attribute:: config_path

       Path to a config file. Most of additional the query customization is
       there.

    .. py:attribute:: formats

       List of available storage file formats.

    """

    nist_db_URL = 'http://physics.nist.gov/cgi-bin/ASD/lines1.pl'
    log_path = '../nist-atomic.log'
    config_path = '../nist-atomic.ini'
    _stored_data_path = '../stored/nist-atomic/'
    _config_parser = configparser.ConfigParser()
    _formats = {
        'ascii': {'ext': '.txt', 'splitter': '\t'},
        'csv': {'ext': '.csv', 'splitter': ';'}
    }
    formats = tuple(_formats.keys())

    @classmethod
    def _setup_logger(cls):
        """Private function for a logger setup."""
        path = os.path.join(os.path.dirname(__file__), cls.log_path)
        logging.basicConfig(filename=path, filemode='w')
        l = logging.getLogger()
        l.setLevel(logging.DEBUG)
        return l

    @classmethod
    def _load(cls, settings):
        """This private method sends request and returns response text and
        response status code. The code should be `200`.
        See `W3 status codes <https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html>`_
        for more info.
        """
        response = requests.post(cls.nist_db_URL, data=settings)
        tree = html.fromstring(response.content)
        data = tree.xpath('//pre/text()')[0].splitlines()
        data = [d.replace(" ", "").split("|") for d in data]
        data_header = [
            ''.join([a, b, c]) for a, b, c in zip(data[2], data[3], data[4])]
        data_values = data[6:-1]
        return response.status_code, [data_header] + data_values

    @classmethod
    def _save(cls, filename, data, splitter):
        with open(filename, 'w') as f:
            for d in data:
                f.write(splitter.join(d) + '\n')

    @classmethod
    def load(cls, values, ignore_bad_response=True):
        """This method loads data from url defined in
        :py:attribute:`nist_db_URL` attribute. Data will be stored in a folder
        specified in the config. See :py:attribute:`config_path`.

        :param values: set of element names or a single element name
        examples: 'H', ['H', 'F', 'Mn']

        .. note:: In each name different combinations are allowed:
                    - Ar I
                    - Mg I-IV
                    - All spectra
                    - Fe I; Si IX,XI; Ni Co-like
                    - H-Ar I-II
                    - Mg Li-like; Al Li-like-Be-like
                    - Sc-Fe K-like-Ca-like
                    - 198Hg I

                  However, you may want to use one element per `load()` all
                  because then the element data will be separated file-by-file.

        :type values: list, tuple, set, str
        :param ignore_bad_response: if True, then no exception on connection
        error will be generated, the loader function just write a debug info.
        :type ignore_bad_response: bool

        :return:
        :rtype:

        :raises: ConnectionError if server returns a bad code (not 200)
        :raises: IOError or OSError if files cannot be written.
        """
        logger = cls._setup_logger()
        logger.debug('Started!')
        error_count = 0

        values = set(values)

        path = os.path.join(os.path.dirname(__file__), cls.config_path)
        cls._config_parser.read(path)
        settings = dict(cls._config_parser['LOADER'])

        format_type = cls._config_parser['SAVER'].get('format', 'ascii')
        file_format = cls._formats.get(format_type, cls._formats['ascii'])
        ext, splitter = file_format['ext'], file_format['splitter']
        path = cls._config_parser['SAVER'].get('path', cls._stored_data_path)
        path = os.path.join(os.path.dirname(__file__), path)
        if not os.path.exists(path):
            os.makedirs(path)

        for value in values:
            logger.debug('Sending db query: %s' % value)
            code, data = cls._load(settings)
            if code == 200:
                filename = os.path.join(path, value + ext)
                cls._save(filename, data, splitter)
            else:
                msg = 'Bad connection. Server returned code %d' % code
                if not ignore_bad_response:
                    raise ConnectionError(msg)
                else:
                    error_count += 1
                    logger.debug(msg)
        logger.debug('Loaded %d files with %d errors'
                     % (len(values), error_count))
