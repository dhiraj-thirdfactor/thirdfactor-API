API Endpoints
=============

This guide details the available endpoints in the ThirdFactor AI API Gateway v0.1.0.

.. _overview:

Overview
--------

ThirdFactor.ai provides AI-powered identity verification and document understanding services through this secure API gateway.

**Base URL**
   ``https://<CUSTOM_URL>`` — issued to your organisation by ThirdFactor.ai.

**Authentication**
   HTTP Bearer Token — issued to your organisation by ThirdFactor.ai.

   .. code-block:: http

       Authorization: Bearer <YOUR_ACCESS_TOKEN>

**Content Types**

+------------------------------------------+------------------------------------------+
| Content-Type                             | Used for                                 |
+==========================================+==========================================+
| ``application/x-www-form-urlencoded``    | Most image-as-base64 inputs              |
+------------------------------------------+------------------------------------------+
| ``application/json``                     | JSON payloads (e.g., face comparison)    |
+------------------------------------------+------------------------------------------+
| ``multipart/form-data``                  | File uploads (e.g., raw image conversion)|
+------------------------------------------+------------------------------------------+

**HTTP Status Codes**

+-------+---------------------------------------------+
| Code  | Meaning                                     |
+=======+=============================================+
| 200   | Success                                     |
+-------+---------------------------------------------+
| 401   | Authentication error                        |
+-------+---------------------------------------------+
| 422   | Input validation failed                     |
+-------+---------------------------------------------+
| 500   | Internal server error                       |
+-------+---------------------------------------------+

All requests are authenticated and encrypted over HTTPS. API tokens must be kept confidential.

**Note regarding Image Inputs:**
All endpoints that accept image data (detect face, compare face, etc.) require the images to be uploaded in **Base64** format. This design ensures consistent handling of image data across various client platforms and network environments, simplifying the JSON payload structure.

.. _error-model:

Error Model
-----------

Sample validation error (HTTP 422):

.. code-block:: json

    {
      "detail": [
        {
          "loc": ["body", "field_name"],
          "msg": "Field is required",
          "type": "value_error.missing"
        }
      ]
    }

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

2. Image to Base64
------------------

Converts an uploaded image file into a base64 string. Use this if your client application needs to convert files before sending them to the analysis endpoints.

*   **Method:** ``POST``
*   **Endpoint:** ``/image-to-base64/``
*   **Auth:** Required
*   **Content-Type:** ``multipart/form-data``

**Form Data**

+-----------+------+------------+---------------------------+
| Key       | Type | Required   | Description               |
+===========+======+============+===========================+
| ``image`` | File | Yes        | Image file to convert.    |
+-----------+------+------------+---------------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "data_url": "data:image/jpeg;base64,/9j/4AAQ...",
      "content_type": "image/jpeg",
      "filename": "uploaded_image.jpg"
    }

3. Detect Face
--------------

Detects faces and optional attributes (age range, gender, occlusion, etc.).

*   **Method:** ``POST``
*   **Endpoint:** ``/detect-face/``
*   **Auth:** Required
*   **Content-Type:** ``application/x-www-form-urlencoded``

**Body Parameters**

+------------------+--------+------------+--------------------------------------------------------------------------------------+
| Key              | Type   | Default    | Description                                                                          |
+==================+========+============+======================================================================================+
| ``base64_image`` | string | *Required* | Base64 encoded string of the image containing the face.                              |
+------------------+--------+------------+--------------------------------------------------------------------------------------+
| ``features``     | string | ``ALL``    | Comma-separated list: ``ALL`` | ``AGE_RANGE`` | ``EYEGLASSES`` |                      |
|                  |        |            | ``GENDER`` | ``FACE_OCCLUDED`` | ``SUNGLASSES``                                       |
+------------------+--------+------------+--------------------------------------------------------------------------------------+

**Response (200 OK — faces found)**

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

**Response (200 OK — no faces found)**

.. code-block:: json

    { "result": false, "total_faces": 0, "faces": [] }

4. Analyze Liveness
-------------------

