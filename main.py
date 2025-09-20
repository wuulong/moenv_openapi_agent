import asyncio
import os
import logging
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import the agent from agent.py
from agent import MoenvOpenApiAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Constants ---
APP_NAME = "moenv_openapi_app"
USER_ID = "test_user_123"
SESSION_ID = "moenv_openapi_session_456"

# --- Debug Switch ---
DEBUG_MODE = False # Set to True to run demonstration prompts, False for interactive mode

# --- Demonstration Prompts (Traditional Chinese) ---
DEMO_PROMPTS = [
    "請給我空氣品質預報資料。", # /aqf_p_01
    "查詢全國細懸浮微粒手動監測資料。", # /aqx_p_10
    "幫我找一下環境部職員官等性別統計資料。", # /epao_p_02
    "有哪些關於環境教育的活動數量？", # /eedu_p_10
    "請查詢酸雨監測值（歷史資料）。", # /acidr_p_01
]

# --- Main execution function ---
async def main():
    # Load environment variables from .env file
    load_dotenv()

    # --- Setup LiteLLM Model ---
    # Get model name, API base, and API key from environment variables
    model_name = os.getenv("LITELLM_MODEL_NAME", "openai/gpt-3.5-turbo")
    api_base = os.getenv("LITELLM_API_BASE")
    api_key = os.getenv("LITELLM_API_KEY")

    logger.info(f"Using LiteLLM model: {model_name}")
    if api_base:
        logger.info(f"LiteLLM API Base: {api_base}")
    if api_key:
        logger.info("LiteLLM API Key: (set)") # Avoid logging sensitive info

    # --- Agent and Runner Setup ---
    agent = MoenvOpenApiAgent(model_name=model_name, api_base=api_base, api_key=api_key)
    session_service = InMemorySessionService()

    # Create a session
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    logger.info("Agent and Runner initialized.")

    if DEBUG_MODE:
        print("\n--- 除錯模式：正在運行展示提示 ---")
        for i, prompt in enumerate(DEMO_PROMPTS):
            print(f"\n--- 演示 {i+1}/{len(DEMO_PROMPTS)} ---")
            print(f"您: {prompt}")
            await process_user_input(runner, USER_ID, SESSION_ID, prompt, session_service)
        print("\n--- 除錯模式：演示完成 ---")
    else:
        print("\n--- 環境部 OpenAPI 代理程式已就緒 (互動模式) ---")
        print("輸入您的查詢。輸入 'exit' 退出。")
        print("---------------------------------------------------\
")

        while True:
            user_input = input("您: ")
            if user_input.lower() == "exit":
                break
            await process_user_input(runner, USER_ID, SESSION_ID, user_input, session_service)

    logger.info("Interaction loop finished.")

async def process_user_input(runner: Runner, user_id: str, session_id: str, user_input: str, session_service: InMemorySessionService):
    """Helper function to process user input and print agent responses."""
    content = types.Content(role="user", parts=[types.Part(text=user_input)])
    events = runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    )

    # Process and print agent's responses
    async for event in events:
        if event.is_final_response() and event.content and event.content.parts:
            print(f"Agent: {event.content.parts[0].text}")
        elif hasattr(event, 'tool_code'):
            logger.info(f"Agent called tool: {event.tool_code.tool_name} with args: {event.tool_code.args}")
        elif hasattr(event, 'tool_response'):
            logger.info(f"Tool response: {event.tool_response.response}")
        elif hasattr(event, 'content') and event.content.role == 'model':
            logger.info(f"Agent message: {event.content.parts[0].text}")
        else:
            logger.debug("Unhandled event type.")

    # Print current session state for debugging
    current_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )
    if current_session:
        logger.info(f"Current session state: {current_session.state}")

if __name__ == "__main__":
    asyncio.run(main())
