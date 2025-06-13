# Contributing to myshift

Thank you for your interest in contributing to myshift! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## Development Environment

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- A PagerDuty account with API access

### Setting Up

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/myshift.git
   cd myshift
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. Make your changes, following the coding standards below

3. Run tests:
   ```bash
   pytest
   ```

4. Commit your changes using semantic commit messages (see below)

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request from your fork to the main repository

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use type hints for function parameters and return values
- Keep functions focused and small
- Write docstrings for all public functions and classes
- Use meaningful variable and function names

### Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/) for our commit messages. This helps maintain a clear and consistent history of changes.

#### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

#### Types

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools
- `ci`: Changes to CI configuration files and scripts

#### Scopes

- `cli`: Command-line interface changes
- `config`: Configuration file handling
- `api`: PagerDuty API integration
- `container`: Container-related changes
- `deps`: Dependency updates
- `docs`: Documentation changes

#### Examples

```
feat(cli): add next command to show upcoming shift

Adds a new command that shows the next scheduled shift for a user.
This is a simpler alternative to the upcoming command when only
the next shift is needed.

Closes #123
```

```
fix(api): handle rate limiting in PagerDuty API calls

- Add exponential backoff for rate-limited requests
- Add proper error handling for 429 responses
- Update documentation with rate limit information

Fixes #456
```

```
docs(readme): update container usage instructions

- Add quay.io image information
- Update mount path for configuration file
- Add examples for both podman and docker
```

#### Guidelines

1. Use the present tense ("Add feature" not "Added feature")
2. Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
3. Limit the first line to 72 characters or less
4. Reference issues and pull requests liberally after the first line
5. Consider starting the commit message with an applicable emoji:
   - 🎨 `:art:` when improving the format/structure of the code
   - 🐎 `:racehorse:` when improving performance
   - 🚱 `:non-potable_water:` when plugging memory leaks
   - 📝 `:memo:` when writing docs
   - 🐛 `:bug:` when fixing a bug
   - 🔥 `:fire:` when removing code or files
   - 💚 `:green_heart:` when fixing the CI build
   - ✅ `:white_check_mark:` when adding tests
   - 🔒 `:lock:` when dealing with security
   - ⬆️ `:arrow_up:` when upgrading dependencies
   - ⬇️ `:arrow_down:` when downgrading dependencies

### Documentation

- Update README.md if you add new features or change existing ones
- Document all new command-line options
- Include examples in docstrings and documentation

## Testing

- Write tests for new features
- Ensure all tests pass before submitting a PR
- Include both unit tests and integration tests where appropriate
- Test edge cases and error conditions

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation with any new command-line options
3. The PR will be reviewed by maintainers
4. Address any feedback or requested changes
5. Once approved, your PR will be merged

## Adding New Features

When adding new features:

1. Discuss the feature in an issue first
2. Follow the existing code structure
3. Add appropriate tests
4. Update documentation
5. Add examples of usage

## Reporting Bugs

When reporting bugs, please include:

1. A clear description of the bug
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, etc.)
6. Any relevant error messages or logs

## Questions and Support

If you have questions or need help:

1. Check the existing documentation
2. Search existing issues
3. Create a new issue if needed

## License

By contributing to myshift, you agree that your contributions will be licensed under the project's Apache License 2.0. 