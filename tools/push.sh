#!/usr/bin/env bash
set -euo pipefail

branch="$(git branch --show-current)"
case "$branch" in
  main|master) echo "拒絕直接 push $branch；請使用 feature branch + PR。" >&2; exit 1 ;;
esac

python3 -m pytest -q
git diff --check
git push origin "$branch"
echo "已 push $branch；下一步用 gh pr create 開 Pull Request。"
