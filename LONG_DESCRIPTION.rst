Verifai SDK for Python
======================

The official Verifai SDK for Python.

Quick introduction
------------------

Verifai is a AI solution that can detect ID documents in images. See
http://www.verifai.com/ for more info.

Companies use it to comply with the GDPR legislation that states you
should not store data about your users and customers that you do not
need for your business. By masking unneeded data you can comply to that.

Features of this SDK
--------------------

- Detect ID documents in JPEG images (in a privacy guaranteed way)
- Give you information about the detected document
- - Position in the image
- - Type of document
- - The zones on the document
- Get a cropped out image from the provided image
- Get crops from all individual zones
- Apply masks to the ID document image

Setup
-----

You can install this package by using the pip tool and installing:

    $ pip install verifai_sdk

Using the Verifai SDK for Python
--------------------------------

Documentation for the Verifai SDK for Python can be found here: https://docs.verifai.com/

Registering for a API token can be done here: https://dashboard.verifai.com/
