import asyncio
import os
import logging
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from datetime import datetime

# Import the agent from agent.py
from agent import MoenvOpenApiAgent

# --- 設定日誌輸出到檔案 ---
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 根據當前時間生成唯一的日誌檔案名
log_filename = datetime.now().strftime("moenv_agent_events_%Y%m%d_%H%M%S.log")
log_filepath = os.path.join(log_dir, log_filename)

# 自訂過濾器，用於阻止特定日誌訊息顯示在控制台上
class TelemetryFilter(logging.Filter):
    def filter(self, record):
        # 如果日誌訊息包含 'Event: {'，則不顯示在控制台上
        return 'Event: {' not in record.getMessage()

# 配置日誌
# 根日誌器設定為 DEBUG 級別，所有訊息都會被捕獲
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filepath, encoding='utf-8') # 所有日誌都寫入檔案
    ],
    force=True # 強制重新配置日誌器，確保我們的 FileHandler 是第一個
)

# 為控制台輸出單獨設定 StreamHandler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO) # 控制台只顯示 INFO 或更高級別的訊息
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
console_handler.addFilter(TelemetryFilter()) # 添加自訂過濾器

# 將 StreamHandler 添加到根日誌器
logging.getLogger().addHandler(console_handler)

logger = logging.getLogger() # Get the root logger


# --- Constants ---
APP_NAME = "moenv_openapi_app"
USER_ID = "test_user_123"
SESSION_ID = "moenv_openapi_session_456"

# --- Debug Switch ---
DEBUG_MODE = False # Set to True to run demonstration prompts, False for interactive mode

# --- 新增遙測日誌開關 ---
ENABLE_TELEMETRY_LOGGING = os.getenv("ENABLE_ADK_TELEMETRY", "True").lower() == "true" # 設定為 True 啟用遙測日誌，False 關閉
print(f"ENABLE_TELEMETRY_LOGGING 的實際值: {ENABLE_TELEMETRY_LOGGING}")
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
    print(f"根日誌器級別: {logging.getLogger().level}")
    print(f"檔案處理器級別: {logger.handlers[0].level}")
    # 確認處理器順序和類型
    print("日誌處理器順序和類型:")
    for i, handler in enumerate(logging.getLogger().handlers):
        print(f"  Handler {i}: {type(handler).__name__}")

    if ENABLE_TELEMETRY_LOGGING:
        print(f"所有事件遙測日誌將寫入到檔案: {log_filepath}")
        print(f"您可以使用 'tail -f {log_filepath}' 來即時監控日誌。")
    else:
        print("遙測日誌已關閉。")

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
        # --- 根據 ENABLE_TELEMETRY_LOGGING 決定是否記錄所有事件 ---
        if ENABLE_TELEMETRY_LOGGING:
            # 記錄所有事件的詳細內容到檔案
            1 and logger.info(f"Event: {event.model_dump_json(indent=2, exclude_none=True)}")
        
        if event.is_final_response() and event.content and event.content.parts:
            1 and print(f"Agent: {event.content.parts[0].text}")
        elif hasattr(event, 'tool_code'):
            # 這些日誌即使 ENABLE_TELEMETRY_LOGGING 為 False 也會顯示，因為它們是 main.py 原有的邏輯
            logger.info(f"Agent called tool: {event.tool_code.tool_name} with args: {event.tool_code.args}")
        elif hasattr(event, 'tool_response'):
            1 and logger.info(f"Tool response: {event.tool_response.response}")
        elif hasattr(event, 'content') and event.content.role == 'model':
            if event.content.parts:
                1 and logger.info(f"Agent message: {event.content.parts[0].text}")
            else:
                1 and logger.info("Agent message: (empty content parts)")
        else:
            # 對於未處理的事件類型，如果遙測日誌關閉，則會記錄較少的資訊
            if not ENABLE_TELEMETRY_LOGGING: # 避免重複記錄，如果 ENABLE_TELEMETRY_LOGGING 為 True，上面已經記錄了
                1 and logger.debug("Unhandled event type (telemetry logging is off).")

    # 強制刷新日誌緩衝區
    # 假設 FileHandler 是第一個 handler (根日誌器的第一個 handler)
    root_logger = logging.getLogger()
    if root_logger.handlers and isinstance(root_logger.handlers[0], logging.FileHandler):
        root_logger.handlers[0].flush()
        print("已刷新日誌緩衝區。")

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
    logging.shutdown()
