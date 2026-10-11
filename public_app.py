"""Public, read-only Sector Radar. Deploy separately from private app.py.

This entrypoint reads ONLY published market data through public_data.py, and
educational material in sector_catalog.py / visual_atlas.py. The private app.py,
proprietary memo files and administrator functions are intentionally not imported.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from public_data import (
    load_public_snapshots, public_company_labels, public_company_record,
    public_sector_rows, public_stock_rows, public_memo_records,
)
from sector_catalog import SECTORS, SECTOR_BY_ID
from visual_atlas import VISUAL_ATLAS, local_diagram_for
from ui_theme import apply_theme, page_hero, section_heading, info_card, status_line


st.set_page_config(page_title="Sector Radar | Designed by C",
                   page_icon="📡", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
.block-container{max-width:1160px;padding-top:1.5rem;padding-bottom:3rem}
[data-testid="stAppViewContainer"]{
 background-image:radial-gradient(ellipse 55% 27% at 100% 0%,rgba(50,101,188,.13),transparent 76%);
}
h1{letter-spacing:-.045em}
[data-testid="stMetric"]{padding:14px;border:1px solid rgba(134,162,215,.17);border-radius:11px}
div[data-testid="stButton"] button{border-radius:10px;min-height:2.65rem}
.public-eyebrow{letter-spacing:.18em;color:#7daff2;font-size:.72rem;font-weight:700}
.public-credit{text-align:center;border-top:1px solid rgba(134,162,215,.19);
 padding:1.7rem 0 0;margin-top:3.5rem;color:#9fb5d4;letter-spacing:.07em}
.public-hero{border:1px solid rgba(132,168,221,.20);border-radius:14px;
 padding:1.3rem 1.4rem;margin:.7rem 0 1.25rem;
 background:linear-gradient(120deg,rgba(49,93,165,.15),rgba(49,93,165,.035))}
@media(max-width:680px){.block-container{padding-left:.8rem;padding-right:.8rem}h1{font-size:1.8rem!important}}
</style>
""", unsafe_allow_html=True)
apply_theme()

PAGES = ("🏠 總覽", "🧭 產業導覽", "📡 產業輪動", "📚 公司基本面", "📝 公司研究 Memo")


@st.cache_data(ttl=1800, show_spinner=False)
def snapshots():
    return load_public_snapshots()


def go_to(page, code=None):
    st.session_state.public_page = page
    if code is not None:
        st.session_state.public_company = str(code)
        st.session_state.public_memo_company = str(code)


def fmt(value, suffix="", digits=1):
    if value is None or pd.isna(value):
        return "—"
    return f"{float(value):,.{digits}f}{suffix}"


data = snapshots()
report = data.get("latest", {})
company_names = public_company_labels(data)
stock_rows = public_stock_rows(data)
sector_rows = public_sector_rows(data)
memos = public_memo_records(data)
if "public_page" not in st.session_state or st.session_state.public_page not in PAGES:
    st.session_state.public_page = PAGES[0]
if "public_company" not in st.session_state or st.session_state.public_company not in company_names:
    st.session_state.public_company = next(iter(company_names), "")

page_hero(
    "SECTOR RADAR",
    "產業研究，從看懂供應鏈開始。公開版呈現產業、行情、公開基本面與原創技術圖解。",
    kicker="PUBLIC RESEARCH / DESIGNED BY C",
    meta="READ ONLY  /  INDUSTRY  /  ROTATION  /  FUNDAMENTALS",
)
status_line([
    "行情快照 " + str(report.get("price_asof") or "尚未同步"),
    "行情覆蓋 " + str(report.get("price_coverage") or "—"),
    "非即時報價 · 僅供研究",
])
st.caption("公開版僅刊登篩選過的公司研究摘要；私人原始研究檔、私人備註及後台管理權限不公開。")
st.radio("研究頁面", PAGES, key="public_page", horizontal=True)
page = st.session_state.public_page


