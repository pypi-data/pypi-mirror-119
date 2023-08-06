Python utils and configuration
==============================

Configuration
-------------

Constants and valiables

.. code-block:: bash

    export CONFIG='/path/to/base_config.yaml;/path/to/config.yaml'


.. code-block:: python

    from ttutils import Config

    CFG = Config()

    CFG.PUBLIC_URL  # get from config files
    CFG.ENV.CONFIG  # get from os env
    CFG.SECRET.KEY  # get from os env and clean


Logging configuration

.. code-block:: bash

    export CONFIG='/path/to/base_log_config.yaml;/path/to/logging.yaml'


.. code-block:: python

    from ttutils import LoggingConfig

    CFG = LoggingConfig({
        'loggers': {
            'aiohttp.access': {  # local overriding
                'level': 'ERROR',
            }
        }
    })


Safe type convertors
--------------------

.. code-block:: python

    from ttutils import try_int, as_bool, to_string, safe_text, text_crop, int_list, int_set

    try_int('123') == 123
    try_int('asd') is None

    as_bool('t') is True
    as_bool(1) is True
    as_bool('false') is False

    to_string(AClass) == '<AClass>'
    to_string('text') == 'text'
    to_string(b'text') == 'text'

    safe_text('<b>text</b>') == '&lt;b&gt;text&lt;/b&gt;'
    safe_text('text') == 'text'

    text_crop('text', 5) == 'text'
    text_crop('sometext', 5) == 'som …'

    int_list(['1', '2', 'a', 'b', None]) == [1, 2]
    int_set(['1', '2', 'a', 'b', None]) == {1, 2}


Compress
--------

Integer, dict integers, list integers compression/decompression functions

.. code-block:: python

    from ttutils import compress

    compress.encode(11232423)  # 'GSiD'
    compress.decode('GSi')  # 175506

    compress.encode_list([12312, 34535, 12323])  # '30o-8rD-30z'
    compress.decode_list('30o-8rD-30z--30C')  # [12312, 34535, 12323, 12324, 12325, 12326]

    compress.encode_dict({12: [234, 453], 789: [12, 98, 99, 100, 101]})  # 'c-3G-75/cl-c-1y--1B'
    compress.decode_dict('c-3G-75/cl-c-1y--1B')  # {12: [234, 453], 789: [12, 98, 99, 100, 101]}
