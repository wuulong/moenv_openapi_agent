# 環境部 OpenAPI 代理程式規範

## 目的
本文件旨在說明 `moenv_openapi_agent` 這個 ADK 範例代理程式的設計，其目的是展示如何將真實世界的 OpenAPI 規範（來自台灣環境部）與 Agent Development Kit (ADK) 整合。最終目標是建立一個能夠**使用自然語言查詢環境部開放資料**的代理程式。

## 代理程式名稱
`moenv_openapi_agent`

## 位置
`my_samples/moenv_openapi_agent/`

## 核心組件

### 1. `agent.py`
此檔案將定義 `LlmAgent` 並整合 OpenAPI 工具。

#### 代理程式定義
`LlmAgent` 將配置以下內容：
*   **名稱：** `moenv_openapi_agent`
*   **模型：** `LiteLlm` (透過 `.env` 檔案配置 API 金鑰/端點)
*   **指令：** 一份詳盡的指令，指導代理程式根據使用者的自然語言查詢，判斷何時以及如何使用環境部 API 工具。它將強調需要 API 金鑰。
*   **工具：** 一個從 `moenv_openapi.yaml` 載入的 `OpenAPIToolset` 實例。

#### OpenAPI 工具集整合
*   `agent.py` 將直接讀取 `moenv_openapi.yaml` 檔案內容。
*   將使用 `moenv_openapi.yaml` 的內容實例化一個 `OpenAPIToolset`。
*   環境部 API 所需的 `api_key` 將從環境變數 (`MOENV_API_KEY`) 傳遞給 `OpenAPIToolset`。

### 2. `main.py`
此檔案將包含運行 `moenv_openapi_agent` 的設定。

*   **匯入：** 必要的 ADK 組件 (`LlmAgent`, `Runner`, `InMemorySessionService`, `LiteLlm`, `dotenv`)。
*   **環境設定：** 從 `.env` 載入環境變數。
*   **代理程式實例化：** 建立 `moenv_openapi_agent` 的實例，並從環境變數傳遞模型配置。
*   **運行器設定：** 使用代理程式和 `InMemorySessionService` 初始化 `Runner`。
*   **互動迴圈：** 一個非同步函數，用於模擬使用者互動，向代理程式發送訊息並列印其回應。這將包括旨在觸發環境部 API 工具的範例查詢。

### 3. `moenv_openapi.yaml`
此檔案包含環境部環境資料開放平台開放資料 API 的 OpenAPI 3.0.0 規範。它定義了各種用於環境資料的 GET 端點，每個端點都需要一個 `api_key` 查詢參數。

### 4. `.env` 配置
`main.py` 將預期在 `my_samples/moenv_openapi_agent/` 目錄中存在一個 `.env` 檔案，其中包含以下配置：

```
LITELLM_MODEL_NAME="您偏好的 litellm 模型" # 例如：openai/gpt-3.5-turbo, gemini-pro
LITELLM_API_KEY="您的 litellm api 金鑰"
MOENV_API_KEY="您的環境部 api 金鑰" # 請從 https://data.moenv.gov.tw/api-term 取得
```

## 使用方式
1.  將 `moenv_openapi.yaml` 檔案放置在代理程式的目錄中。
2.  建立一個 `.env` 檔案，其中包含所需的 API 金鑰和模型名稱。
3.  運行 `main.py`。
4.  透過提出可使用環境部 API 回答的問題來與代理程式互動（例如：「查詢酸雨監測值」）。

## 驗證
如果滿足以下條件，則該範例將被視為成功：
*   代理程式可以初始化並運行而沒有錯誤。
*   環境部 API 工具在收到適當的使用者查詢後，能被代理程式成功調用。
*   代理程式的回應能反映從環境部 API 檢索到的資料。
