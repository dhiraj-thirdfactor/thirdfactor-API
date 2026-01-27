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
   security