Analyzes a video file to verify liveness and detecting potential spoofing attempts.

*   **Method:** ``POST``
*   **Endpoint:** ``/api/analyze-liveness``
*   **Auth:** Not required
*   **Content-Type:** ``multipart/form-data``

**Body Parameters (form-data)**

+---------+------+--------------+---------------------------+
| Key     | Type | Content-Type | Description               |
+=========+======+==============+===========================+
| ``video``| File | ``item/binary``| The video file to analyze.|
+---------+------+--------------+---------------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "analysis": {
        "liveness_score": "0.70",
        "antispoof_score": "1.00",
        "blink_count": 0
      },
      "antispoof_score": "1.00",
      "blink_count": 0,
      "liveness_score": "0.70",
      "frames": [
        0: "data:image/jpeg;base64,/9j/4AAQ...",
        1:"data:image/jpeg;base64,/9j/4AAQ..."
      ],
      "is_live": true
    }

5. Compare Face (1:1)
---------------------

Compares two face images to verify if they belong to the same person.

*   **Method:** ``POST``
*   **Endpoint:** ``/compare-face/``
*   **Auth:** Required
*   **Content-Type:** ``application/json``

**Query Parameters**

+---------------------+-----------+-------------------------------------------------------------------+
| Key                 | Default   | Description                                                       |
+=====================+===========+===================================================================+
| ``threshold``       | ``52.0``  | Similarity threshold (float) for matching.                        |
+---------------------+-----------+-------------------------------------------------------------------+
| ``live_check``      | ``false`` | Optional liveness check (boolean).                                |
+---------------------+-----------+-------------------------------------------------------------------+
| ``occlusion_check`` | ``false`` | Check for face obstructions (boolean).                            |
+---------------------+-----------+-------------------------------------------------------------------+

**Body (JSON Array)**

.. code-block:: json

    [
      "<BASE64_IMAGE_1>",
      "<BASE64_IMAGE_2>"
    ]

**Response (200 OK — match)**

.. code-block:: json

    {
      "verified": true,
      "confidence": 98.5,
      "percentage_match": 99.9
    }

**Response (200 OK — no match)**

.. code-block:: json

    {
      "verified": false,
      "percentage_match": 0
    }

6. Compare Face (1:N)
---------------------

Performs a reverse search to find a face match within a pre-ingested database.

*   **Method:** ``POST``
*   **Endpoint:** ``/api/face-reverse-search``
*   **Auth:** Not required
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

7. Ingest Face (1:N Search)
---------------------------

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

8. Detect & Crop Document
-------------------------

Automatically detects the type of document and returns a cropped image.

*   **Method:** ``POST``
*   **Endpoint:** ``/type-of-document-crop/``
*   **Auth:** Required
*   **Content-Type:** ``application/x-www-form-urlencoded``

**Supported Document Types:**

The API recognises the following document types:

*   ``citizenship-front`` / ``citizenship-back``
*   ``driving-license``
*   ``passport-front`` / ``passport-back``
*   ``pan-id``
*   ``disability-id``
*   ``national-id``
*   ``voter-id``
*   ``foreign-passport``

**Body Parameters**

+------------------+--------+------------+----------------------------------------------+
| Key              | Type   | Required   | Description                                  |
+==================+========+============+==============================================+
| ``base64_image`` | string | Yes        | Base64 encoded string of the document image. |
+------------------+--------+------------+----------------------------------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "document_type": "national-id-front",
      "score": 0.98,
      "cropped_image": "data:image/jpeg;base64,/9j/..."
    }

9. Analyze Document (OCR)
-------------------------

Performs OCR and structured information extraction from supported document types.

*   **Method:** ``POST``
*   **Endpoint:** ``/document-extract-information/``
*   **Auth:** Required
*   **Content-Type:** ``application/x-www-form-urlencoded``

**Body Parameters**

+------------------+--------+------------+-----------------------------------------------+
| Key              | Type   | Required   | Description                                   |
+==================+========+============+===============================================+
| ``base64_image`` | string | Yes        | Base64 encoded string of the document image.  |
+------------------+--------+------------+-----------------------------------------------+

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

