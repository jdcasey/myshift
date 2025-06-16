# myshift

A command-line tool for managing on-call schedules in PagerDuty.

## Installation

### From Source

```bash
git clone https://github.com/jdcasey/myshift.git
cd myshift
pip install -e .
```

### From Container

```bash
# Using podman
podman run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml quay.io/jdcasey/myshift

# Using docker
docker run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml quay.io/jdcasey/myshift
```

### From PyPI

```bash
pip install myshift
```

## Configuration

Create a `myshift.yaml` file in one of the following standard locations:

### Linux
- `$XDG_CONFIG_HOME/myshift.yaml` (if XDG_CONFIG_HOME is set)
- `~/.config/myshift.yaml` (default if XDG_CONFIG_HOME is not set)

### macOS
- `~/Library/Application Support/myshift.yaml`

You can generate a sample configuration file by running:
```bash
myshift config --print
```

The configuration file should have the following structure:

```yaml
# PagerDuty API token
token: "your-pagerduty-token"

# Default schedule ID (optional)
# schedule_id: "your-default-schedule-id"

# Your PagerDuty user ID or email (optional)
# This will be used when no --user-id or --user-email is provided
# my_user: "your-email@example.com"  # or "your-user-id"
```

- `token`: Your PagerDuty API token (required)
- `schedule_id`: The ID of your PagerDuty schedule (optional)
- `my_user`: Your PagerDuty user ID or email address (optional)

## Usage

### Container Usage

```bash
# Using podman
podman run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml myshift

# Using docker
docker run -it --rm -v /path/to/myshift.yaml:/etc/myshift.yaml myshift
```

**NOTE:** When you run in container mode, the `repl` command will be used.

### Command Line Usage

#### Show Next On-Call Shift

```bash
myshift next [schedule_id] [--user-id USER_ID | --user-email USER_EMAIL]
```

Shows your next on-call shift. If no user is specified, uses the `my_user` from your configuration.

#### Show Upcoming On-Call Shifts

```bash
myshift upcoming [schedule_id] [--user-id USER_ID | --user-email USER_EMAIL] [--weeks WEEKS]
```

Shows your upcoming on-call shifts for the next N weeks (default: 4).

#### Show All On-Call Shifts

```bash
myshift plan [schedule_id] [--weeks WEEKS] [--utc]
```

Shows all on-call shifts in the schedule for the next N weeks (default: 4). Use `--utc` to display times in UTC instead of local timezone.

## Development

### Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- black for code formatting
- flake8 for linting
- mypy for type checking

Run all checks with:
```bash
pre-commit run --all-files
```

## License

Apache License 2.0 