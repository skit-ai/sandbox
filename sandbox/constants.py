import os

## data storage
DATA_DIR = "data"
TASKS_DIR = os.path.join(DATA_DIR, "tasks")
USERS_DIR = os.path.join(DATA_DIR, "users")

SESSION_INFO = "session_info.yaml"
SESSION_DATA = "session_data.yaml"
ADMIN_YAML = os.path.join(DATA_DIR, "admin.yaml")

## call status values - for outbound dialler client
END_STATUS = "LOGGED"
COMPLETED_STATUS = ["LOGGED", "ENDED"]
ALL_STATUS = ["LOGGED", "ENDED", "NOT ANSWERED", "NOT COMPLETED"]