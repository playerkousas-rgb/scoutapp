# 香港童軍總會荃灣第7旅 · 平台文件（合訂本）

**7th Tsuen Wan Scout Group — Scout Platform: the complete manual**

_由 `tools/compile_docs.py` 於 2026-11-13 由各份文件自動合併；改動任何一份之後請重新執行。_

_Compiled automatically from the individual documents below. Edit the source file, then run the tool again._

---

## 目錄 · Contents

1. [總覽：這個平台是甚麼 — Overview — what this platform is](#1-總覽這個平台是甚麼--overview--what-this-platform-is)  
　<sub>`README.md`</sub>
2. [上線步驟（一次做完） — Going live, step by step](#2-上線步驟一次做完--going-live-step-by-step)  
　<sub>`LAUNCH.md`</sub>
3. [部署到 Vercel — Deploying to Vercel](#3-部署到-vercel--deploying-to-vercel)  
　<sub>`docs/05-vercel.md`</sub>
4. [試算表：所有人共用同一份資料 — Google Sheets as the shared database](#4-試算表所有人共用同一份資料--google-sheets-as-the-shared-database)  
　<sub>`docs/02-google-sheets-setup.md`</sub>
5. [電郵：重設密碼 — Email — password resets](#5-電郵重設密碼--email--password-resets)  
　<sub>`docs/03-email-setup.md`</sub>
6. [GitHub：備份與版本 — GitHub — backup and history](#6-github備份與版本--github--backup-and-history)  
　<sub>`docs/04-github.md`</sub>
7. [架構與設計 — Architecture and design](#7-架構與設計--architecture-and-design)  
　<sub>`docs/01-architecture.md`</sub>
8. [更新時，資料會不會受影響？ — Will an update touch the data?](#8-更新時資料會不會受影響--will-an-update-touch-the-data)  
　<sub>`docs/06-safe-updates.md`</sub>
9. [示範卡 — Demo card](#9-示範卡--demo-card)  
　<sub>`DEMO.md`</sub>


<a id="1-總覽這個平台是甚麼--overview--what-this-platform-is"></a>

## 1. 總覽：這個平台是甚麼 — Overview — what this platform is

<sub>來源 / source: `README.md`</sub>

**7th Tsuen Wan Scout Group · Scout Progress Platform**

這個 Flask 平台讓童軍查看獎章與任務、玩通用童軍學習遊戲、提交進度，並讓領袖管理帳戶、內容、審批與公告。

> **目前狀態：未可正式收集資料。** 新 Google Sheet／Drive 尚未接妥。Vercel 的 `/tmp` 只供短暫預覽，會被回收；正式帳戶、進度及積分必須等 `/health` 顯示 `storage: sheets` 後才建立。

### 荃灣第 7 旅客製

- 品牌：`香港童軍總會荃灣第7旅`／`7th Tsuen Wan Scout Group`
- 暫用中性 `TW7` 文字標記，沒有沿用其他旅團 Logo
- 不設小隊；登入頁直接列出所有成員姓名
- 領袖開戶、成員清單、忘記密碼及個人檔案均不要求小隊
- 沒有搬入舊旅團帳戶、進度、積分或審計紀錄
- 按用戶確認，原有 50 題會員章題庫及通用遊戲內容保持不變
- 龍虎榜及獎品預設關閉；抽卡保留原有通用內容，但已移除舊小隊卡

### 本機啟動

需要 Python 3.11+。

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env.local
python app.py
```

開啟 `http://localhost:5001`。空資料庫會先顯示「建立第一位領袖」。

#### 測試

```bash
python -m compileall -q app.py api scout tools tests
python -m pytest -q
```

### 正式資料接駁

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

### 資料與安全

- 密碼使用逐帳戶 salt 的 scrypt hash；模板只取得公開帳戶欄位。
- 登入 session 使用 `HttpOnly`、`SameSite=Lax` cookie；正式環境不接受 URL session token。
- 電郵重設連結只儲存 token hash，使用一次後失效，並撤銷舊 session。
- `.env*`、service-account JSON、憑證、本機 uploads 及備份均由 Git 忽略。
- `data/db/*.json` 是空白本機 scaffold，不是正式資料來源；`data/` 不會上傳 Vercel。
- 卡圖功能沒有在前端放 API key 或 prompt-vault token；如未設定 `GEMINI_API_KEY`，功能會安全地保持關閉。

### 圖標

`static/icons/` 依 G11 提供 9 個 PNG／ICO：favicon 16/32/ICO、Apple 180、PWA 192/512、maskable 192/512 及 OG 1200×630。主體位於中央 66% 安全區，合計體積受 260 KB 上限約束。

重新產生（需要 Pillow 與 ImageMagick）：

```bash
python tools/generate_icons.py
```

### Git 工作流程

本 repo 依真理倉原則處理：

1. feature branch 修改
2. 每個 commit 一件事，使用 Conventional Commits
3. `pytest` 與 GitHub Actions 綠燈
4. Pull Request 審核
5. squash merge 至受保護的 `main`

不可直接在 `main` 修改或用 force push 繞過檢查。

### 架構

- `app.py`：Flask app factory、共用模板 context、health、security headers
- `api/index.py`：Vercel serverless entry point
- `scout/drivers/`：本機 JSON 與 Google Sheets／Drive drivers
- `scout/routes/`：登入、童軍、領袖、個人檔案與遊戲 routes
- `content/member-badge/`：通用會員章指南、山洞題庫與故事
- `templates/`、`static/`：Jinja UI、CSS、JS、圖像及圖標
- `tests/`：權限、流程、資料持久性、遊戲與 UI 合約測試

### 真理倉回饋建議（本輪只作建議）

這個 App 值得真理倉吸收的通用做法：storage readiness health check、首次 setup gate、模板不接 password 欄、reset token hash＋session 撤銷、redeploy 資料守護測試、空庫 seed 不覆寫、自助修正 Sheets 錯誤提示、feature flags、雙語與 reduced-motion/no-JS fallback、audit log，以及部署前瀏覽器 walkthrough。旅團層級、小隊流程與遊戲內容不應硬套到所有專案。

---

<a id="2-上線步驟一次做完--going-live-step-by-step"></a>

## 2. 上線步驟（一次做完） — Going live, step by step

<sub>來源 / source: `LAUNCH.md`</sub>

> 目前新 Google Sheet 尚未接妥；在下列 **P0** 全部完成前，只可預覽，不可建立正式帳戶或資料。

### P0 — 必須完成

- [ ] 建立朋友旅團專用 Google Sheet、Google Cloud project 及 service account
- [ ] 開啟 Google Sheets API；使用上載時亦開啟 Google Drive API
- [ ] Sheet／Drive folder 已分享給 service account（Editor）
- [ ] Vercel Production 已設定 `SESSION_SECRET`、`COOKIE_SECURE=true`、`DATA_DRIVER=sheets`、`GOOGLE_SHEET_ID`、`GOOGLE_SERVICE_ACCOUNT_JSON`
- [ ] `DEMO_LOGIN=false`、`SEED_DEMO=false`、`ALLOW_URL_SESSION=false`
- [ ] Redeploy 後 `/health` 顯示 `storage: sheets`、`demo: false`、`catalog_error` 空白
- [ ] 第一位正式領袖由 `/setup` 建立；密碼不是示範值
- [ ] 真機完成：登入 → 讀 → 寫 → 登出
- [ ] Redeploy 一次，再確認帳戶及寫入資料仍存在
- [ ] `python -m pytest -q` 與 PR CI 全綠

### P1 — 內容與私隱

- [ ] 領袖確認原有 50 題會員章題庫及遊戲內容保持不變
- [ ] 檢查公告、建議、獎品、抽卡、龍虎榜開關；不適用或未審核的功能應關閉
- [ ] 確認成員姓名、電郵及相片的收集與使用已獲適當同意
- [ ] 不在聊天、Git、URL、截圖或前端程式放 service-account JSON、API key、session token
- [ ] 領袖測試忘記密碼及一次性 reset link
- [ ] 英文／中文、手機／桌面、reduced motion、無 JavaScript 基本流程各走一次

### Vercel Dashboard 手動核對

本工作環境目前沒有 Vercel project read 權限，因此以下項目須由專案擁有人在 Dashboard 手動確認：

1. Settings → Environment Variables：Production 與 Preview 值分開；secret 只在 server-side。
2. Deployments：目前 Production deployment 指向已合併、CI 綠燈的 commit。
3. Domains：正式域名指向正確 project，HTTPS 正常。
4. Logs：啟動後沒有 Sheets 權限、JSON 解析、tab schema 或 Drive upload 錯誤。
5. Functions：沒有依賴 `/tmp` 作正式資料庫。

### 回滾

如新版本異常：Vercel → Deployments → 找上一個成功 deployment → **Promote to Production**。程式回滾不應回寫或清空 Google Sheet；回滾後再做一次讀寫驗證。

---

<a id="3-部署到-vercel--deploying-to-vercel"></a>

## 3. 部署到 Vercel — Deploying to Vercel

<sub>來源 / source: `docs/05-vercel.md`</sub>

本 App 已接上 Vercel 網址，但新 Google Sheet 尚未接妥；現階段只可預覽。

### Environment Variables（Production）

| Key | 要求 |
|---|---|
| `SESSION_SECRET` | 至少 32 bytes 隨機值 |
| `COOKIE_SECURE` | `true` |
| `DATA_DRIVER` | `sheets` |
| `GOOGLE_SHEET_ID` | 荃灣第 7 旅專用 Sheet ID |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | 完整 service-account JSON，只放 server-side env |
| `GOOGLE_DRIVE_FOLDER_ID` | 選填；使用證明相片／卡圖上載時填 |
| `DEMO_LOGIN` | `false` |
| `SEED_DEMO` | `false` |
| `ALLOW_URL_SESSION` | `false` |
| `GEMINI_API_KEY` | 選填；留空即關閉卡圖生成 |

### Google 設定

1. 建立朋友旅團專用 Google Cloud project、service account 與 Sheet。
2. 開啟 Google Sheets API；如需檔案上載亦開 Drive API。
3. 把 Sheet（及 Drive folder）以 Editor 分享給 service account 的 `client_email`。
4. JSON 整份由 `{` 至 `}` 貼入 Vercel；不可 commit 或放前端。
5. Redeploy。

### 驗收

打開 `/health`，確認：

- `storage` 是 `sheets`
- `demo` 是 `false`
- `catalog_error` 空白
- badges／tasks 目錄數目正常

之後才建立正式領袖與成員。完成一次真機讀寫、登出及 Redeploy 保留資料測試。若 `storage` 是 `local`，資料位於 `/tmp` 並會消失，不能正式使用。

### 回滾

Vercel → Deployments → 上一個成功版本 → Promote to Production。回滾後重新驗證 `/health` 及一筆讀寫；不要清空 Sheet。

---

<a id="4-試算表所有人共用同一份資料--google-sheets-as-the-shared-database"></a>

## 4. 試算表：所有人共用同一份資料 — Google Sheets as the shared database

<sub>來源 / source: `docs/02-google-sheets-setup.md`</sub>

目標：**你的 Google 試算表就是資料庫**，相片存在你的 Google Drive 資料夾。
童軍在家用電話、在集會用平板、領袖在電腦登入，看到的都是同一份進度；
Vercel 重新部署、執行個體被回收，資料都不會消失。

> 已經有 Node 版用的試算表？不用重建。填同一個 Sheet ID 即可 ——
> 分頁、欄位、密碼格式完全相容。

**次序**：①②③ 在 Google 做，④ 在 Vercel 做，⑤ 回來這頁檢查。

---

### ① 建立試算表（1 分鐘）

1. 到 <https://sheets.new> 建立新試算表。
2. 命名為例如「童軍進度平台 2026」。
3. 從網址複製 ID：
   `https://docs.google.com/spreadsheets/d/`**`1AbC…xyz`**`/edit`
   → 這就是 `GOOGLE_SHEET_ID`。
4. **分頁不用自己建立** —— 程式首次連上時會自動建立 15 個分頁與標題列。

### ② 建立服務帳戶與金鑰（3 分鐘，只需一次）

1. 到 <https://console.cloud.google.com/> → 上方專案選單 → **新增專案**（例如 `scout-platform`）。
2. **API 和服務 → 程式庫** → 分別搜尋並**啟用**兩個 API：
   * **Google Sheets API**
   * **Google Drive API**（相片用；沒有它其餘功能照常）
3. **IAM 與管理 → 服務帳戶 → 建立服務帳戶**
   * 名稱：`scout-platform`；角色可留空（權限由「分享」決定）。
4. 建立後點進該服務帳戶 → **金鑰 → 新增金鑰 → JSON → 建立**，會下載一個 `.json` 檔。
5. 打開那個檔案，找到 `client_email`，樣子像：
   `scout-platform@你的專案.iam.gserviceaccount.com`
   → **複製它**，下一步要用。

### ③ 分享給「機械人」電郵（最容易漏的一步）

| 分享甚麼 | 給誰 | 權限 |
|---|---|---|
| 你的**試算表**（按「共用」） | 上一步的服務帳戶電郵 | **編輯者** |
| Drive 的**相片資料夾**（可選） | 同上 | **編輯者** |

就像分享文件給同事，只是對象是一個機械人電郵；**不是**分享給自己。
權限一定要「編輯者」，只給「檢視者」會在第一次寫入時失敗（403）。

相片資料夾：在 Drive 建立例如「童軍進度平台 — 相片」，共用給同一電郵，
然後從網址複製 `https://drive.google.com/drive/folders/`**`1XyZ…`** → 這是
`GOOGLE_DRIVE_FOLDER_ID`。不設定也可以，相片會放在服務帳戶自己的 Drive。

### ④ 在 Vercel 加入環境變數（3 分鐘）

Vercel → 你的專案 → **Settings → Environment Variables**，逐項 **Add**：

| 名稱 | 值 | 備註 |
|---|---|---|
| `DATA_DRIVER` | `sheets` | 一定要 |
| `GOOGLE_SHEET_ID` | ①的 ID | 一定要 |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | ②下載的**整個 JSON 檔案內容**（由 `{` 到 `}` 全部貼上） | 一定要 |
| `GOOGLE_DRIVE_FOLDER_ID` | ③的資料夾 ID | 要收相片才需要 |
| `SESSION_SECRET` | 隨機長字串（`openssl rand -hex 32`） | 建議 |

* 貼 JSON 時把檔案的內容**原文**貼進值欄即可，不需要改格式。
* 加好之後 → **Deployments → 最新一筆 → …→ Redeploy**（改環境變數一定要重新部署）。

### ⑤ 檢查接通了沒有

**方法一（最直接）**：登入領袖後台 → **設定**，看到

> ✅ **資料存放於 Google 試算表**（附試算表連結）

就代表成功。若看到「⚠️ 資料暫存中，會自己重置」，即代表還未接上（多數是 `DATA_DRIVER` 或步驟③的分享）。

**方法二（本機先驗一次，最省時間）**：在自己電腦用同一組環境變數跑

```bash
export DATA_DRIVER=sheets
export GOOGLE_SHEET_ID=1AbC…xyz
export GOOGLE_SERVICE_ACCOUNT_FILE=./service-account.json
python3 tools/check_sheets.py
```

它會順序檢查：環境變數 → 金鑰 → 開試算表 → 建立分頁 → 讀寫測試 → 相片上載，
最後印 `ALL GOOD` 或指出哪一步要修。**在 Vercel 之前跑一次，就不用來回部署。**

**方法三**：打開試算表本身，分頁裡應該即時看到 `users`（領袖那一列）等資料。

---

### 之後會是怎樣

- 童軍在任何裝置登入 → 讀寫的都是同一份試算表；換電話、換電腦進度都不會不見。
- 領袖後台改內容、開帳戶、審批 → 直接寫入試算表；同步到所有裝置。
- 每次部署新版本（`tools/push.sh`）**不會**影響資料：資料在試算表，不在 Vercel。

### 推送新版本會不會洗掉資料？（答案：不會）

這是設計上刻意保證的，不是巧合：

| 情況 | 會發生的事 |
|---|---|
| 空試算表第一次連上 | 程式建立獎章、任務等「目錄」一次，內容是空的 |
| 以後每次部署新版本 | 目錄**已存在就完全不碰**；只讀，不寫 |
| 領袖在後台改過的標題、題目、答案 | 永遠保留，新版本不會蓋過去 |
| 童軍的進度、積分、提交記錄 | 全部在試算表，程式只新增，不重寫 |
| 想換回舊版本 | 直接 Redeploy 舊 commit 也可以，資料完全不變 |
| 誤開了 `SEED_DEMO=true` | 若已有領袖，示範資料**不會**被植入 |

自動測試 `tests/test_redeploy_keeps_data.py` 會真的模擬一次「推送新版本＋重新部署」：
建立領袖、開童軍帳戶、完成任務、改標題與題目，再用同一份試算表重新啟動 ——
所有列數與編輯必須一字不差。所以**不需要重設，也不需要重新輸入資料**。

> 日後如果程式新增「新的獎章或新的遊戲」，下次開啟平台時會**自動補上缺少的
> 那一項**（只新增，不會動到你已有的內容）。你在後台**刪除**過的項目會記在
> 設定的 `catalog_removed`，不會自己回來。
- 建議偶爾在試算表「檔案 → 建立副本」留一份備份；也可以下載成 `.xlsx` 存檔。

### 常見問題

| 情況 | 原因 / 解法 |
|---|---|
| 領袖設定仍顯示「資料暫存中」 | `DATA_DRIVER=sheets` 未設，或未 Redeploy |
| `403 … has not been used in project … or it is disabled` | **API 未啟用**（不是共用問題）：到 console.cloud.google.com → API 和服務 → 程式庫，啟用 **Google Sheets API** 與 **Google Drive API**，等一兩分鐘後 Redeploy |
| `403 … The caller does not have permission` | 未分享試算表給服務帳戶電郵，或只給了檢視權限 |
| `GOOGLE_SHEET_ID is required` | 環境變數名稱打錯，或值有前後空白 |
| 相片打不開 | Drive 資料夾未分享給服務帳戶；程式會嘗試設為「知道連結者可檢視」 |
| 想確認是不是真的在寫入 | 一邊用人員帳戶玩遊戲，一邊開著試算表 `progress_records` 分頁看它增加 |
| 想搬回本機 | `DATA_DRIVER=local`，資料就寫到 `./data/db/*.json` |
| 想由本機轉上雲端 | 把 `data/db/*.json` 的內容貼到對應分頁（欄位相同），第一列放欄位名稱 |

### 本機測試（不用 Vercel）

```bash
export DATA_DRIVER=sheets
export GOOGLE_SHEET_ID=1AbC…xyz
export GOOGLE_SERVICE_ACCOUNT_FILE=./service-account.json
export SECRET_KEY=$(python3 -c "import secrets;print(secrets.token_hex(32))")
python3 -m flask --app app run --host 0.0.0.0 --port 5001
```

### 免費額度

Sheets API 對小型旅團（數十位童軍、每天數百次讀寫）遠遠用不完；
讀取有 15 秒快取，寫入是定點更新，不會重寫整個分頁。

### 貼上金鑰之前，先驗一次

用瀏覽器打開 `tools/check-service-account.html`，貼上 JSON 內容按「檢查」：
它會告訴你金鑰是否有效、`client_email` 要共用給哪個電郵，並指出最常見的三個貼上錯誤
（只複製一部分、貼了檔案路徑、複製時 `\n` 變成真換行）。
工具只在你的瀏覽器內運作，不會上傳任何內容。

> 程式現在也會自行處理兩種情況：整段值被引號包住，以及 `private_key` 裡的 `\n`
> 變成真換行。其餘錯誤會在 `/health` 與領袖後台 → 設定 直接寫出原因與做法。

---

<a id="5-電郵重設密碼--email--password-resets"></a>

## 5. 電郵：重設密碼 — Email — password resets

<sub>來源 / source: `docs/03-email-setup.md`</sub>

平台要寄出「重設密碼」連結，就需要一個寄信信箱。**單位的 Gmail 就可以了**（學校或總會的
帳戶通常封鎖外部登入，除非管理員另外給你應用程式密碼；一般 Gmail 最簡單）。

設定好之後的流程：

1. 童軍在密碼頁按「忘記密碼？」。
2. 平台寄一封信到他**第一次登入時填的電郵**（他不需要再打一次電郵）。
3. 他打開信裡的連結（一次性、預設 60 分鐘內有效），設定新密碼。
4. 舊密碼即時失效；舊的登入狀態也會一併登出。

---

### 一、開一個 Gmail 應用程式密碼（約 3 分鐘）

1. 用單位 Gmail 登入 <https://myaccount.google.com>。
2. **安全性** → 開啟 **兩步驗證（2-Step Verification）**。沒有開這個，下面就不會出現
   應用程式密碼。
3. 回到**安全性** → **應用程式密碼 / App passwords**。
4. 名稱隨意填（例如 `scout platform`），按**建立**。
5. Google 會給你 16 個英文字母（顯示為 4 組、每組 4 個字，例如 `abcd efgh ijkl mnop`）。
   **複製它** —— 只會顯示一次。

> 這 16 個字是給程式用的，不是你平時登入 Gmail 的密碼。如果外洩，可以隨時在同一個頁面
> 刪除再建立一個新的。

### 二、填進平台

領袖登入 → **⚙️ 設定** → **✉️ 寄信信箱（重設密碼連結）**：

| 欄位 | 填甚麼 |
|---|---|
| SMTP 主機 | `smtp.gmail.com` |
| 連接埠 | `587` |
| 加密 | `TLS (587)` |
| 寄件人 | 單位 Gmail，例如 `tw7.scout@example.com` |
| 帳號 | 同一個 Gmail |
| 應用程式密碼 | 貼上那 16 個字 |
| 重設連結有效期 | 預設 60 分鐘 |
| 平台網址 | 留空即可（見下） |

按**儲存設定**，然後在「🧪 試寄一封」填自己的電郵按**寄測試郵件**。收到就成功了。
設定頁會顯示上一次寄信的結果，失敗時會寫出原因（例如 `SMTPAuthenticationError` = 應用程式
密碼錯了）。

### 三、網址要注意的事

電郵裡的連結會用「使用者正在用的網址」。所以：

- **在自己電腦跑**（例：`http://192.168.1.20:5001`）：童軍要在同一個 Wi-Fi 才開得到。
  想指定另一個地址，就在「平台網址」填上，例如 `http://192.168.1.20:5001`。
- **真正放在伺服器**（有網域）：在「平台網址」填 `https://your-domain.example`。

### 四、沒有設定信箱時會怎樣？

不會壞，只是走另一條路：

- 童軍按「忘記密碼？」時，會看到「領袖還未設定寄信的信箱」，然後可以**即時**用電郵 +
  新密碼自行重設（這個方法無須寄信）。
- 帳號未有電郵的童軍，就只會看到「通知領袖重設密碼」的按鈕。
- 領袖後台的「🔑」鈕（代為重設）任何時候都可以用。

### 五、安全設計（供領袖了解）

- 連結裡是隨機 32 位元組的 token；平台只存它的 **SHA-256 雜湊**，資料庫被看到也不能用。
- **一次性**：設定完新密碼即失效，其他未用的連結亦一併作廢。
- **有時限**：預設 60 分鐘（可改成 5–1440 分鐘）。
- **寄出頻率有上限**：同一帳號一分鐘最多一封、一小時最多五封，避免有人用來濫發。
- 寄信失敗時，那個 token 立即作廢，不會留下「未寄出但有效」的連結。
- 電郵內容只寫姓名、連結與有效期，**永不包含密碼**。

---

<a id="6-github備份與版本--github--backup-and-history"></a>

## 6. GitHub：備份與版本 — GitHub — backup and history

<sub>來源 / source: `docs/04-github.md`</sub>

目前 repository：`playerkousas-rgb/scoutapp`。

### 工作流程

1. 從受保護 `main` 建 feature branch。
2. 每個 commit 只做一件事，使用 Conventional Commits。
3. Push feature branch，開 Pull Request。
4. 等 GitHub Actions `test` 綠燈並完成 review。
5. squash merge；不可直接 push 或 force push `main`。

### 認證與 secret

- 使用已登入的 `git`／`gh`，不要把 Personal Access Token 寫進 repo、home file、聊天或 script。
- `.env*`、service-account JSON、private key 與本機資料由 `.gitignore` 排除。
- PR 前檢查 `git diff --check`、secret scan、完整 `pytest`。

### 回滾

程式問題可 revert merge commit，或在 Vercel Promote 上一個成功 deployment。正式資料在 Google Sheet／Drive，不應隨程式回滾或被 seed 覆寫。

---

<a id="7-架構與設計--architecture-and-design"></a>

## 7. 架構與設計 — Architecture and design

<sub>來源 / source: `docs/01-architecture.md`</sub>

### 沒有 cookie 也要登入得到 (the preview iframe)

Arena 的預覽把頁面放在第三方 iframe，瀏覽器會拒絕儲存 cookie，於是
`POST /login/… → 302 /home → 302 /login`（登入後立即被踢回登入頁）。平台的處理：

```
before_request   token = ?sid=… or X-Session-Token or scout_sid cookie → g.sid → g.user
url_for (Jinja)  自動把 ?sid=… 加在所有內部連結與表單 action 上
after_request    相對轉向的 Location 也補上 ?sid=…；若 token 來自網址，順便補回 cookie
_set_session_cookie  登入後的 302 目標、以及 JSON 回應的 redirect 欄位都帶 ?sid=…
閃退訊息         flash 需要 cookie，所以在無 cookie 環境改用 ?ok= / ?err= / ?done= / ?redo=
                 由頁面自己顯示（例如 /home?ok=password 的「🎉 密碼已設定」）
```

效果：cookie 正常時完全照舊（token 只在第一次轉向出現一次）；cookie 被封鎖時整個平台
（示範登入、開發者選名、任務提交、上載、領袖審批）仍然運作，`tests/test_auth.py` 有五條
「假裝瀏覽器不收 cookie」的測試守住它。

### 第一次進入的流程 (first entry: password + email are required)

```
GET /login/scout/<patrol>            小隊選名頁（未設定密碼的名字有「第一次登入 · 免密碼」標記）
GET /login/scout/<patrol>/<user_id>  未設密碼 → sign_in() → 302 /welcome（不問密碼）
                                     有密碼 → 密碼頁；must_change_password 者輸入後同樣 302 /welcome
GET  /welcome                        必填表單：新密碼 + 確認 + 聯絡電郵（全部 required）
POST /welcome                        set_password(store, user, password, email)
                                     → 302 /home?ok=password｜錯誤 → ?err=short|mismatch|missing_email|email
@scout_required                      未完成設定 → HTML 302 /welcome；fetch/API 403 setup_required
```

設計上的三個要點：

1. **入場免費，設定必做**。`needs_first_time()` 代表「未有個人密碼或仍是領袖給的臨時密碼」，
   所以按名字（或輸入臨時密碼）都只會走到 `/welcome`。`scout_required` 對**每一個**童軍
   GET/POST 檢查它：直接輸入 `/home`、獎章頁或山洞網址都會被導回表單，介面呼叫回
   `403 setup_required`。`home_for()` 與示範捷徑同樣遵守，不能繞過。
2. **重設有三條路**。
   - **電郵連結（預設）**：密碼頁的「忘記密碼？」（`/forgot/scout/<patrol>/<id>`）只有一個
     按鈕 —— 平台寄一條一次性連結到**帳號上已有的電郵**，由他自己設定新密碼。童軍無須輸入
     電郵，所以別人猜到帳號也無法代他重設。`password_resets` 只存 token 的 SHA-256 雜湊，
     連結一次性（用過即失效，其餘同帳號連結同時作廢）、預設 60 分鐘有效，並且每次重設都會
     刪除該帳號所有 `sessions`。寄出頻率：一分鐘一封、一小時五封；寄信失敗即作廢該 token。
     設定步驟見 `docs/03-email-setup.md`。
   - **即時重設（未設定信箱時的後備）**：頁面要求輸入自己第一次登入時填的電郵，對得上就
     即時設定新密碼（`set_password` + `self_reset_password` 稽核）。離線示範與未設定 SMTP 的
     部署行這條路。
   - **領袖代辦**：領袖在帳戶版面按 🔑，清空 `password_hash` 並把 `must_change_password`
     設為 true；那位童軍下次按名字就直接進入必填表單。帳號未有電郵（領袖建立、未完成設定）
     時，自助頁只會顯示通知領袖的按鈕，沿用 `/forgot` 與 `password_reset_requests`；領袖也
     可以在帳戶頁按 ✉️ 直接把連結寄給他。
3. **Flash 與登入 cookie 不可同名**。平台自己的登入憑證用 `scout_sid`（`sessions` 分頁的
   token）。Flask 的 flash 訊息也預設叫 `scout_sid`，於是任何一次 `flash()`（例如提交任務後）
   都會覆寫登入 cookie，把童軍靜靜地登出。現在 flash 的 session cookie 改名為
   `scout_flash`（`app.py` 的 `SESSION_COOKIE_NAME`），`tests/test_auth.py` 有一條回歸測試
   專門守住這件事。

### 為甚麼是伺服器渲染

Node 版是一個 SPA：一個 HTML 檔 + JavaScript 在前端畫出所有畫面。這一版把同樣的
功能改成**每一頁有自己的網址**：

* 童軍可以加書籤、按上一頁、把 `/badges` 的連結貼給隊友 — 對小朋友重要。
* 無 JavaScript 也完全可用（學校電腦、舊平板、被封鎖的瀏覽器）；JS 只是加分項。
* 領袖可以「右鍵 → 開新分頁」同時開審批與內容。
* 搜尋引擎與列印（領袖想印進度表）自然可用。

遊戲層（圓環、路線圖、彩紙、音效）全部保留，改為「裝飾已經存在的頁面」。

### 請求的生命週期

```
request
  └─ before_request: load_user()        讀 scout_sid → sessions 分頁 → users 分頁
  └─ context_processor: inject_globals() lang · L() · settings · user(public) · TASK_TYPES
  └─ blueprint 路由
        auth_routes    登入流程（頁面）+ 表單 POST
        scout_routes   童軍頁面 + /api/*（遊戲層用）
        leader_routes  領袖後台 + /api/leader/*
  └─ 守衛: @scout_required / @leader_required / @login_required
        HTML 請求 → 302 去 /login?next=…
        fetch 請求 (X-Requested-With / Accept: json) → 401/403 JSON
  └─ Jinja 模板 (base.html → 各頁) → HTML
```

同一個 POST 端點服務兩種客戶端：瀏覽器表單（302 + flash）與遊戲層 fetch
（JSON + 事件），因此「無 JS」與「有 JS」走同一套規則，只有回應格式不同。

### 模組

| 模組 | 責任 | 不負責 |
|---|---|---|
| `scout/schema.py` | 資料表定義、欄位型別、預設設定、種子內容、任務類型 | 任何邏輯 |
| `scout/util.py` | 密碼雜湊、日期時間（Asia/Hong_Kong）、ID | 資料存取 |
| `scout/drivers/*` | 一個集合一個 list/get/insert/update/remove（+ 上載） | 規則 |
| `scout/store.py` | 驅動之上的共同層：設定合併、每位童軍的 stats 快取、上載、首次設定、示範資料、帳本重建 | 進度規則 |
| `scout/engine.py` | **所有規則**：評分、獎章自動頒發、積分帳本、連續活躍、龍虎榜、進度、建議 | HTTP |
| `scout/auth.py` | 工作階段、守衛、登入輔助 | 頁面渲染 |
| `scout/routes/*` | HTTP 進出、表單解析、審計 | 規則（一律呼叫 engine） |
| `scout/content.py` | 讀 `content/`：11 項完成指南、第 4 項題庫（答案鍵在伺服器側合併）、山洞歷險劇本 `cave.json` ＋場景圖清單 | 進度規則 |

**內容與程式分開**：獎章的「完成指南」放在 `content/member-badge/guide.json`（`n / title /
req / method / links`），第 4 項 50 題分開 `item4-question-bank.json`（題目）與
`item4-answer-key.json`（答案＋解說）。播題時合併成 `config_json.questions`，
但 `engine.strip_answers()` 在送到瀏覽器之前把 `answer` / `explain_*` 剔走 —
所以答案在頁面原始碼裡面找不到，只有交卷之後由 `scout_routes._task_context()`
以 `quiz_review` 的形式補回來（連「你的答案 vs 正確答案」）。

**山洞歷險（第 4 項的遊戲）**：`content/member-badge/cave.json` 只寫故事 —— 四段壁畫（圖片、標題、
史實、年份小籤）、每段要問哪一條題目、錯路的修正文字、出口文字。題目本身仍然只有一份，住在題庫裡；
`GET /tasks/<id>/cave` 把題目按 1. 隱藏答案、2. 每段把正解插到不同位置（`order.insert(index % len, …)`）
之後，連同全部場景圖名單寫進 `data-cave-config`。遊戲由 `static/js/cave.js` 在瀏覽器內走路
（照片換景、按圖選路、死路回頭），所以同一個遊戲在離線 `demo-preview.html` 裡面一樣玩得到。
故事內容檔換掉，遊戲就換掉 —— 程式不用改。

**單一真相**：`points_ledger`（只加不改）決定餘額；`progress_records` 決定任務狀態。
`stats` 只是快取，`Store.rebuild_stats()` 可以隨時由帳本重建（有測試驗證）。

### 資料模型（與 Node 版完全相同）

15 個集合 = 試算表的 15 個分頁：

| 分頁 | 主鍵 | 用途 |
|---|---|---|
| `users` | id | 領袖與童軍（`role` 分開；`patrol` 小隊；`avatar`） |
| `sessions` | token | 登入工作階段（`expires_at`） |
| `settings` | key | 單位設定，值為 JSON 文字 |
| `stats` | user_id | 每位童軍的餘額／任務數／獎章數／連續活躍（快取） |
| `badges` | id | 進度性獎章（`order_index` 決定路線次序，`prerequisite_badge_ids`，`guide_json` = 完成指南） |
| `tasks` | id | 任務（`type`, `points`, `pass_score`, `config_json`） |
| `progress_records` | id | 每次提交（`attempt_no`, `status`, `score`, 答案／清單／相片／反思） |
| `badge_awards` | id | 已考獲獎章 |
| `points_ledger` | id | 積分帳本（只加不改，每筆都有中英理由） |
| `rewards` / `redemptions` | id | 獎品目錄與換領紀錄（換領預設關閉） |
| `suggestions` | id | 領袖推薦卡 |
| `announcements` | id | 公告（`pinned`, `expires_at`, `audience`） |
| `password_reset_requests` | id | 忘記密碼申請（領袖處理） |
| `password_resets` | id | 已寄出的重設連結：token 雜湊、到期、用過未用（`used_at`） |
| `audit_log` | id | 操作紀錄 |

複雜值（`config_json`、`prerequisite_badge_ids`）在試算表裡是同一個儲存格的 JSON 文字。
`keyFieldFor` 等價物是 `scout/schema.py:key_field`：stats→`user_id`、settings→`key`、sessions→`token`，其餘 `id`。

### 遊戲層

* 圓環 (`ring-wrap`) 由 Jinja macro 直接輸出 SVG：沒有載入閃爍，JS 只負責由 0 動畫到目標值。
* 路線圖 (`quest-map`) 是純 HTML/CSS，節點狀態 done / current / locked 由 `progress_for` 決定。
* 彩紙 (`burst`)、音效 (`sfx`)、按壓 (`pressable`)、初次導覽 (`maybeShowTour`) 在 `effects.js`；
  導覽的「下一步」是**真的換頁**（`/badges`、`/`），所以每一頁都是正常網址。
* `prefers-reduced-motion` 之下所有動畫與粒子自動消失。

#### 會員章大冒險 (the adventure)

```
/badges/<id>              badge_intro.html  （唯一一頁：玩法 = 荒島故事 ＋ 尋寶圖 ＋ 區域卡；
                           ?started=1 加「冒險開始！」；?intro=1 是別名，同一頁）
/badges/<id>/requirements 官方 11 項完成要求（原來的完成要求頁）
POST /badges/<id>/start   開始冒險（fetch → JSON{ok, trail, credited}；無 JS → 302 ?started=1）
```

* 會員章**只有一頁**：`badge_intro.html`（玩法）。主頁方塊、獎章頁、任何舊連結都入這一頁；
  `guide_json.quest` 是否存在，決定它是「大冒險」還是「清單」；`?intro=1` 只是舊連結的別名。
  未出發的童軍在頁尾見到 **划出去 →**（POST 後回到 `?started=1`），已出發的見到 **繼續冒險**（`#map`）。
  之前那一頁關卡路線（`badge_quest.html`）已刪除，連同它的 CSS。
  所以領袖可以由 `content/member-badge/guide.json` 決定一個獎章是「遊戲」還是「清單」。
* 路線是**五個區域**，不是 11 關：`quest.areas` 每個區域有 `name_*`、`icon`、`hint_*` 與 `items`（屬該區的
  訓練綱要項目編號，合共 1–11）。`engine.stage_list()` 把區域與任務拼成路線
  （`{n, icon, name_*, hint_*, items_label_*, status, done, next, done_count, tasks[]}`；
  區域的狀態由區內項目歸納：全部完成＝已完成，有一項待批＝等領袖核實）。
* 開始冒險只是**一次過補回第 1 項要求**（`engine.credit_opening_stages()`）：
  該任務 `config_json = {"start_credited": true}`，代表「簡介會已經參加過，不需要再做一次」。
  它是 idempotent 的 — 再按一次不會多得一項。
* 區域只是官方要求的包裝：區域與項目是一對多，官方 11 項全部要在路線之內完成，沒有任何新分數。
* **玩法頁就是一個荒島故事**，不是一堆框：文案全部在 `guide.json` 的 `quest.beats_*`
  （三段：在荒島醒來 → 走過五個區域 → 沙灘上的木筏），頁面沿著一條虛線小徑渲染出來，
  最後一段是**尋寶圖**（= 你的逃生路線）：米色紙、虛線路線、指南針／山脈／波浪與紅色的 ✕
  全部是**內嵌 SVG 墨線**（不是 emoji，也不依賴字型，離線一樣），五個區域是圖上五個標記，
  路線末端是「沙灘 · 木筏」。要修改故事，改 JSON 即可。
* 背景是 `static/img/mascots/quest-island.jpg`（手繪風荒島，與登入頁同一畫風／色系）；
  滑過只會 `transform: scale()`，**沒有 filter**（登入頁的標誌正是被 filter 造成閃爍）。
* 尋寶圖使用**純 radio + label**：
  選哪一個區域（圖上哪一個標記），下面就切換為哪一張卡，全靠頁面自己的那段 `<style>`（每個區域一行由 Jinja 生成，
  放在 `{% block head %}`）——沒有 JavaScript 也能夠切換，離線檔一樣。
* 留意兩件事：(1) `effects.js` 的 `initStageBoard()` **每個板只會綁定一次**
  （`data-stage-bound`），因為離線檔每次切換 pane 都會重新執行 `init()`；
  (2) `tools/offline_demo.py` 會把每一頁 `<head>` 的 `<style>` 抽出來，合併入檔案唯一的那個
  stylesheet —— 否則尋寶圖的規則會留在 pane 裡面，離線時就不會切換卡片。
* 標記的位置是**裝飾，不是規則**：`quest.areas` 的第 1–5 個區域落在圖上寫死的五個座標
  （`.stage-map .stage-chip:nth-child(n)`），超過五個就疊在中央；≤700px 時地圖自動摺成一條直線小路。

### 與 Node 版的分工

| | Node 版 | Python 版 |
|---|---|---|
| 前端 | SPA（`app.js` 畫畫面） | Jinja 伺服器渲染，每頁一網址 |
| 遊戲層 | `public/js/effects.js` | `static/js/effects.js`（同樣功能，無 import） |
| 資料 | local JSON / Google Sheets | 相同 |
| 密碼 | scrypt | 相同（雙向互通，`test_parity.py` 驗證） |
| 離線示範 | `demo-preview.html`（單檔） | 直接跑 `python3 -m flask --app app run` |

兩者可以同時使用，指向同一個 Google 試算表。

---

<a id="8-更新時資料會不會受影響--will-an-update-touch-the-data"></a>

## 8. 更新時，資料會不會受影響？ — Will an update touch the data?

<sub>來源 / source: `docs/06-safe-updates.md`</sub>

**答案：不會。** 這份文件說明為甚麼，以及每次更新前後你可以做的事。

---

### 一句話版本

> **資料住在 Google 試算表，程式住在 GitHub／Vercel。**
> 更新＝換掉「讀寫資料的程式」，不是換掉資料。試算表一直在原位，內容一格都不會被清空。

| 甚麼東西 | 放在哪裡 | 更新時會不會變 |
|---|---|---|
| 帳戶、密碼、童軍姓名／旅團／小隊 | 試算表 `users` 分頁 | 不會 |
| 進度、提交內容、審批記錄 | 試算表 `progress_records` | 不會 |
| 積分、兌換記錄 | 試算表 `points_ledger`、`redemptions` | 不會 |
| 獎章標題、任務／遊戲題目與答案、公告、獎勵 | 試算表 `badges`、`tasks`、`announcements`、`rewards` | 不會（你改過的就是你改的） |
| 畫面、遊戲、按鈕、流程 | GitHub → Vercel（程式碼） | **會換成新版本** |
| 遊戲的預設題目（原始稿） | 程式碼裡的 `content/` | 會換；但**試算表已有內容時不會覆蓋** |

---

### 我每次更新會遵守的四條規則

1. **只加不刪。** 新功能用新的分頁或新的欄位；不會重寫、不會搬動已有的列。
2. **目錄只建立一次。** 獎章與任務目錄只在「空白試算表第一次連上」時建立，
   之後任何部署、重啟都不會再寫入 —— 你在後台改過的標題、題目、正確答案全部保留。
3. **不做「清空再匯入」式更新。** 永遠不需要你把資料重新輸入一次。
4. **每批更新都附上自動測試。** `tests/test_redeploy_keeps_data.py` 會真的模擬
   「推送新版本 ＋ Vercel 重新部署」：建領袖、開童軍、完成任務、改標題與題目，
   然後用同一份試算表重新啟動，逐項確認資料與編輯一字不差、沒有重複列。

> **新增項目**（例如日後的新獎章或新遊戲）：下次開啟平台時會自動補上缺少的
> 那一項 —— 只新增、不覆寫；你在後台刪除過的項目不會自己回來。
> 每次啟動只會補「程式有、試算表沒有」的列，仍然不會動你已有的內容。

---

### 更新流程（照著做就好）

**更新之前**

1. 在專案資料夾跑一次存檔工具（**只讀，不會改動試算表**）：
   ```bash
   python3 tools/backup_sheet.py
   ```
   它會把所有分頁存成 `backups/sheet-<日期>-<時間>/`（每個分頁一個 CSV ＋ 一份完整 JSON ＋ 指紋）。
2. 或在 Google 試算表按 **檔案 → 建立副本**，多留一份線上備份（幾秒鐘）。

**更新之後**

3. 再跑一次 `python3 tools/backup_sheet.py`：它會列出每個分頁比上次**多／少幾列**，
   例如 `＋ progress_records：18 → 24 列`。用這個就知道更新有沒有意外動到資料。
4. 三個畫面各看一次：**領袖後台總覽**、**一位童軍的獎章頁**、**排行榜**。
5. 有問題就回報我；急的話你可以自己一分鐘回到舊版（見下）。

---

### 兩層免費保險（Google 自己就有）

- **版本記錄**：試算表內 **檔案 → 版本記錄 → 查看版本記錄**。
  每個時間點的內容都留著，可以隨時還原到任何一刻。這是對付「誤刪、誤覆蓋」最有效的一招。
- **建立副本**：**檔案 → 建立副本**，多一份完整線上備份。

### 程式出問題時的一鍵回頭（Vercel）

1. 打開 Vercel → 你的專案 → **Deployments**
2. 找到上一個正常的部署 → 右邊 **⋯ → Promote to Production**（或 Rollback）
3. 一分鐘內回到舊版本。**試算表完全不變**，資料照樣在。

所以「更新 → 不合意 → 回到舊版」不會損失任何資料，只損失那一分鐘。

---

### 甚麼情況才會動到資料？

| 情況 | 會不會動資料 |
|---|---|
| 我在後台改內容、開帳戶、審批 | 會 —— 這正是它應該做的事（寫入試算表） |
| 我推送新版本、Vercel 重新部署 | 不會 |
| 領袖改密碼、童軍完成遊戲 | 不會（只在原有分頁新增／更新該列） |
| 你明確要我「刪除某個帳戶／某項記錄」 | 會 —— 我會**先跟你確認、先備份**，才動手 |
| 其他任何情況 | 不會 |

### 我對你的承諾

- 不會有任何一次更新要求你「重設平台」或「重新輸入資料」。
- 不會有更新清空任何分頁。
- 每次更新的說明我都會寫明：**這次會不會碰到資料**（絕大多數是「不會」）。
- 如果我認為某個改動有機會影響資料，我會先告訴你風險與備份方法，等你同意才做。

---

### 給未來的自己：更新清單

- [ ] 更新前跑 `python3 tools/backup_sheet.py`（或建立副本）
- [ ] 推送新版本 → 等 Vercel 部署完成（網址不變）
- [ ] 更新後再跑一次存檔工具，看增減是否合理
- [ ] 走一次：領袖登入 → 童軍登入 → 開一個遊戲 → 排行榜
- [ ] 有異常：Vercel Rollback，再回頭查

---

### 不小心刪了內建的遊戲？（2026-10-17 新增）

領袖在 內容 頁按下垃圾桶把**石室（第 4 項）或渡口（第 5 項）**刪走的話，同一頁上方有一張
「🔧 修復遊戲與缺少的項目」卡：

| 按鈕 | 作用 | 會不會影響資料 |
|---|---|---|
| 🔧 還原內建遊戲（石室、渡口） | 清走「已刪除」記號、重建缺少的任務、重新接好第 1／2 區 | **只新增**；重建時會沿用舊記錄的 id，童軍已完成的記錄保留 |
| ↺ 還原所有內建項目 | 連其他獎章的示範任務（M01…、T-…）也一次帶回 | 同上；你自己建立的內容、自己改過的區域安排一律不動 |

- 卡上會直接寫出缺少了甚麼（例如「缺少任務 M05 · 第 2 區未接好」，或「M05 的內容被清空了」），齊全時顯示 ✓。
- **你自己按垃圾桶刪掉的任務不算「缺少」**：卡上只會一行列出「你已刪除 M07、M08…（不計入）」，旁邊顯示 14 / 14，並不會催你還原。只有「沒有刪除記錄卻不見了」（例如直接在試算表刪掉一行）或兩個內建遊戲（石室、渡口）不見了，才會出警告。
- 「內容被清空」是指任務列還在、但題目／設定空掉：修復只會填回**真的空了**的欄位，你改過的題目不會被覆蓋。
- 內建遊戲（M04、M05）與會員章本身**現在不能刪除**：要換走某一區的遊戲，請在該區改派另一項任務。
- 還原後按 F5 重新載入，第 1、2 區就會恢復原狀；已在該遊戲完成的童軍仍然是「已完成」。

---

### 壁畫與遊戲插圖，放在哪裡？（改圖改字不用碰試算表）

山洞的壁畫、教學牌與遊戲插圖，全部住在程式碼的 `content/member-badge/cave.json`
（文字）與 `static/img/quest/cave/`（圖片），**更新版本就會生效，不會動到試算表**。

| 想改 | 改哪裡 |
|---|---|
| 壁畫上的字（導言、時間線、資料欄、記憶提示） | `content/member-badge/cave.json` 的 `groups[n].wall` |
| 壁畫圖片 | 換掉 `static/img/quest/cave/wall-*.jpg`（同名即可） |
| 題目、選項、正確答案 | 領袖後台 → 🕯️ 編輯題目與答案（寫入試算表的 `tasks` 分頁） |
| 遊戲內的按鈕文字 | `content/member-badge/cave.json` 的 `labels` |

更新壁畫時，圖片、教學文字、題目與解說要一起核對。旅團人物、區會、旅巾及旅慶等專屬資料必須先由領袖核實；種子只在**首次建立**時寫入，所以領袖已在平台改過的答案不會被覆蓋。

---

### 山洞的成績怎樣算？（2026-10-17 起）

走出洞口時，成績以**百分比**顯示，不再只是「78 分」：

   80% — 50 題中第一次就答對 40 題
   全程共作答 87 次，其中 37 次答錯。上面的百分比只看第一次作答 —— 起初多錯幾題，百分比就會低一些。

- **百分比＝第一次作答就答對的題數 ÷ 50。** 答錯後重試、被死路送回壁畫再答，
  都**不會**把已錯的第一答改回正確；起初多錯幾題，最終百分比就低一些。
- **第二次數字**是全程作答次數與答錯次數（含重試）—— 想讓童軍知道「錯了 37 次」就看這裡。
- 進度記錄（試算表 `progress_records` 的 `score`）仍然保存第一次作答的百分比，
  領袖在後台看到的也一樣。
- 通關不受百分比影響：走完 50 題即完成第 4 項。

相關文件：`docs/02-google-sheets-setup.md`（試算表接線）、`docs/05-vercel.md`（部署與上線清單）。

---

### 遊戲 2（渡口）與遊戲 3（步操場）的考核：領袖在帳戶按「批准」（2026-11-10 起）

第 5、6 項分**兩半**完成，**童軍不再輸入任何代碼**：

1. **玩完遊戲**：渡口三關木板全部鋪好，紀錄為 `crossed`（已過橋）；步操訓練場兩節全部通過，
   紀錄為 `studied`（已學完）。這一步只證明遊戲玩完，**未算完成**：分數、徽章進度、
   「已完成」都不會出現。
2. **領袖考核**：童軍找領袖**背誦**銘言、誓詞、規律（遊戲 2）或**親身做出**步操動作與集隊手號
   （遊戲 3）；領袖在自己的帳戶按**批准**，第 5／6 項才算完成 —— 分數、積分、
   徽章進度在這一步一次過發放，童軍的任務頁與會員章頁面即時變成 ✓。
   - 批核位置：**領袖後台 → 審批**。已完成的遊戲排在最前（銅色左邊），
     標籤「🎮 已完成遊戲 · 等考核」，卡上列出要考核的項目；
     按「✅ 批准並加分」即完成（積分可即時調整）。
   - 「稍後再審」不會把已完成的遊戲變回一般提交；「退回」則讓童軍重玩，
     重玩會另開一筆紀錄，不會重複派分。
   - 未玩完遊戲不能直接批准：一般提交（`POST /tasks/<id>/submit`）對這兩項會回 403，
     一定要先有 `crossed`／`studied` 紀錄。
- **遊戲內的考核卡**：「⏳ 已提交 · 等領袖批准」＋「🔄 重新檢查」；卡片每 20 秒自己問一次伺服器
  （`GET /tasks/<id>/status`），領袖一按批准，卡片自動變成「領袖批准了 ✓」。
  也可以先去玩下一個遊戲 —— 批准之後回來就見到 ✓。
- **狀態字**：地圖與綱要頁一律顯示「⏳ 已提交 · 等領袖批准」；完成後是「✓ 領袖批准 · 已完成」。
- 考核卡的文字（要背甚麼、要講解甚麼）在 `content/member-badge/river.json` 與
  `drill.json` 的 `assess` 一節；舊部署的任務說明由啟動時的 `refresh_game_copy()`
  換成新版本（只換未改動過的原始種子句，領袖改過的文字不會被覆蓋）。
- **離線示範**（`demo-preview.html`／`bridge-preview.html`）沒有領袖帳戶，
  考核卡上有一粒清楚標明「示範：模擬領袖批准」的按鈕代替。
- 舊的代碼路由（`/tasks/<id>/bridge-code`、`/drill-code`）與 `bridge_assess_code`、
  `drill_assess_code` 設定已移除。
- **龍虎榜不受批准影響**：玩完遊戲（`crossed`／`studied`）即時上「會員章 · 各遊戲」榜，
  不必等領袖批准。批准只決定第 5／6 項是否完成、發不發分與積分。
  榜上未批准的童軍每個遊戲顯示「等批准」小標，名次照計。
- **各遊戲各有各的量尺**：遊戲 1 看答對百分比（高分先）；遊戲 2、3 看完成時間（快者先），
  時間由遊戲頁自己計（`elapsed_ms`），存在該筆記錄 `answers_json` 的 `_ms`；
  8 秒以下或 6 小時以上當作沒有計時 —— 仍然見到玩完，但榜上不排名次。舊記錄沒有時間，
  一樣列在榜尾（「沒有計時」）。
---

### 尋寶圖的光跟人走（2026-10-18 起）

地圖上**大張的亮卡（第一站）只會站在童軍的下一站**：完成了的站會退回普通小卡（打勾、變淡），
「▶ 下一站 · 你在這裡」的金框亮卡與童軍頭像會移到下一個要玩的遊戲。

- 未開始：第 1 區（山洞）是大卡「第一站 · 從這裡開始」——跟以前一樣。
- 完成 2 個遊戲後：第 1、2 區是打了勾的小卡，第 3 區是亮卡（附「▶ 下一站」），不會再停在山洞。
- 過了橋等批准：亮卡一樣移到第 3 區，第 2 區顯示 ⏳ 與「看批准狀態」的門。
- **地圖卡不再顯示遊戲簡介**（2026-10-18）：每個地點只剩編號、名稱、遊戲名與狀態，
  遊戲的內容走進去自然會知道。領袖在後台填的簡介仍會儲存（第 3–5 區將來用得着），
  只是地圖不再展示。

---

### 尋寶圖改成真正的島嶼場景（2026-10-18 起；同日固定比例）

地圖不再只是一張紙加插圖，而是**畫出了一座島**：四周是海，島上有一條河由北灣流向南海，
五個地點沿島劃成一圈，地形跟地名相配——

- **第 1 站 叢林深處**（西北）：樹木塗鴉＋叢林色塊；**第 2 站 迷霧小徑**（北）：河流經過，
  河上有小板橋（遊戲 2 的渡口），水面飄着霧；**第 3 站 石壁山嶺**（東）：山形筆畫； 
  **第 4 站 溪谷旗桿**（南）：溪流從山嶺流入河谷，谷裏豎了旗桿；**第 5 站 臨海山崗**（西南）：
  崖壁筆畫臨着西岸——**沙灘·木筏就在旁邊的岸上**，走完第 5 站即到逃生點。
- 五站走線為一圈，站距實測 31–37%，均勻用盡全圖；虛線由**站與站的正確座標**計算生成，
  每一段都穿過卡片中心點。
- 營地（營帳＋營火）移到島中央、河流以東；太陽、兩群海鳥、海浪、棕櫚、名牌（右下角）
  與指南針（右上角）各歸其位。
- 實測 3 個進度狀態 × 6 種視窗闊度（851–1440px）：卡×卡、卡×木筏、卡×全部塗鴉**零重疊**。
- 手機版（≤850px）不變：場景收起，五張卡對齊成直向行程。

- 新增 6 個同款墨風塗鴉：太陽、兩群飛鳥、營帳、營火、小樹——手機（≤850px）同樣收起。
- 走線虛線（trail）跟隨新站位重畫，路徑穿過每個站的中心點。
- 亮卡（下一站）與頭像照舊跟 `.is-here` 走，站 1 的 `stage-chip-first` 樣式不變。
- 幾何用 `tools/checks/` 的量測方式覆核過三個狀態：未開始（大卡在左上）、過了山洞（亮卡到第 2 站）、
  完成 2 個遊戲（亮卡到第 3 站）——卡與卡、卡與塗鴉之間均無重疊。

---

### 尋寶圖固定比例＋故事便條半透明（2026-10-18 起）

- **地圖不再隨視窗拉寬**：桌面版尋寶圖高度固定 455px、寬度上限 910px
  （剛好 2:1）。視窗再寬，地圖都保持 910×455 不變，置中放在紙底上，
  不會再變成一條過寬的長條。已於 851–1440px 六種視窗 × 新手/完成兩站
  兩種狀態實測：五張站卡、沙灘標籤與全部塗鴉零重疊。
- 開場故事卡 3 的尋寶圖同樣以 2:1 置中顯示（手機直向維持原有填滿）。
- **故事便條半透明＋文字自動適應**：羊皮紙便條約 7 成透明＋ 4.5px 背景模糊
  （`backdrop-filter`），童軍可以清楚看見背後的插畫。文字顏色會**自動適應**
  背景亮度（瀏覽器量度便條後面的畫面）：背景暗（船難、山洞、迷霧、山嶺、
  溪谷）→ 文字轉為米白「燈光色」＋深色玻璃底；背景亮（尋寶圖紙、沙灘、
  日出）→ 保持深墨色。領袖日後換插畫也會自動跟著變，不用改任何設定。

### 手機版五站對齊（2026-10-18 起）

窄螢幕（≤850px）的直向行程本來有一個不一致：四個普通站是**齊左的整行卡片**，
唯獨「下一站」的亮卡保留了置中的窄卡樣式，看起來像浮在中間。

- 現在**五張卡同一個形狀**：同樣齊左、同樣闊度（跟隨螢幕）、同樣的行內排版（編號在左、
  名稱遊戲在右），一站一行，順序 1→5。
- 「下一站」照舊只有一個：金框、呼吸光暈（`now-pulse`）、「▶ 下一站 · 你在這裡」眉標
  與童軍頭像都留在下一站的卡上；完成了的站照舊打勾變淡。
- 實測（390px 闊）：五卡同一左緣、同一右緣、無橫向溢出；未開始與完成 2 個遊戲兩個狀態
  各只有一張亮卡。

---

### 靜態檔案加入版本號（2026-10-18 起）

`styles.css` 與所有 JS 網址現在帶有版本參數（`?v=檔案修改時間`，如
`styles.css?v=1792319780`）：檔案一改，網址就跟住改。

- 解決的問題：瀏覽器或代理伺服器把舊 CSS留在快取，更新上線後用戶仍看到舊樣式。
- 之後每次更新樣式或腳本，用戶**一刷新就拿到新檔**，不用清快取。
- 離線演示版不受影響（CSS本來就內聯在單一 HTML 內）。

### 開場故事：第一次玩會員章的八張圖卡（2026-10-18 起，同日改良）

首次打開會員章的童軍，會在**頁面內**看到開場故事：九張圖卡，每張一張
大圖配一段清楚的文字，只靠「下一張／上一張」按鈕推進，**全程不用捲動**；
點點可跳去任何一張，「跳過故事」或看完最後一張的「出發」就結束。故事
放在頁面內而不是全螢幕蓋版，所以**頂欄的捷徑一直按得到**——想離開，
點頂欄就可以走。

- 每張卡的文字以**羊皮紙便條**疊在圖上（kicker 小標＋大標＋內文），
  配雙線墨框、頁碼（3 / 8）與指南針標記，像翻故事書。
- 卡 1–2：船撞礁石、在荒島醒來（新插畫，跟遊戲同一套水墨水彩風格）。
- 卡 3：**真的荒島尋寶圖**——與會員章頁面同一張地圖（島、河、虛線、
  山嶺、旗桿、沙灘木筏都在），上面加了五個編號圓點標示路線順序，
  第 1 站紅色標「起點」。
- 卡 4–8：五個地點**逐個一站一卡**介紹（第 1 站山洞用遊戲內的洞口圖、
  第 2 站渡口用河岸圖；第 3 站石壁山嶺、第 4 站溪谷旗桿、第 5 站臨海
  山崗各一張新插畫）。
- 卡 9（目標頁）：乘木筏離開荒島的日出場景為底，會員章以**小圓徽**
  （約 96px，手機 76px）坐在羊皮紙便條上，配「五個遊戲全部完成，就
  可以乘木筏離開」→ **出發按鈕直入第 1 站的遊戲 1**。

離開故事（跳過／出發）會自動記下「已開始冒險」（沿用舊的 `start_quest`
記錄，用 `sendBeacon` 送出，離開頁面也照樣寫入）。

**之後再回來**：會員章頁面不再顯示頂部的荒島故事描述，直接開在
「你的逃生路線」地圖——一行 slim 標題（獎章名稱＋🌿 X/5 區域 · 🎮 X/5
遊戲的進度條）＋地圖＋底部按鈕。想重看故事，按 slim 標題的
「重看故事」連結（`?intro=1`）即可。

技術細節（領袖不用記）：

- 故事文字與圖片路徑放在 `content/member-badge/guide.json` 的
  `quest.intro_slides`；路由以**內容檔為預設、資料庫為準**合併，所以
  已存在的獎章不用重做就會出現故事。想改字可以直接改這個檔。
- 尋寶圖的墨繪部分抽成共用檔 `templates/scout/_map_art.html`，頁面
  地圖與故事卡 3 用同一份；故事卡上以五個編號圓點（`story-stops`）
  代替站卡。
- 五張新插畫：`static/img/quest/intro/` 下的 `shipwreck.jpg`（船難）、
  `ridge.jpg`（第 3 站石壁山嶺）、`valley.jpg`（第 4 站溪谷旗桿）、
  `bluff-raft.jpg`（第 5 站山崗木筏）、`sail-away.jpg`（目標頁啟航）。
- 故事框高度以 `calc(100dvh - 216px)`（手機 224px）對齊頂欄以下
  整屏，已於 1180/1366/820/390/360px 五種螢幕實測零捲動。
- 離線演示（`demo-preview.html`）同樣有整個故事：`quest-intro` pane 是
  首次的圖卡，跳過後的所有入口改去 `quest-map` pane（你的逃生路線），
  頂欄的回家捷徑在離線版一樣按得到。

---

<a id="9-示範卡--demo-card"></a>

## 9. 示範卡 — Demo card

<sub>來源 / source: `DEMO.md`</sub>

正式部署不會建立示範帳戶。只有在本機明確設定以下兩項時，才會載入開發 fixture：

```bash
DEMO_LOGIN=true SEED_DEMO=true python app.py
```

Fixture 仍可包含歷史相容流程（例如有小隊的舊資料），用途是驗證舊 URL 及資料格式不會在升級時損壞；它不是荃灣第 7 旅正式名單，也不會由 `.vercelignore` 上傳至 Vercel。

正式驗收應使用一個全新臨時資料目錄，確認：

1. `/setup` 建立第一位領袖。
2. 領袖毋須選小隊即可建立成員。
3. `/login` 直接列出所有成員姓名。
4. 首次登入設定密碼與電郵。
5. 完成個人檔案、遊戲、提交及領袖審批。
6. 使用 Google Sheets 測試時，Redeploy 後資料仍存在。

示範密碼只屬自動化 fixture，絕不可用作正式領袖或成員密碼。

---
