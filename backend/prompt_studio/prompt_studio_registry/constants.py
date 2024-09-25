class PromptStudioRegistryKeys:
    CREATED_BY = "created_by"
    TOOL_ID = "tool_id"
    NUMBER = "Number"
    FLOAT = "Float"
    PG_VECTOR = "Postgres pg_vector"
    ANSWERS = "answers"
    UNIQUE_FILE_ID = "unique_file_id"
    PROMPT_REGISTRY_ID = "prompt_registry_id"
    FILE_NAME = "file_name"
    UNDEFINED = "undefined"
    TABLE = "table"
    RECORD = "record"


class PromptStudioRegistryErrors:
    SERIALIZATION_FAILED = "Data Serialization Failed."
    DUPLICATE_API = "It appears that a duplicate call may have been made."
    CUSTOM_TOOL_EXISTS = "Custom tool with similiar configuration already exists"


class LogLevels:
    INFO = "INFO"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    RUN = "RUN"


# TODO: Update prompt studio constants to have a single source of truth
class JsonSchemaKey:
    TYPE = "type"
    TITLE = "title"
    DEFAULT = "default"
    ENUM = "enum"
    DESCRIPTION = "description"
    REQUIRED = "required"
    STRING = "string"
    PROCESSOR_TO_USE = "Processor to use"
    AZURE_OPEN_AI = "Azure OpenAI"
    PROPERTIES = "properties"
    DISPLAY_NAME = "display_name"
    FUNCTION_NAME = "function_name"
    PARAMETERS = "parameters"
    VERSIONS = "versions"
    OUTPUT_TYPE = "output_type"
    INPUT_TYPE = "input_type"
    IS_CACHABLE = "is_cacheable"
    REQUIRES = "requires"
    DEFAULT_DESCRIPTION_PROCESSOR = "Use Unstract processor \
        if you do not want to use a cloud provider for privacy reasons"
    NAME = "name"
    ACTIVE = "active"
    PROMPT = "prompt"
    CHUNK_SIZE = "chunk-size"
    PROMPTX = "promptx"
    VECTOR_DB = "vector-db"
    EMBEDDING = "embedding"
    X2TEXT_ADAPTER = "x2text_adapter"
    CHUNK_OVERLAP = "chunk-overlap"
    LLM = "llm"
    RETRIEVAL_STRATEGY = "retrieval-strategy"
    SIMPLE = "simple"
    TYPE = "type"
    NUMBER = "number"
    EMAIL = "email"
    DATE = "date"
    BOOLEAN = "boolean"
    JSON = "json"
    PREAMBLE = "preamble"
    SIMILARITY_TOP_K = "similarity-top-k"
    PROMPT_TOKENS = "prompt_tokens"
    COMPLETION_TOKENS = "completion_tokens"
    TOTAL_TOKENS = "total_tokens"
    RESPONSE = "response"
    POSTAMBLE = "postamble"
    GRAMMAR = "grammar"
    WORD = "word"
    SYNONYMS = "synonyms"
    OUTPUTS = "outputs"
    SECTION = "section"
    DEFAULT = "default"
    AUTHOR = "author"
    ICON = "icon"
    REINDEX = "reindex"
    TOOL_ID = "tool_id"
    EMBEDDING_SUFFIX = "embedding_suffix"
    FUNCTION_NAME = "function_name"
    PROMPT_REGISTRY_ID = "prompt_registry_id"
    NOTES = "NOTES"
    TOOL_SETTINGS = "tool_settings"
    ENABLE_CHALLENGE = "enable_challenge"
    CHALLENGE_LLM = "challenge_llm"
    ENABLE_SINGLE_PASS_EXTRACTION = "enable_single_pass_extraction"
    SUMMARIZE_PROMPT = "summarize_prompt"
    SUMMARIZE_AS_SOURCE = "summarize_as_source"
    ENABLE_HIGHLIGHT = "enable_highlight"
    PLATFORM_POSTAMBLE = "platform_postamble"


class SpecKey:
    PROCESSOR = "processor"
    SPEC = "spec"
    OUTPUT_FOLDER = "outputFolder"
    CREATE_OUTPUT_DOCUMENT = "createOutputDocument"
    USE_CACHE = "useCache"
    EMBEDDING_TRANSFORMER = "embeddingTransformer"
    VECTOR_STORE = "vectorstore"
    OUTPUT_TYPE = "outputType"
    OUTPUT_PROCESSING = "outputProcessing"
