# GitHub：版本與協作

目前 repository：`playerkousas-rgb/scoutapp`。

## 工作流程

1. 從受保護 `main` 建 feature branch。
2. 每個 commit 只做一件事，使用 Conventional Commits。
3. Push feature branch，開 Pull Request。
4. 等 GitHub Actions `test` 綠燈並完成 review。
5. squash merge；不可直接 push 或 force push `main`。

## 認證與 secret

- 使用已登入的 `git`／`gh`，不要把 Personal Access Token 寫進 repo、home file、聊天或 script。
- `.env*`、service-account JSON、private key 與本機資料由 `.gitignore` 排除。
- PR 前檢查 `git diff --check`、secret scan、完整 `pytest`。

## 回滾

程式問題可 revert merge commit，或在 Vercel Promote 上一個成功 deployment。正式資料在 Google Sheet／Drive，不應隨程式回滾或被 seed 覆寫。
