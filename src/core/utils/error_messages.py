class ErrorMessages:
    X_REQUEST_ID_REQUIRED = "X-Request-ID header is required"
    NO_SCOPE_FOUND = "No Scope found"
    INVALID_TOKEN = "Invalid Token"
    TOKEN_SCOPE_DISABLED = "Disabled Scope in Token"
    INACTIVE = "Inactive"
    INVALID_USERNAME = "Invalid Username "
    INCORRECT_PASSWORD = "Incorrect Password"
    BLOCKED_USERNAME = "Disabled Username"
    INVALID_CONSUMER = "Invalid Consumer"
    BLOCKED_CONSUMER = "Disabled Consumer"
    INVALID_SCOPE = "Invalid Scope"
    BLOCKED_SCOPE = "Disabled Scope"
    NO_FILES = "No Files Found"
    INVALID_FILE_TYPE = "Invalid file type. Please upload pdf files"
    INVALID_IMAGE_TYPE = "Invalid image type. Please upload image files"
    LARGE_FILE = "File size too big"
    LARGE_IMAGE = "Image size too big"
    INVALID_UUID = "Invalid value. It must be a valid UUID."
    INVALID_UUID_4 = "Invalid value. It must be a valid UUIDv4."
    INVALID_THREAD_ID = "Invalid thread_id. It must be a valid UUIDv4."
    INVALID_FILE_ID = "Invalid File Id"
    NO_FILES_TO_VECTORIZED = "No files to vectorized"


errors = ErrorMessages()
