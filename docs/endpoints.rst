API Endpoints
=============

This guide details the available endpoints in the ThirdFactor AI API Gateway v0.1.0. 

All endpoints, unless otherwise stated, require an **Authorization** header with a valid Bearer token.

.. code-block:: http

    Authorization: Bearer <YOUR_ACCESS_TOKEN>

---

1. Health Check
---------------

Verifies that the API service is operational.

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

Analyzes a base64-encoded image to detect faces and extract specified attributes.

*   **Method:** ``POST``
*   **Endpoint:** ``/detect-face/``
*   **Content-Type:** ``application/x-www-form-urlencoded``

**Body Parameters**

+------------------+------+------------+-------------------------------------------------------------+
| Key              | Type | Default    | Description                                                 |
+==================+======+============+=============================================================+
| ``base64_image`` | Text | *Required* | The base64 encoded string of the image containing the face. |
| ``features``     | Text | ``ALL``    | Comma-separated list: ``ALL``, ``AGE_RANGE``, ``EYEGLASSES``, |
|                  |      |            | ``GENDER``, ``FACE_OCCLUDED``, ``SUNGLASSES``.                |
+------------------+------+------------+-------------------------------------------------------------+

**Response (200 OK)**

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

3. Compare Face
---------------

Performs a 1:1 comparison between two face images to verify identity.

*   **Method:** ``POST``
*   **Endpoint:** ``/compare-face/``
*   **Content-Type:** ``application/json``

**Query Parameters**

+---------------------+----------+----------------------------------------+
| Key                 | Value    | Description                            |
+=====================+==========+========================================+
| ``threshold``       | ``52.0`` | Similarity threshold for matching.     |
| ``live_check``      | ``false``| Enable liveness checking (true/false). |
| ``occlusion_check`` | ``false``| Enable occlusion checking (true/false).|
+---------------------+----------+----------------------------------------+

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

4. Detect & Crop Document Type
------------------------------

Identifies the type of document (e.g., national-id, passport) and returns a cropped version of the image.

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

Extracts structured text information from supported document types using OCR.

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

A utility endpoint to convert an uploaded image file into a base64 string.

*   **Method:** ``POST``
*   **Endpoint:** ``<base_url>/image-to-base64/``

**Body Parameters (form-data)**

+---------+------+--------------+---------------------------+
| Key     | Type | Content-Type | Description               |
+=========+======+==============+===========================+
| ``image``| File | ``image/jpeg``| The image file to convert.|
+---------+------+--------------+---------------------------+

7. Forgery Detection
--------------------

Analyzes an image to detect potential manipulation or forgery.

*   **Method:** ``POST``
*   **Endpoint:** ``/api/analyze``
*   **Content-Type:** ``multipart/form-data``

**Body Parameters (form-data)**

+---------+------+--------------+---------------------------+
| Key     | Type | Content-Type | Description               |
+=========+======+==============+===========================+
| ``image``| File | ``image/png`` | The image file to analyze.|
+---------+------+--------------+---------------------------+

**Response (200 OK)**

.. code-block:: json

    {
        "is_forged": false,
        "original_image": "/static/uploads/original_ID.png",
        "highlighted_image": "/static/uploads/overlay_ID.png",
        "analysis": {
            "status": "AUTHENTIC",
            "forgery_score": "0.13",
            "details": "No manipulation detected"
        }
    }

8. 1:N Reverse Face Search
--------------------------

Performs a reverse search to find a face match within a pre-ingested database.

*   **Method:** ``POST``
*   **Endpoint:** ``/api/face-reverse-search``
*   **Content-Type:** ``binary``

**Body**

*   **Binary File:** Upload the image file as the raw body content.

**Response (200 OK)**

.. code-block:: json

    {
        "matches": [
            {
                "id": 6,
                "score": 0.0,
                "metadata": {
                    "filename": "ingest_1764663714_user.jpg"
                }
            },
            {
                "id": 25,
                "score": 0.32,
                "metadata": {
                    "filename": "ingest_1768883379_FRONT.jpg"
                }
            }
        ],
        "query_time_seconds": 1.38,
        "search_time_seconds": 0.00007,
        "query_image": "/static/uploads/query_1769539703.jpg",
        "total_time_seconds": 1.39
    }

9. Batch Ingest (1:N Search)
----------------------------

Ingests an image into the database for future 1:N reverse face searches.

*   **Method:** ``POST``
*   **Endpoint:** ``/batch_ingest``
*   **Content-Type:** ``binary``

**Body**

*   **Binary File:** Upload the image file as the raw body content.

**Response (200 OK)**

.. code-block:: json

    {
        "results": [
            {
                "filename": "test.jpeg",
                "id": 35
            }
        ]
    }

10. Generate KYC URL (SDK)
--------------------------

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
      "name": "Jane User",
      "iss": "<YOUR_ISSUER_ID>",
      "token": "<YOUR_TOKEN>",
      "iat": 1516239022,
      "identifier": "9888888888",
      "label": "Jane User",
      "secondary_label": "jane",
      "callback": "https://your-webhook.com/callback-id"
    }

*   ``callback``: The URL where the results of KYC Verification will be sent.

**Response (200 OK)**

.. code-block:: json

    {
      "url": "https://<endpoint>/tfauth/start?token=...",
      "remaining_credits": 96
    }

**Response (Error - Invalid Token)**

.. code-block:: json

    {
      "error": "Invalid token or token does not belong to tenant: <Org Name>"
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
          "created_at": "2026-01-27T10:43:26.644142+00:00",
          "is_verified": true,
          "nationality": "nepali",
          "document_number": "11111111",
          "photo": "data:image/jpeg;base64,/9j/4AAQS...",
          "original_photo": "data:image/jpeg;base64,/9j/4AAQS..."
        }
      ]
    }

*   **Note:** The ``photo`` and ``original_photo`` fields contain the full **Base64** string of the respective images.
