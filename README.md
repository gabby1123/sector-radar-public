# Sector Radar — Public Edition

**Designed by C** · 台股產業研究 · Industry Intelligence

此專案是獨立公開、唯讀的產業研究平台；不含私人研究 Memo、估值工作底稿、交易策略、管理頁或 API 金鑰。

## 部署 Streamlit Community Cloud

- Repository: `gabby1123/sector-radar-public`
- Branch: `main`
- Main file path: `public_app.py`
- App URL：部署後由 Streamlit Cloud 提供，可在新 App 的 Sharing 設為 Public。

## 功能

- 🏠 產業總覽：研究宇宙與產業領先群
- 🧭 產業導覽：PCB/CCL、AI 伺服器、先進封裝、半導體設備、光通訊及原創技術 SVG
- 📡 產業輪動：以歷史價格為基礎的規則型排名
- 📚 公司基本面：上市櫃公司公告資料、MOPS 月營收、FinMind 已發布季度資料

## 資料狀態與注意事項

- 本次公開價格快照：2026-10-08
- 公司資料同步：2026-10-11T06:25:32+00:00
- 月營收同步：2026-10-11T06:25:40+00:00
- 季報來源同步：2026-10-11T05:51:02+00:00

**這是經白名單篩選的一次性公開快照，不會自動同步原本的私人 Repository。** 後續若要定期更新，需要增設安全的公開資料發布工作流程；請勿複製私人 Repo 的整個 `data/`。

所有排行、評分和模型階段只供研究，不代表投資建議或預測未來報酬，行情非即時。
公司的產業關聯可能只是研究主題，未經公司證實者不應解讀成正式出貨或訂單。

## 本機執行

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -p 'test_*.py' -v
streamlit run public_app.py
```