def public_overview():
    section_heading("公開研究總覽", label="MARKET PULSE", description="從產業趨勢出發，連結公司公開財報與技術導覽。")
    a, b, c = st.columns(3)
    a.metric("有行情公司", len(stock_rows))
    b.metric("追蹤產業", len(sector_rows))
    c.metric("公司研究 Memo", len(memos))
    if not sector_rows:
        st.info("尚未取得最新市場掃描；產業導覽仍可使用。")
    else:
        frame = pd.DataFrame(sector_rows).sort_values("mean_momentum_score", ascending=False)
        section_heading("強勢產業觀察", label="SECTOR RANKING")
        st.dataframe(frame.head(8).rename(columns={
            "sector": "產業", "count": "公司數", "median_r20": "20日中位報酬%",
            "mean_discovery_score": "提前挖掘評分",
            "mean_momentum_score": "強勢評分", "flow_coverage": "法人資料覆蓋",
        }), hide_index=True, use_container_width=True)
        plot = frame.set_index("sector")[["mean_momentum_score", "mean_discovery_score"]]
        st.bar_chart(plot.rename(columns={
            "mean_momentum_score": "強勢", "mean_discovery_score": "挖掘"
        }))
        st.caption("分數為自訂篩選規則，不是收益預測；法人欄為資料覆蓋，非持股比例。")
    left, right = st.columns(2)
    with left:
        st.button("🧭 看懂產業供應鏈 →", on_click=go_to,
                  args=(PAGES[1],), use_container_width=True)
    with right:
        st.button("📚 查詢公司基本面 →", on_click=go_to,
                  args=(PAGES[3],), use_container_width=True)


def public_explorer():
    section_heading("產業導覽", label="INDUSTRY EXPLORER", description="五個產業教學主題與對應原創示意圖。")
    st.caption("五個產業教學主題，包含原創圖解、上下游、代表公司、關鍵 KPI 及風險。")
    sector_ids = [sector["id"] for sector in SECTORS]
    active = st.selectbox("選擇產業", sector_ids, key="public_sector",
                          format_func=lambda key: SECTOR_BY_ID[key]["icon"] + " " +
                          SECTOR_BY_ID[key]["title"])
    sector = SECTOR_BY_ID[active]
    section_heading(sector["icon"] + " " + sector["title"], label="INDUSTRY BRIEF")
    info_card("SECTOR OVERVIEW", sector["tagline"], sector["intro"], tone="primary")
    atlas = VISUAL_ATLAS.get(active, {})
    diagram = local_diagram_for(active)
    if diagram:
        st.markdown("#### 🖼️ " + atlas.get("diagram_title", "技術概念圖"))
        st.image(diagram.read_text(encoding="utf-8"), use_container_width=True)
        st.caption(atlas.get("diagram_caption", "通用教學示意圖，非公司實際產品照片。"))
    products, chain, companies, drivers = st.tabs([
        "產品與用途", "上下游供應鏈", "代表公司與 KPI", "成長與風險"
    ])
    with products:
        for title, desc in sector["products"]:
            with st.container(border=True):
                st.markdown("**" + title + "**")
                st.write(desc)
    with chain:
        for num, (title, description) in enumerate(sector["chain"], 1):
            with st.container(border=True):
                st.caption(f"STEP {num:02d}")
                st.markdown("**" + title + "**")
                st.write(description)
        st.caption("產業位置為概念分類，不代表任何公司已取得特定 AI 客戶訂單。")
    with companies:
        st.markdown("#### 代表公司")
        for code, role, qualifier in sector["companies"]:
            left, right = st.columns([3, 1])
            with left:
                st.markdown(f'**{company_names.get(code, code)} ({code})**')
                st.caption(role + " · " + qualifier)
            with right:
                st.button("公開財報 →", key="public_company_" + active + "_" + code,
                          on_click=go_to, args=(PAGES[3], code),
                          use_container_width=True, disabled=code not in company_names)
        section_heading("關鍵 KPI", label="MEASURABLE SIGNALS")
        indicators = list(sector["kpis"])
        for start in range(0, len(indicators), 2):
            cells = st.columns(2, gap="medium")
            for index, (title, description) in enumerate(indicators[start:start + 2]):
                with cells[index]:
                    info_card("KPI / " + str(start + index + 1).zfill(2), title, description)
    with drivers:
        st.markdown("#### 成長動能")
        for point in sector["drivers"]:
            st.write("↗ " + point)
        st.markdown("#### 風險")
        for point in sector["risks"]:
            st.write("⚠ " + point)
        st.markdown("#### 查證問題")
        for question in sector["questions"]:
            st.write("• " + question)
    st.caption("代表公司、跨題材歸類是研究導覽，不構成訂單認列、營收占比或投資建議。")


