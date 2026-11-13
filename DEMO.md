# 開發示範資料

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
