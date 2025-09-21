import logging
import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MoenvOpenApiAgent(LlmAgent):
    def __init__(self, model_name: str, api_base: str | None = None, api_key: str | None = None):
        lite_llm_config = {"model": model_name, "max_output_tokens": 4096}
        if api_base:
            lite_llm_config["api_base"] = api_base
        if api_key:
            lite_llm_config["api_key"] = api_key

        # Get MOENV API Key from environment variable
        moenv_api_key = os.environ.get("MOENV_API_KEY")
        if not moenv_api_key:
            raise ValueError("MOENV_API_KEY environment variable not set.")

        # Create AuthCredential for MOENV API Key
        moenv_api_credential = AuthCredential(auth_type=AuthCredentialTypes.API_KEY, api_key=moenv_api_key)

        # Load OpenAPI Specification
        file_path = os.path.join(os.path.dirname(__file__), "moenv_openapi.yaml")
        file_content = None
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                file_content = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The API Spec '{file_path}' was not found.")

        # Create OpenAPIToolset
        # The MOENV API uses api_key as a query parameter, so we pass it directly to the toolset.
        # The toolset will then include it in the generated function calls.
        openapi_toolset = OpenAPIToolset(
            spec_str=file_content,
            spec_str_type="yaml",
            auth_credential=moenv_api_credential,
        )

        super().__init__(
            name="moenv_openapi_agent",
            model=LiteLlm(**lite_llm_config),
            instruction=(
                "你是一個能夠查詢台灣環境部開放資料的智能助理。"  # You are an intelligent assistant that can query Taiwan's Ministry of Environment open data.
                "請根據使用者的自然語言查詢，利用提供的工具來獲取環境資料。"  # Please use the provided tools to retrieve environmental data based on the user's natural language query.
                "例如：當使用者詢問「查詢酸雨監測值」，請使用酸雨監測相關工具。"  # For example: when the user asks "query acid rain monitoring values", please use the acid rain monitoring related tools.
                "請注意，所有查詢都需要提供 API Key，請從環境變數 MOENV_API_KEY 中獲取。" # Please note that all queries require an API Key, please get it from the environment variable MOENV_API_KEY.
            ),
            description="一個能夠透過 OpenAPI 規範與環境部開放資料互動的代理程式。", # An agent that can interact with MOENV open data via OpenAPI specification.
            tools=[openapi_toolset],
        )