JSON API
==================================

.. function:: /api/info/{stem}

   **Method:** GET

   **Example output:**

   .. code-block:: json

      {
          "stem": "kvuqM",
          "url": "https://github.com/"
          "shortened_url": "http://shorty.local/kvuqM",
          "added_time": 1692917681, // Unix timestamp
          "hits": 2,
      }

.. function:: /api/shorten

   **Method:** POST

   **Example payload:**

   .. code-block:: json

      {
          "url": "https://github.com/",
          "force": false
      }

   **Example output:**

   .. code-block:: json

      {
          "stem": "kvuqM",
          "shortened_url": "http://shorty.local/kvuqM",
      }