def public_rotation():
    section_heading("產業輪動", label="SECTOR ROTATION",
                    description="由掃描快照整理的個股相對強弱與產業排名。")
    st.caption("行情為最近一次批次掃描快照，非即時委託簿。")
    if not stock_rows or not sector_rows:
        st.warning("市場資料尚未同步；請先使用產業導覽。")
        return
    table = pd.DataFrame(stock_rows)
    sector_options = ["全部產業"] + sorted(table["sector"].dropna().unique().tolist())
    selected = st.selectbox("產業篩選", sector_options, key="public_rotation_sector")
    category = st.radio("排序方式", ("強勢評分", "提前挖掘", "20日報酬"), horizontal=True)
    sort_key = {"強勢評分": "momentum_score",
                "提前挖掘": "discovery_score", "20日報酬": "r20"}[category]
    if selected != "全部產業":
        table = table[table["sector"] == selected]
    table = table.sort_values(sort_key, ascending=False, na_position="last")
    st.dataframe(table[[
        "code", "name", "sector", "close", "r5", "r20",
        "rs20", "discovery_score", "momentum_score", "stage"
    ]].rename(columns={
        "code": "代號", "name": "公司", "sector": "產業",
        "close": "收盤價", "r5": "5日漲跌%", "r20": "20日漲跌%",
        "rs20": "相對強度%", "discovery_score": "挖掘評分",
        "momentum_score": "強勢評分", "stage": "模型階段"
    }), hide_index=True, use_container_width=True)
    st.caption("缺值不可視為零；價格、相對強度、評分及模型階段皆只用於研究篩選。")
    sector_table = pd.DataFrame(public_sector_rows(data)).sort_values(
        "mean_momentum_score", ascending=False)
    st.markdown("#### 產業強弱比較")
    st.dataframe(sector_table.rename(columns={
        "sector": "產業", "count": "公司數", "median_r20": "20日中位報酬%",
        "mean_discovery_score": "挖掘評分",
        "mean_momentum_score": "強勢評分", "flow_coverage": "法人資料覆蓋"
    }), hide_index=True, use_container_width=True)


def public_fundamentals():
    section_heading("公司公開基本面", label="COMPANY FUNDAMENTALS",
                    description="僅展示官方登錄、申報月營收與已公布歷史財報。")
    st.caption("財務指標取自公開財報；研究假設另見「📝 公司研究 Memo」，兩者不得混為一談。")
    if not company_names:
        st.info("公司清單尚未同步。")
        return
    code = st.selectbox("搜尋公司代號／名稱", list(company_names),
                        key="public_company",
                        format_func=lambda key: key + " · " + company_names[key])
    entry = public_company_record(data, code)
    section_heading(str(entry["name"]) + " · " + str(entry["code"]), label="COMPANY PROFILE")
    status_line(["研究分類 " + str(entry["sector"]), "市場 " + str(entry["market"])])
    if entry["official_name"]:
        st.markdown("**公司官方名稱：** " + str(entry["official_name"]))
    else:
        st.info("目前沒有同步到此公司的官方公司登錄資料，不能據此推估其財務數字。")
    section_heading("最近月營收變化", label="MONTHLY REVENUE")
    a, b, c = st.columns(3)
    a.metric("營收 MoM", fmt(entry["revenue_mom_pct"], "%"))
    b.metric("營收 YoY", fmt(entry["revenue_yoy_pct"], "%"))
    c.metric("年初至今 YoY", fmt(entry["revenue_ytd_yoy_pct"], "%"))
    st.caption(f'公告月份：{entry["revenue_period"] or "尚未同步"} '
               '· 缺值顯示 —，不等於 0%')
    section_heading("已公布季度財報", label="QUARTERLY FINANCIALS")
    quarters = entry["quarters"]
    if not quarters:
        st.info("目前沒有可用的季度數據；不使用估計 EPS 或填補缺漏。")
    else:
        latest = quarters[-1]
        a, b, c = st.columns(3)
        a.metric("最新季度 EPS", fmt(latest["eps"], " 元", 2))
        b.metric("毛利率", fmt(latest["gross_margin"], "%", 2))
        c.metric("營業利益率", fmt(latest["operating_margin"], "%", 2))
        st.caption("季度：" + latest["period"] +
                   " · 季度 EPS 不是分析師預估值；單季 EPS 不應直接當全年 EPS。")
        qframe = pd.DataFrame(quarters)
        if qframe["eps"].notna().any():
            st.line_chart(qframe.set_index("period")["eps"])
        st.dataframe(qframe.rename(columns={
            "period": "季度", "eps": "EPS 元", "gross_margin": "毛利率%",
            "operating_margin": "營益率%",
            "revenue_yoy_pct": "營收 YoY%",
            "gross_margin_yoy_pp": "毛利率同比變化 pp",
            "eps_yoy_delta": "EPS 同比差額 元"
        }), hide_index=True, use_container_width=True)
    st.caption("來源：TWSE / TPEx 發行公司公開資訊、MOPS 申報月營收、FinMind 歷史季報。")
    for label, url in (("查看公司資訊來源 ↗", entry["official_source"]),
                       ("查看月營收來源 ↗", entry["revenue_source"])):
        if isinstance(url, str) and url.startswith("https://"):
            st.link_button(label, url)
    if code in ("6456", "7873"):
        st.caption("此標的目前為產業研究連結，不代表已納入上述行情與季度財報同步宇宙。")
    if code in memos:
        st.button("📝 閱讀這家公司的研究 Memo →", key="fundamental_to_memo",
                  on_click=go_to, args=(PAGES[4], code), use_container_width=True)


