## 做咗乜 / What changed

## 規則與風險 / Rules and risks
- [ ] 身份或權限有沒有改？
- [ ] 有沒有新增環境變數？`.env.example` 已同步？
- [ ] 有沒有新增寫入 action？授權、驗證與測試已加？
- [ ] 有沒有新增 secret？只放 server-side env？
- [ ] 有沒有包含舊旅團、示範帳戶或個人資料？

## 測試 / Tests
- [ ] `python -m pytest -q`
- [ ] `/health` 顯示 `storage: sheets`
- [ ] 真機走一次：登入 → 讀 → 寫 → 登出

## 部署與回滾 / Deploy and rollback
- Deployment URL:
- Rollback: Vercel → Deployments → 上一個成功版本 → Promote to Production