10. Detect Forgery
------------------

Analyzes an image to detect potential manipulation or forgery.

*   **Method:** ``POST``
*   **Endpoint:** ``/api/analyze``
*   **Auth:** Not required
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

11. Generate KYC URL (SDK)
--------------------------

Generates a dynamic URL for the ThirdFactor SDK authentication process. To use this endpoint, you must first generate a signed JWT token.

**1. Generate JWT Token**

Create a JWT token signed with **HMAC SHA256 (HS256)** using your provided **Secret**.

*   **Header:**

    .. code-block:: json

        {
          "alg": "HS256",
          "typ": "JWT"
        }

*   **Payload:**

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
          "callback": "https://your-webhook.com/callback-id",
          "is_sdk": true
        }

    *   ``callback``: The URL where the results of the KYC Verification will be sent via webhook.

**2. Make the Request**

*   **Method:** ``POST``
*   **Request URL:** ``https://<thirdfactor_URL>/tfauth/get-kyc-url/``
*   **Content-Type:** ``application/json``

**Request Body:**

Include the generated JWT token in the JSON body.

.. code-block:: json

    {
        "jwt_token": "<YOUR_GENERATED_JWT_TOKEN>"
    }

**Response (200 OK)**

.. code-block:: json

    {
        "url": "https://endpoint/tfauth/start?",
        "remaining_credits": 97
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

**11.1 Webhook Notification (Full Payload)**

When the KYC process is completed, the SDK server sends a notification to the ``callback`` URL specified in the payload. The payload provides a complete log of the detection and verification process.

**Example Payload Structure:**

.. code-block:: json

    {
      "documentDetectionLog": [
        {
          "created_at": "2026-01-27 10:43:26.644142+00:00",
          "is_verified": true,
          "nationality": "nepali",
          "document_number": "11111111",
          "photo": "<BASE64_STRING_OF_SCANNED_DOC>",
          "original_photo": "<BASE64_STRING_OF_ORIGINAL_FRAME>",
          "claimed_doc_type": "citizenship-back",
          "detected_doc_type": "citizenship-back",
          "reason": "Valid Type"
        },
        {
          "created_at": "2026-01-27 10:43:27.201931+00:00",
          "is_verified": true,
          "nationality": "nepali",
          "document_number": "11111111",
          "photo": "<BASE64_STRING>",
          "original_photo": "<BASE64_STRING>",
          "percentage_match": 64.7401,
          "claimed_doc_type": "citizenship-front",
          "detected_doc_type": "citizenship-front",
          "reason": "Valid"
        }
      ],
      "documentPhoto": [
        {
          "created_at": "2026-01-27 10:43:26.644142+00:00",
          "is_verified": true,
          "nationality": "nepali",
          "document_number": "11111111",
          "photo": "<BASE64_STRING>",
          "claimed_doc_type": "citizenship-back",
          "detected_doc_type": "citizenship-back",
          "reason": "Valid Type"
        }
      ],
      "gestureDetectionLog": [
        {
          "created_at": "2026-01-27 10:43:10.255518+00:00",
          "is_verified": true,
          "challenged_gesture": "Thumb_Down",
          "detected_gesture": "Thumb_Down",
          "percentage_match": 80.8998,
          "photo": "<BASE64_STRING_OF_GESTURE>",
          "reason": "Valid",
          "is_passive_live": true,
          "passive_score": 99.998
        }
      ],
      "faceDetectionLog": [
        {
          "created_at": "2026-01-27 10:42:58.538744+00:00",
          "is_verified": false,
          "photo": "<BASE64_STRING_OF_FACE>",
          "age": "-1",
          "gender": "N/A",
          "reason": "Face Occluded or Blurry.",
          "force_next": true
        }
      ],
      "nationality": "nepali",
      "completed_at": "2026-01-27T10:43:27.882837+00:00",
      "bypassed": 1,
      "document_uplaod_retries": 2,
      "session": "F7bgp2I",
      "faceDetectionSuccess": false,
      "document_number": "11111111",
      "gestureSuccess": true,
      "gender": "N/A",
      "documentDetectionSuccess": true,
      "in_progress": 0,
      "age": -1,
      "expires_at": "2026-01-29T18:24:26.141586+00:00",
      "userPhoto": "<BASE64_STRING_OF_USER>",
      "gesture_photo": "<BASE64_STRING>",
      "gesture_challenge": [
        "Thumb_Down"
      ],
      "percentage_match": 64.7401,
      "face_detection_retries": 1,
      "allow_force_next": 1,
      "started_at": "2026-01-27T10:42:46.141586+00:00",
      "gesture_verification_retries": 1,
      "label": "Jane User",
      "secondary_label": "jane",
      "identifier": "1715",
      "jwt": "<JWT_TOKEN>",
      "is_verified": true,
      "forced_next": false,
      "signature": "<SIGNATURE>"
    }

*   **Note:** The ``photo``, ``original_photo``, ``userPhoto``, and ``gesture_photo`` fields contain the full **Base64** string of the respective images.

12. KYB - Business Document Detection
-------------------------------------

Set of endpoints for detecting and validating business-related documents.

**12.1 Single Inference**

Detects business document class in a single uploaded image.

*   **Method:** ``POST``
*   **Endpoint:** ``/api/v1/business_doc_detection/inference/single``
*   **Content-Type:** ``multipart/form-data``

**Parameters**

+--------------------+----------+-------------------------------------------------+
| Key                | Type     | Description                                     |
+====================+==========+=================================================+
| ``file``           | File     | **Required**. The image file to analyze.        |
| ``expected_class`` | Text     | Optional. The expected class name for validaton.|
| ``confidence``     | Number   | Optional. Confidence threshold. Default: ``0.7``|
+--------------------+----------+-------------------------------------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "filename": "image.jpg",
      "predicted_class": "business_vat_pan",
      "expected_class": "business_vat_pan",
      "confidence": 0.95,
      "is_correct": true,
      "bbox": [100, 150, 400, 500],
      "output_path": "/app/media_files/results/image.jpg"
    }

