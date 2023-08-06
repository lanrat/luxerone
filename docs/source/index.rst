.. Unofficial Luxer One Python Client documentation master file, created by
   sphinx-quickstart on Fri Aug  4 17:30:46 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Unofficial Luxer One Python Client's documentation!
==============================================================

Welcome to the documentation for the unofficial Luxer One Residential Python client. This library is
intended for developers who wish to integrate with the `Luxer One <https://www.luxerone.com/>`_ package receiving
service to retrieve information about deliveries. Please note that this is an **UNOFFICIAL** client and makes use of
some reverse engineering to interact with the Luxer One service.


This project was originally forked from Lanrat's `luxerone <https://github.com/lanrat/luxerone>`_ project and
adds several quality of life improvements, the principal user facing improvement being that you no longer
need to parse through a dictionary to interact with the data. Data wrapper classes have been added to make
it easier and faster to find what information you are looking for. Further improvements include
no longer needing to keep track of your auth token as the new LuxerOneClient class handles the token
behind the scenes. You do still have the ability to manually manipulate the token if needed (such as the case
where you have a long-lived token that you want to reuse across multiple sessions), but for most applications
this will not be the case. The remaining changes are not user-facing and pertain to code maintainability
and packaging for use as a library.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
