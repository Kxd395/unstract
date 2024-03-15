from django.conf import settings


class LoginConstant:
    INVITATION = "invitation"
    ORGANIZATION = "organization"
    ORGANIZATION_NAME = "organization_name"


class Common:
    NEXT_URL_VARIABLE = "next"
    PUBLIC_SCHEMA_NAME = "public"
    ID = "id"
    USER_ID = "user_id"
    USER_EMAIL = "email"
    USER_EMAILS = "emails"
    USER_IDS = "user_ids"
    USER_ROLE = "role"
    MAX_EMAIL_IN_REQUEST = 10


class UserModel:
    USER_ID = "user_id"
    ID = "id"


class OrganizationMemberModel:
    USER_ID = "user__user_id"
    ID = "user__id"


class Cookie:
    ORG_ID = "org_id"
    Z_CODE = "z_code"
    CSRFTOKEN = "csrftoken"


class ErrorMessage:
    ORGANIZATION_EXIST = "Organization already exists"
    DUPLICATE_API = "It appears that a duplicate call may have been made."
    USER_LOGIN_ERROR = "Invalid username or password. Please try again."


class DefaultOrg:
    ORGANIZATION_NAME = "mock_org"
    MOCK_ORG = "mock_org"
    MOCK_USER = "unstract"
    MOCK_USER_ID = "mock_user_id"
    MOCK_USER_EMAIL = "email@mock.com"
    MOCK_USER_PASSWORD = settings.DEFAULT_AUTH_PASSWORD


class UserLoginTemplate:
    TEMPLATE = "login.html"
    ERROR_PLACE_HOLDER = "error_message"


class PluginConfig:
    PLUGINS_APP = "plugins"
    AUTH_MODULE_PREFIX = "auth"
    AUTH_PLUGIN_DIR = "authentication"
    AUTH_MODULE = "module"
    AUTH_METADATA = "metadata"
    METADATA_SERVICE_CLASS = "service_class"
    METADATA_IS_ACTIVE = "is_active"


class AuthorizationErrorCode:
    """Error code reference
    frontend/src/components/error/GenericError/GenericError.jsx."""

    IDM = "IDM"
    UMM = "UMM"
    INF = "INF"
    USF = "USF"
