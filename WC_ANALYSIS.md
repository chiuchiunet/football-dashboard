# World Cup Dashboard Comparison Feature - 檢討

## 問題同解決

### 1. Collapsible 加親就壞 (第一round)
- **原因**: `<details>` tag 包錯範圍，matches render 咗出啲
- **解決**: 放棄 collapsible，keep 乾淨 version
- **教訓**: 改 structure 前要确保 HTML valid

### 2. Badge 唔 show 實際比分
- **原因**: f-string bug - `${real_hs}` 變咗 literal text
- **解決**: 用 `f'<span>...</span>'` 而非 `'<span>...</span>'`
- **教訓**: Python f-string 要用 `f'...{var}...'` 而非 `${var}`

### 3. 新比賽 results 唔 show
- **原因**: Match ID mapping 唔啱
  - API: match ID = "3" (Canada vs Bosnia)
  - Dashboard: match index = 2 (0-based), match ID = "3"
  - 但 Brazil vs Morocco 撞咗 ID "6"
- **解決**: Check home + away team 名，唔單純靠 ID
- **教訓**: Data source 同 dashboard match order 唔一樣

## Time Spent

| Round | Issue | Time |
|-------|-------|------|
| 1 | Collapsible 整壞 UI | ~30 min |
| 2 | Badge f-string bug | ~15 min |
| 3 | Actual score 顯示 | ~10 min |
| 4 | Match ID mapping | ~20 min |
| **Total** | | **~75 min** |

## 改進建議

1. **Minimal change approach**: comparison badge 淨係加係 score 旁邊，唔改 structure
2. **Test locally first**: 確保 generate 成功先 push
3. **Debug with print**: 用 print 確認變數值先入 HTML
4. **Team name matching**: 用 team 名對照，唔靠 ID

## 最终方案

- Badge show 係 score 隔離: `1⚽0 🟡 2-0`
- 預測為主，badge 顯示實際比分 + 估啱定估錯
- 每日 12:00 HKT cron auto update