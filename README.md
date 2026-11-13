# 香港童軍總會荃灣第7旅童軍進度平台

**7th Tsuen Wan Scout Group · Scout Progress Platform**

這個 Flask 平台讓童軍查看獎章與任務、玩通用童軍學習遊戲、提交進度，並讓領袖管理帳戶、內容、審批與公告。

> **目前狀態：未可正式收集資料。** 新 Google Sheet／Drive 尚未接妥。Vercel 的 `/tmp` 只供短暫預覽，會被回收；正式帳戶、進度及積分必須等 `/health` 顯示 `storage: sheets` 後才建立。

## 荃灣第 7 旅客製

- 品牌：`香港童軍總會荃灣第7旅`／`7th Tsuen Wan Scout Group`
- 暫用中性 `TW7` 文字標記，沒有沿用其他旅團 Logo
- 不設小隊；登入頁直接列出所有成員姓名
- 領袖開戶、成員清單、忘記密碼及個人檔案均不要求小隊
- 沒有搬入舊旅團帳戶、進度、積分或審計紀錄
- 按用戶確認，原有 50 題會員章題庫及通用遊戲內容保持不變
- 龍虎榜及獎品預設關閉；抽卡保留原有通用內容，但已移除舊小隊卡

## 本機啟動

需要 Python 3.11+。

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env.local
python app.py
```

開啟 `http://localhost:5001`。空資料庫會先顯示「建立第一位領袖」。

### 測試

```bash
python -m compileall -q app.py api scout tools tests
python -m pytest -q
```

## 正式資料接駁

在朋友旅團專用的 Google Cloud／Google Sheet 準備完成後，於 Vercel **Production** 環境設定：

```dotenv
SESSION_SECRET=<至少 32 bytes 的隨機值>
COOKIE_SECURE=true
DATA_DRIVER=sheets
GOOGLE_SHEET_ID=<朋友旅團專用 Sheet ID>
GOOGLE_SERVICE_ACCOUNT_JSON=<完整 service-account JSON>
GOOGLE_DRIVE_FOLDER_ID=<選填；證明相片及卡圖使用>
DEMO_LOGIN=false
SEED_DEMO=false
ALLOW_URL_SESSION=false
```

1. 開啟 Google Sheets API；需要檔案上載時亦開啟 Google Drive API。
2. 把 Sheet（及選填 Drive folder）以 Editor 分享給 service account 電郵。
3. 在 Vercel 儲存環境變數並 Redeploy。
4. 開啟 `/health`，確認 `storage` 是 `sheets`、`demo` 是 `false`、`catalog_error` 為空。
5. 才建立正式領袖與成員帳戶，並以真機走一次：登入 → 讀取 → 寫入 → 登出 → Redeploy → 再登入確認資料仍在。

詳細上線檢查見 [`LAUNCH.md`](LAUNCH.md)。

## 資料與安全

- 密碼使用逐帳戶 salt 的 scrypt hash；模板只取得公開帳戶欄位。
- 登入 session 使用 `HttpOnly`、`SameSite=Lax` cookie；正式環境不接受 URL session token。
- 電郵重設連結只儲存 token hash，使用一次後失效，並撤銷舊 session。
- `.env*`、service-account JSON、憑證、本機 uploads 及備份均由 Git 忽略。
- `data/db/*.json` 是空白本機 scaffold，不是正式資料來源；`data/` 不會上傳 Vercel。
- 卡圖功能沒有在前端放 API key 或 prompt-vault token；如未設定 `GEMINI_API_KEY`，功能會安全地保持關閉。

## 圖標

`static/icons/` 依 G11 提供 9 個 PNG／ICO：favicon 16/32/ICO、Apple 180、PWA 192/512、maskable 192/512 及 OG 1200×630。主體位於中央 66% 安全區，合計體積受 260 KB 上限約束。

重新產生（需要 Pillow 與 ImageMagick）：

```bash
python tools/generate_icons.py
```

## Git 工作流程

本 repo 依真理倉原則處理：

1. feature branch 修改
2. 每個 commit 一件事，使用 Conventional Commits
3. `pytest` 與 GitHub Actions 綠燈
4. Pull Request 審核
5. squash merge 至受保護的 `main`

不可直接在 `main` 修改或用 force push 繞過檢查。

## 架構

- `app.py`：Flask app factory、共用模板 context、health、security headers
- `api/index.py`：Vercel serverless entry point
- `scout/drivers/`：本機 JSON 與 Google Sheets／Drive drivers
- `scout/routes/`：登入、童軍、領袖、個人檔案與遊戲 routes
- `content/member-badge/`：通用會員章指南、山洞題庫與故事
- `templates/`、`static/`：Jinja UI、CSS、JS、圖像及圖標
- `tests/`：權限、流程、資料持久性、遊戲與 UI 合約測試

## 真理倉回饋建議（本輪只作建議）

這個 App 值得真理倉吸收的通用做法：storage readiness health check、首次 setup gate、模板不接 password 欄、reset token hash＋session 撤銷、redeploy 資料守護測試、空庫 seed 不覆寫、自助修正 Sheets 錯誤提示、feature flags、雙語與 reduced-motion/no-JS fallback、audit log，以及部署前瀏覽器 walkthrough。旅團層級、小隊流程與遊戲內容不應硬套到所有專案。
