# 部署到 Vercel

本 App 已接上 Vercel 網址，但新 Google Sheet 尚未接妥；現階段只可預覽。

## Environment Variables（Production）

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

## Google 設定

1. 建立朋友旅團專用 Google Cloud project、service account 與 Sheet。
2. 開啟 Google Sheets API；如需檔案上載亦開 Drive API。
3. 把 Sheet（及 Drive folder）以 Editor 分享給 service account 的 `client_email`。
4. JSON 整份由 `{` 至 `}` 貼入 Vercel；不可 commit 或放前端。
5. Redeploy。

## 驗收

打開 `/health`，確認：

- `storage` 是 `sheets`
- `demo` 是 `false`
- `catalog_error` 空白
- badges／tasks 目錄數目正常

之後才建立正式領袖與成員。完成一次真機讀寫、登出及 Redeploy 保留資料測試。若 `storage` 是 `local`，資料位於 `/tmp` 並會消失，不能正式使用。

## 回滾

Vercel → Deployments → 上一個成功版本 → Promote to Production。回滾後重新驗證 `/health` 及一筆讀寫；不要清空 Sheet。
