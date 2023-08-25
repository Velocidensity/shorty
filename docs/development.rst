Development
==================================

Development environment is managed with poetry.

.. code-block:: console

   $ git clone https://github.com/Velocidensity/shorty
   $ cd shorty
   $ poetry install --with-dev

------------------------------
Compiling Tailwind CSS
------------------------------

Default frontend comes with a precompiled Tailwind file, but if you wish to change it, you can recompile it with the following commands:

.. code-block:: console

   $ npm install -D tailwindcss
   $ npx tailwindcss -c tailwind.config.js -o shorty/static/tailwind.css --minify

------------------------------
Formatting JavaScript code
------------------------------

JavaScript code is formatted using `semistandard <https://github.com/standard/semistandard>`_.
