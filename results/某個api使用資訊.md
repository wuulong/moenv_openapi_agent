您: wqx_p_03 有哪些查詢條件了以下
23:40:45 - LiteLLM:INFO: utils.py:3337 -
LiteLLM completion() model= gpt-oss-120b; provider = openai
INFO:LiteLLM:
LiteLLM completion() model= gpt-oss-120b; provider = openai
INFO:__main__:Agent message: {
  "language": "zh",
  "offset": 0,
  "limit": 1
}
23:40:47 - LiteLLM:INFO: utils.py:3337 -
LiteLLM completion() model= gpt-oss-120b; provider = openai
INFO:LiteLLM:
LiteLLM completion() model= gpt-oss-120b; provider = openai
Agent: ### `wqx_p_03`（水庫水質監測資料）可供查詢的欄位（條件）

| 欄位名稱 | 說明 | 範例 |
|---|---|---|
| **siteid** | 測站代碼（每一個監測點的唯一編號） | `2095` |
| **sitename** | 測站中文名稱 | `翡翠水庫六` |
| **siteengname** | 測站英文名稱 | `Fei‑Tsui Reservoir VI` |
| **damname** | 所屬水庫名稱 | `翡翠水庫` |
| **county** | 所屬縣市 | `新北市` |
| **township** | 所屬鄉鎮市區 | `石碇區` |
| **twd97lon** | TWD97 經度（座標） | `121.6222770` |
| **twd97lat** | TWD97 緯度（座標） | `24.9374720` |
| **twd97tm2x** | TWD97 二度分帶 X 座標 | `312845.20` |
| **twd97tm2y** | TWD97 二度分帶 Y 座標 | `2758995.79` |
| **sampledate** | 取樣時間（日期＋時間） | `2025‑06‑02 10:47:00` |
| **samplelayer** | 取樣水層（如「表水」） | `表水` |
| **sampledepth** | 取樣深度（公尺） | `0.5` |
| **itemname** | 監測項目中文名稱 | `葉綠素a` |
| **itemengname** | 監測項目英文名稱 | `Chlorophyl‑A` |
| **itemengabbreviation** | 監測項目英文縮寫 | `Chl_a` |
| **itemvalue** | 監測值 | `1.3` |
| **itemunit** | 單位 | `μg/L` |
| **note** | 備註說明（可為空） | ` ` |

### 其他可使用的通用參數

| 參數 | 說明 | 範例 |
|---|---|---|
| **language** | 取得資料的語系，`zh`（中文）或 `en`（英文） | `zh` |
| **offset** | 分頁起始筆數（從第幾筆開始）| `0` |
| **limit** | 每次回傳筆數上限（最大 1000）| `100` |

---

#### 如何使用這些條件

您可以在 API 呼叫時把想篩選的欄位加入查詢字串，例如：

```
/api/v2/wqx_p_03?api_key=YOUR_KEY&damname=翡翠水庫&itemname=葉綠素a&sampledate>=2024-01-01&sampledate<=2024-12-31&limit=200
```

- `damname`、`itemname`、`county`、`sampledate` 等欄位皆支援 **等於** 或 **比較（>、>=、<、<=）** 的條件（視平台實作而定）。
- 若只需要特定測站，可直接以 `siteid` 篩選。
- `sampledate` 為完整的時間戳記，可利用日期範圍查詢。

---

如果您有特定的篩選需求（例如只查 **某座水庫**、**某測項**、**特定時間區間**），請告訴我，我會為您組合完整的 API 呼叫並回傳結果。
INFO:__main__:Current session state: {}
您