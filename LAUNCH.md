# 荃灣第 7 旅正式上線清單

> 目前新 Google Sheet 尚未接妥；在下列 **P0** 全部完成前，只可預覽，不可建立正式帳戶或資料。

## P0 — 必須完成

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

## P1 — 內容與私隱

- [ ] 領袖確認原有 50 題會員章題庫及遊戲內容保持不變
- [ ] 檢查公告、建議、獎品、抽卡、龍虎榜開關；不適用或未審核的功能應關閉
- [ ] 確認成員姓名、電郵及相片的收集與使用已獲適當同意
- [ ] 不在聊天、Git、URL、截圖或前端程式放 service-account JSON、API key、session token
- [ ] 領袖測試忘記密碼及一次性 reset link
- [ ] 英文／中文、手機／桌面、reduced motion、無 JavaScript 基本流程各走一次

## Vercel Dashboard 手動核對

本工作環境目前沒有 Vercel project read 權限，因此以下項目須由專案擁有人在 Dashboard 手動確認：

1. Settings → Environment Variables：Production 與 Preview 值分開；secret 只在 server-side。
2. Deployments：目前 Production deployment 指向已合併、CI 綠燈的 commit。
3. Domains：正式域名指向正確 project，HTTPS 正常。
4. Logs：啟動後沒有 Sheets 權限、JSON 解析、tab schema 或 Drive upload 錯誤。
5. Functions：沒有依賴 `/tmp` 作正式資料庫。

## 回滾

如新版本異常：Vercel → Deployments → 找上一個成功 deployment → **Promote to Production**。程式回滾不應回寫或清空 Google Sheet；回滾後再做一次讀寫驗證。
