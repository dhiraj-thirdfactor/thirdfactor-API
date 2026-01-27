API Endpoints
=============

This guide details the available endpoints in the ThirdFactor AI API Gateway v0.1.0.

1. Health Check
---------------

Verifies that the API service is up and running.

*   **Method:** ``GET``
*   **Endpoint:** ``/health``

**Headers**

+-------------+--------------------+
| Key         | Value              |
+=============+====================+
| ``Accept``  | ``application/json``|
+-------------+--------------------+

**Example Request**

.. code-block:: http

    GET /health HTTP/1.1
    Host: <base_url>
    Authorization: Bearer <token>
    Accept: application/json


2. Detect Face
--------------

Detects faces in a given base64-encoded image.

*   **Method:** ``POST``
*   **Endpoint:** ``/detect-face/``

**Headers**

+----------------+-------------------------------------+
| Key            | Value                               |
+================+=====================================+
| ``Content-Type``| ``application/x-www-form-urlencoded``|
+----------------+-------------------------------------+

**Body Parameters (x-www-form-urlencoded)**

+------------------+------+------------+-----------------------------------------------------------+
| Key              | Type | Default    | Description                                               |
+==================+======+============+===========================================================+
| ``base64_image`` | Text | *Required* | The base64 encoded string of the image containing the face.|
| ``features``     | Text | ``ALL``    | Specify features to extract.                              |
+------------------+------+------------+-----------------------------------------------------------+

**Example Request**

.. code-block:: bash

    curl --location '<base_url>/detect-face/' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --header 'Authorization: Bearer <token>' \
    --data-urlencode 'base64_image=<BASE64_STRING>' \
    --data-urlencode 'features=ALL'


3. Compare Face
---------------

Compares two face images to check for a match.

*   **Method:** ``POST``
*   **Endpoint:** ``/compare-face/``

**Query Parameters**

+---------------------+----------+---------------------------------------+
| Key                 | Value    | Description                           |
+=====================+==========+=======================================+
| ``threshold``       | ``52``   | Similarity threshold for matching.    |
| ``live_check``      | ``false``| Enable liveness checking (true/false).|
| ``occlusion_check`` | ``false``| Enable occlusion checking (true/false).|
+---------------------+----------+---------------------------------------+

**Headers**

+----------------+--------------------+
| Key            | Value              |
+================+====================+
| ``Content-Type``| ``application/json``|
+----------------+--------------------+

**Body (raw JSON)**

Array containing two base64 strings.

.. code-block:: json

    [
      "BASE64_IMAGE_STRING_1",
      "BASE64_IMAGE_STRING_2"
    ]

**Example Request**

.. code-block:: bash

    curl --location '<base_url>/compare-face/?threshold=52&live_check=false&occlusion_check=false' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <token>' \
    --data '[
        "BASE64_IMAGE_1",
        "BASE64_IMAGE_2"
    ]'


4. Document Crop (Get Document Type)
------------------------------------

Analyzes a document image and determines cropping or document type details.

*   **Method:** ``POST``
*   **Endpoint:** ``/type-of-document-crop/``

**Headers**

+----------------+--------------------+
| Key            | Value              |
+================+====================+
| ``Content-Type``| ``application/json``|
+----------------+--------------------+

**Body Parameters (x-www-form-urlencoded)**

*Note: The Postman collection indicates urlencoded body mode, though Content-Type header suggests JSON. Please verify the backend expectation.*

+------------------+------+---------------------------------------------+
| Key              | Type | Description                                 |
+==================+======+=============================================+
| ``base64_image`` | Text | Base64 encoded string of the document image.|
+------------------+------+---------------------------------------------+

**Example Request**

.. code-block:: bash

    curl --location '<base_url>/type-of-document-crop/' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <token>' \
    --data-urlencode 'base64_image=<BASE64_STRING>'


5. OCR Document
---------------

Extracts text information from a document image.

*   **Method:** ``POST``
*   **Endpoint:** ``/document-extract-information/``

**Headers**

+----------------+-------------------------------------+
| Key            | Value                               |
+================+=====================================+
| ``Content-Type``| ``application/x-www-form-urlencoded``|
+----------------+-------------------------------------+

**Body Parameters (x-www-form-urlencoded)**

+------------------+------+---------------------------------------+
| Key              | Type | Description                           |
+==================+======+=======================================+
| ``base64_image`` | Text | Base64 encoded string of the document.|
+------------------+------+---------------------------------------+

**Example Request**

.. code-block:: bash

    curl --location '<base_url>/document-extract-information/' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --header 'Authorization: Bearer <token>' \
    --data-urlencode 'base64_image=<BASE64_STRING>'


6. Image to Base64
------------------

Utility endpoint to convert an uploaded image file to a base64 string.

*   **Method:** ``POST``
*   **Endpoint:** ``https://ep-sa1.thirdfactor.ai/image-to-base64/``
*   **Note:** This endpoint has a specific host different from the base URL.

**Body Parameters (form-data)**

+---------+------+--------------+---------------------------+
| Key     | Type | Content-Type | Description               |
+=========+======+==============+===========================+
| ``image``| File | ``image/jpeg``| The image file to convert.|
+---------+------+--------------+---------------------------+

**Example Request**

.. code-block:: bash

    curl --location 'https://ep-sa1.thirdfactor.ai/image-to-base64/' \
    --header 'Authorization: Bearer <token>' \
    --form 'image=@"/path/to/file.jpg"'