def public_memo_page():
    section_heading("公司研究 Memo", label="RESEARCH NOTES",
                    description="原始研究工作台整理出的可公開摘要：研究論點、瓶頸、反證與 2027 EPS 驗證方向。")
    if not memos:
        st.info("尚未發布任何公司研究摘要；請等待研究發布流程。")
        return
    a, b, c = st.columns(3)
    a.metric("涵蓋公司", len(memos))
    b.metric("深度研究提綱", sum(bool(item.get("deep")) for item in memos.values()))
    c.metric("人工研究筆記", sum(bool(item.get("manual")) for item in memos.values()))
    meta = data.get("memos") or {}
    st.caption("研究提綱日期：" + str(meta.get("prepared_on") or "未註明") +
               " · 不是自動更新的券商共識或正式 EPS 預測")
    st.info("以下為研究假設與待查證問題，不代表已證實的公司訂單、營收占比、客戶或 2027 年 EPS。")

    if "public_memo_company" not in st.session_state or st.session_state.public_memo_company not in memos:
        previous = st.session_state.get("public_company")
        st.session_state.public_memo_company = previous if previous in memos else next(iter(memos))
    code = st.selectbox("搜尋公司代號或名稱", list(memos), key="public_memo_company",
                        format_func=lambda key: key + " · " + memos[key]["name"])
    entry = memos[code]
    section_heading(entry["name"] + " · " + code, label="COMPANY RESEARCH")
    st.caption("資料分類：可公開研究摘要 · 非公司公告或券商報告")
    manual = entry.get("manual")
    deep = entry.get("deep")
    if deep:
        info_card("RESEARCH THESIS", "研究定位",
                  deep.get("research_position") or "仍待建立完整研究論點", tone="primary")
        first, second = st.columns(2, gap="medium")
        with first:
            info_card("EARNINGS ENGINE", "獲利成長假設",
                      deep.get("earnings_engine") or "待補齊")
            info_card("KEY KPI", "核心追蹤指標",
                      deep.get("key_metric_focus") or "待補齊")
        with second:
            info_card("BOTTLENECK", "主要瓶頸",
                      deep.get("potential_bottleneck") or "待補齊")
            info_card("BEAR CASE", "風險與反證",
                      deep.get("bear_case") or "待補齊")
        thesis, verify = st.tabs(["2027 EPS · 情境思考", "待查證清單"])
        with thesis:
            scenario = deep.get("scenario_2027") or {}
            st.markdown("#### 獲利橋接邏輯")
            st.write(scenario.get("framework") or "未建立量化模型")
            st.markdown("#### 敏感度與關鍵變數")
            st.write(scenario.get("sensitivity") or "缺乏可查證的輸入")
            st.markdown("#### 尚缺資料")
            for value in scenario.get("missing_inputs", []):
                st.write("• " + value)
        with verify:
            for question in deep.get("verification", []):
                st.write("☐ " + question)
            if deep.get("source_qualification"):
                st.caption(deep["source_qualification"])
        st.caption("研究提綱整理日期：" + str(deep.get("prepared_on") or "未註明"))
    if manual:
        with st.expander("📒 人工研究筆記", expanded=not bool(deep)):
            for title, key in (("主要業務", "business"), ("投資論點", "thesis"),
                               ("觀察催化劑", "catalyst"), ("主要風險", "risk"),
                               ("確信程度與限制", "confidence")):
                if manual.get(key):
                    st.markdown("**" + title + "**")
                    st.write(manual[key])
            if manual.get("questions"):
                st.markdown("**優先驗證的問題**")
                for question in manual["questions"]:
                    st.write("• " + question)
    left, right = st.columns(2)
    with left:
        st.button("查看公司已公布財報 →", key="memo_to_fundamentals",
                  on_click=go_to, args=(PAGES[3], code), use_container_width=True)
    with right:
        st.link_button("公開資訊觀測站 ↗", "https://mops.twse.com.tw/",
                       use_container_width=True)
    st.caption("研究來源為原創分析與查證方向；不含付費券商報告原文。完整原始研究檔仍只存放於私人工作台。")


if page == PAGES[0]:
    public_overview()
elif page == PAGES[1]:
    public_explorer()
elif page == PAGES[2]:
    public_rotation()
elif page == PAGES[3]:
    public_fundamentals()
else:
    public_memo_page()

st.markdown("""<div class="public-credit">
SECTOR RADAR · DESIGNED BY C<br>
<span style="font-size:.75rem;letter-spacing:normal">
PUBLIC / READ ONLY · 非投資建議 · 非即時報價
</span></div>""", unsafe_allow_html=True)
