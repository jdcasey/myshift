"""Constants used throughout the myshift package."""

# Configuration file locations
DEFAULT_CONFIG_DIR = "~/.config/myshift"
DEFAULT_CONFIG_FILE = "config.yaml"

# Configuration keys
CONFIG_API_KEY = "api_key"
CONFIG_SCHEDULE_ID = "schedule_id"
CONFIG_TIMEZONE = "timezone"
CONFIG_DISPLAY_FORMAT = "display_format"
CONFIG_LOG_LEVEL = "log_level"

# Display formats
DISPLAY_FORMAT_DEFAULT = "default"
DISPLAY_FORMAT_JSON = "json"
DISPLAY_FORMAT_YAML = "yaml"

# Log levels
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_ERROR = "ERROR"

# Time formats
TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"

# API endpoints
API_BASE_URL = "https://api.pagerduty.com"
API_VERSION = "2" 