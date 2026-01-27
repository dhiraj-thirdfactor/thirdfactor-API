API Endpoints
=============

This guide details the available endpoints in the ThirdFactor AI API Gateway v0.1.0.

1. Health Check
---------------

Verifies that the API service is up and running.

*   **Method:** ``GET``
*   **Endpoint:** ``/health``
*   **Auth:** Not required

**Headers**

+-------------+--------------------+
| Key         | Value              |
+=============+====================+
| ``Accept``  | ``application/json``|
+-------------+--------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "status": "healthy",
      "service": "thirdfactor-ai-gateway"
    }

2. Detect Face
--------------

Detects faces in a given base64-encoded image and extracts optional attributes.

*   **Method:** ``POST``
*   **Endpoint:** ``/detect-face/``
*   **Content-Type:** ``application/x-www-form-urlencoded``

**Body Parameters**

+------------------+------+------------+-------------------------------------------------------------+
| Key              | Type | Default    | Description                                                 |
+==================+======+============+=============================================================+
| ``base64_image`` | Text | *Required* | The base64 encoded string of the image containing the face. |
| ``features``     | Text | ``ALL``    | Comma-separated list: ALL, AGE_RANGE, EYEGLASSES, GENDER,   |
|                  |      |            | FACE_OCCLUDED, SUNGLASSES.                                  |
+------------------+------+------------+-------------------------------------------------------------+

**Response (200 OK - Example)**

.. code-block:: json

    {
      "result": true,
      "total_faces": 1,
      "faces": [
        {
          "confidence": 0.84,
          "age_range": { "min_age": 27, "max_age": 32, "detected_age": 29 },
          "gender": "Male",
          "occluded": false
        }
      ]
    }

**Response (No Faces Found)**

.. code-block:: json

    { "result": false, "total_faces": 0, "faces": [] }

3. Compare Face
---------------

Compares two face images to verify if they belong to the same person.

*   **Method:** ``POST``
*   **Endpoint:** ``/compare-face/``
*   **Content-Type:** ``application/json``

**Query Parameters**

+---------------------+----------+---------------------------------------+
| Key                 | Value    | Description                           |
+=====================+==========+=======================================+
| ``threshold``       | ``52.0`` | Similarity threshold for matching.    |
| ``live_check``      | ``false``| Enable liveness checking (true/false).|
| ``occlusion_check`` | ``false``| Enable occlusion checking (true/false).|
+---------------------+----------+---------------------------------------+

**Body (JSON Array)**

.. code-block:: json

    [
      "<BASE64_IMAGE_1>",
      "<BASE64_IMAGE_2>"
    ]

**Response (200 OK - Match)**

.. code-block:: json

    {
      "verified": true,
      "confidence": 98.5,
      "percentage_match": 99.9
    }

**Response (No Match)**

.. code-block:: json

    {
      "verified": false,
      "percentage_match": 0
    }

4. Detect & Crop Document Type
------------------------------

Automatically detects the type of document (e.g., national-id, passport, driving-license) and returns a cropped image.

*   **Method:** ``POST``
*   **Endpoint:** ``/type-of-document-crop/``
*   **Content-Type:** ``application/json``

**Body Parameters**

+------------------+------+---------------------------------------------+
| Key              | Type | Description                                 |
+==================+======+=============================================+
| ``base64_image`` | Text | Base64 encoded string of the document image.|
+------------------+------+---------------------------------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "document_type": "national-id-front",
      "score": 0.98,
      "cropped_image": "data:image/jpeg;base64,/9j/..."
    }

5. Analyze Document (OCR)
-------------------------

Performs OCR and structured information extraction from supported document types.

*   **Method:** ``POST``
*   **Endpoint:** ``/document-extract-information/``
*   **Content-Type:** ``application/x-www-form-urlencoded``

**Body Parameters**

+------------------+------+---------------------------------------+
| Key              | Type | Description                           |
+==================+======+=======================================+
| ``base64_image`` | Text | Base64 encoded string of the document.|
+------------------+------+---------------------------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "success": true,
      "data": {
        "id_number": "XXXX-XXXX-XXXX",
        "name": "Jane Smith",
        "address": "Sample Address",
        "gender": "F",
        "dob": { "year": "1995", "month": "07", "day": "10" },
        "detected_type": "national-id",
        "confidence": 0.97
      }
    }

6. Image to Base64
------------------

Utility endpoint to convert an uploaded image file to a base64 string.

*   **Method:** ``POST``
*   **Endpoint:** ``https://ep-sa1.thirdfactor.ai/image-to-base64/``
*   **Note:** This endpoint has a specific host URL.

**Body Parameters (form-data)**

+---------+------+--------------+---------------------------+
| Key     | Type | Content-Type | Description               |
+=========+======+==============+===========================+
| ``image``| File | ``image/jpeg``| The image file to convert.|
+---------+------+--------------+---------------------------+

**Response (200 OK)**

.. code-block:: json

7. Generate KYC URL (SDK)
-------------------------

Generates a dynamic URL for the ThirdFactor SDK authentication process.

*   **Method:** ``POST``
*   **Endpoint:** ``/tfauth/get-kyc-url/``
*   **Auth:** Requires a self-signed JWT token in the body (or authorization header, implementation dependent).

**Request Body (JSON)**

The request requires specific payload data which should be used to generate a JWT token signed with your **JWT Token Secret**.

**Payload Data Sample:**

.. code-block:: json

    {
      "sub": "1234567890",
      "name": "Dhiraj Chapagain",
      "iss": "IZ8371QZ40",
      "token": "3IRY66384N",
      "iat": 1516239022,
      "identifier": "9888888888",
      "label": "Dhiraj Chapagain",
      "secondary_label": "dhiraj",
      "callback": "https://yourwebhook.comma/281f1268-6f8b-4cf9-903d-d8ab3ab9618a"
    }

*   ``callback``: The URL where the results of KYC Verification will be sent.

**JWT Generation:**

Use the payload data above and your secret to generate a JWT. You can test decoding at `jwt.io <https://jwt.io/>`_.

**Response (200 OK)**

.. code-block:: json

    {
      "url": "https://endpoint/tfauth/start?token=...",
      "remaining_credits": 96
    }

**Response (Error - Invalid Token)**

.. code-block:: json

    {
      "error": "Invalid token or token does not belong to tenant: Org Name"
    }

**Response (Error - Insufficient Credits)**

.. code-block:: json

    {
      "error": "Insufficient credits. Available credits: 0. 1 credit is required to generate KYC URL."
    }

Webhook Notification
--------------------

When the KYC process is completed, the SDK server sends a notification to the ``callback`` URL specified in the payload.

**Example Webhook Payload**

.. code-block:: json

    {
      "documentDetectionLog": [
        {
          "created_at": "2026-01-27 10:43:26.644142+00:00",
          "is_verified": true,
          "nationality": "nepali",
          "document_number": "11111111",
          "photo": "data:image/jpeg;base64,/9j/4AAQS..."
        }
      ]
    }