**12.2 Folder Inference**

Batch processes images within a specified folder path.

*   **Method:** ``POST``
*   **Endpoint:** ``/api/v1/business_doc_detection/inference/folder``
*   **Content-Type:** ``multipart/form-data``

**Parameters**

+-----------------+----------+-------------------------------------------------+
| Key             | Type     | Description                                     |
+=================+==========+=================================================+
| ``folder_path`` | Text     | **Required**. Path to the folder containing imgs|
| ``confidence``  | Number   | Optional. Confidence threshold. Default: ``0.7``|
+-----------------+----------+-------------------------------------------------+

**Response (200 OK)**

.. code-block:: json

    {
      "total_images": 10,
      "correct_predictions": 8,
      "incorrect_predictions": 1,
      "no_predictions": 1,
      "files": [
         { "filename": "doc1.jpg", "predicted_class": "vat", "confidence": 0.98 },
         { "filename": "doc2.jpg", "predicted_class": "pan", "confidence": 0.92 }
      ]
    }

**12.3 Health Check (KYB)**

Checks the status of the Business Document Detection service.

*   **Method:** ``GET``
*   **Endpoint:** ``/api/v1/business_doc_detection/health``

**Response (200 OK)**

.. code-block:: json

    { "status": "Ok" }

---

Security & Compliance
---------------------

*   **Transport Security** — All traffic must use HTTPS (TLS 1.2+). Plain HTTP requests are rejected.

*   **Transient Processing** — Face and document data are processed transiently. No images are stored unless explicitly configured for audit logging.

*   **Privacy Compliance** — ThirdFactor.ai is mostly compliant with major privacy frameworks, including:

    *   **GDPR** (General Data Protection Regulation)

*   **Token Confidentiality** — API Bearer tokens must be kept confidential and must never be exposed in client-side code or public repositories.

