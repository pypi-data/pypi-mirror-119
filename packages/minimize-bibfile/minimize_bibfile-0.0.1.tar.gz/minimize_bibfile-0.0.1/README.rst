Minimize Bib file
=====================================
|pip| |downloads|

Python package to identify and remove duplicated or near-duplicated bib entries.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install minimize_bibfile


Usage example
----------------------------------------------
To check if a bib file can be further minimized, just run:

.. code:: python

    from minimize_bibfile import general_bib_check

    general_bib_check("path/to/my/bibfile.bib")

This will help you find the duplicated entries hiding in your bibliographies.


.. |pip| image:: https://badge.fury.io/py/minimize-bibfile.svg
    :target: https://badge.fury.io/py/minimize-bibfile
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/minimize-bibfile
    :target: https://pepy.tech/badge/minimize-bibfile
    :alt: Pypi total project downloads 