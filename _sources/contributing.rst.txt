Contributing
============

Thank you for your interest in contributing to myshift! This guide will help you get started.

Development Setup
---------------

1. Fork the repository
2. Clone your fork:

.. code-block:: bash

   git clone https://github.com/yourusername/myshift.git
   cd myshift

3. Create a virtual environment:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # or
   .venv\Scripts\activate  # Windows

4. Install development dependencies:

.. code-block:: bash

   pip install -e ".[dev]"

Code Style
---------

We use the following tools to maintain code quality:

* `black` for code formatting
* `isort` for import sorting
* `mypy` for type checking
* `pylint` for linting

Run the formatters before committing:

.. code-block:: bash

   black .
   isort .

Running Tests
------------

Run the test suite:

.. code-block:: bash

   pytest

Run with coverage:

.. code-block:: bash

   pytest --cov=myshift

Building Documentation
--------------------

Build the documentation:

.. code-block:: bash

   cd docs
   make html

The built documentation will be in `docs/_build/html/`.

Pull Request Process
------------------

1. Update the documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update the changelog
5. Submit a pull request

Pull Request Checklist
~~~~~~~~~~~~~~~~~~~~

* [ ] Tests added/updated
* [ ] Documentation updated
* [ ] Changelog updated
* [ ] Code style checks pass
* [ ] Type checks pass
* [ ] All tests pass

Commit Messages
--------------

Follow the Conventional Commits specification:

* `feat:` for new features
* `fix:` for bug fixes
* `docs:` for documentation changes
* `style:` for formatting changes
* `refactor:` for code refactoring
* `test:` for test changes
* `chore:` for maintenance tasks

Example:

.. code-block:: text

   feat: add support for custom date formats

   - Add date_format configuration option
   - Update documentation
   - Add tests for new feature

Release Process
-------------

1. Update version in `pyproject.toml`
2. Update changelog
3. Create a release tag
4. Build and publish to PyPI

Code of Conduct
--------------

Please be respectful and considerate of others. We aim to foster an inclusive and welcoming community.

Reporting Bugs
-------------

1. Check if the bug has already been reported
2. Use the bug report template
3. Include steps to reproduce
4. Include expected and actual behavior
5. Include system information

Feature Requests
--------------

1. Check if the feature has already been requested
2. Use the feature request template
3. Explain the problem you're trying to solve
4. Describe the proposed solution
5. Consider implementation complexity

Questions and Discussion
---------------------

* Use GitHub Discussions for general questions
* Use GitHub Issues for bug reports and feature requests
* Join our community chat for real-time discussion

Thank you for contributing to myshift! 