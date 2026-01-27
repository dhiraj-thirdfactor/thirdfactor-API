ThirdFactor AI API Gateway
============================

**Version:** 0.1.0
**Released:** 2025-11-21

Welcome to the documentation for the **ThirdFactor AI API Gateway**. This API provides robust face detection, verification, and document analysis services.

Core Services
-------------

The API Gateway primarily exposes the following services:

*   **Face Detection**: Detect faces within images and analyze features.
*   **Face Verification**: Compare faces to determine similarity and identity.
*   **Document Analysis**: Analyze and extract text from documents (OCR) and handle document cropping.

Base URL
--------

All API requests (unless otherwise specified) should be directed to the base URL:

.. code-block:: text

    https://<YOUR_API_ENDPOINT>

*Note: Replace `<YOUR_API_ENDPOINT>` with the actual endpoint provided to you.*

Authentication
--------------

The API uses **HTTP Bearer Token** authentication. All requests must include the ``Authorization`` header with a valid token.

**Header Format:**

.. code-block:: http

    Authorization: Bearer <YOUR_ACCESS_TOKEN>

Response Status Codes
---------------------

The API uses standard HTTP status codes to indicate the success or failure of a request.

*   **200 OK**: Request was successful.
*   **422 Unprocessable Entity**: Validation failed (e.g., missing fields, invalid format).
*   **401 Unauthorized**: Authentication failed or invalid token.
*   **500 Internal Server Error**: An unexpected error occurred on the server.

Error Model
-----------

When a request fails validation (HTTP 422), the API returns a structured JSON response detailing the error.

**Sample Validation Error:**

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

Version History
---------------

+---------+------------+------------------------------------------+
| Version | Date       | Changes                                  |
+=========+============+==========================================+
| 0.1.0   | 2025-11-21 | Initial public release of Face &         |
|         |            | Document APIs                            |
+---------+------------+------------------------------------------+

Contents
--------

.. toctree::
   :maxdepth: 2

   endpoints
