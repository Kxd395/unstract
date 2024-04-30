class ToolCommandKey:
    PROPERTIES = "properties"
    SPEC = "spec"
    VARIABLES = "variables"
    ICON = "icon"


class LogType:
    LOG = "LOG"
    UPDATE = "UPDATE"
    COST = "COST"
    RESULT = "RESULT"
    SINGLE_STEP = "SINGLE_STEP_MESSAGE"


class ToolKey:
    TOOL_INSTANCE_ID = "tool_instance_id"


class Env:
    TOOL_CONTAINER_NETWORK = "TOOL_CONTAINER_NETWORK"
    TOOL_CONTAINER_LABELS = "TOOL_CONTAINER_LABELS"
    WORKFLOW_DATA_DIR = "WORKFLOW_DATA_DIR"
    TOOL_DATA_DIR = "TOOL_DATA_DIR"
    PRIVATE_REGISTRY_CREDENTIAL_PATH = "PRIVATE_REGISTRY_CREDENTIAL_PATH"
    PRIVATE_REGISTRY_USERNAME = "PRIVATE_REGISTRY_USERNAME"
    PRIVATE_REGISTRY_URL = "PRIVATE_REGISTRY_URL"
    LOG_LEVEL = "LOG_LEVEL"
    REMOVE_CONTAINER_ON_EXIT = "REMOVE_CONTAINER_ON_EXIT"
