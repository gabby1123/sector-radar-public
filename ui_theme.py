"""Shared visual language for Sector Radar.

Presentation-only helpers. No data, ranking or financial calculation lives here.
All dynamic text embedded into HTML is escaped.
"""
from html import escape


GLOBAL_CSS = """
<style>
:root {
    --sr-accent: #75adf8;
    --sr-ink-muted: #8da1bb;
    --sr-stroke: rgba(123, 157, 208, .23);
    --sr-radius: 14px;
}
html {scroll-behavior:smooth}
[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse 75% 30% at 89% -6%,rgba(57,112,191,.18),transparent 68%),
        radial-gradient(ellipse 55% 24% at 0% 55%,rgba(38,89,157,.065),transparent 70%);
}
[data-testid="stAppViewContainer"] .block-container {
    max-width:1260px;
    padding:1.55rem 2.1rem 5rem;
}
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    letter-spacing:-.025em;
    line-height:1.38;
    scroll-margin-top:24px;
}
[data-testid="stMarkdownContainer"] h2 {margin-top:1.2rem}
[data-testid="stMarkdownContainer"] h3 {margin-top:1rem}
[data-testid="stMarkdownContainer"] p {line-height:1.72}
[data-testid="stCaptionContainer"] p {line-height:1.6}
[data-testid="stVerticalBlockBorderWrapper"] {
    border:1px solid var(--sr-stroke);
    border-radius:var(--sr-radius);
    background:color-mix(in srgb,var(--secondary-background-color) 44%, transparent);
}
[data-testid="stMetric"] {
    border:1px solid var(--sr-stroke);
    border-radius:var(--sr-radius);
    background:linear-gradient(135deg,
        color-mix(in srgb,var(--secondary-background-color) 72%, transparent),
        color-mix(in srgb,var(--background-color) 86%, var(--primary-color) 14%));
    min-height:104px;
    padding:17px 18px 15px;
}
[data-testid="stMetricLabel"] {letter-spacing:.025em}
[data-testid="stMetricValue"] {
    font-size:clamp(1.22rem,2vw,1.7rem);
    font-weight:750;
    letter-spacing:-.03em;
}
[data-testid="stMetricDelta"] {font-size:.8rem}
[data-testid="stDataFrame"] {
    border:1px solid var(--sr-stroke);
    border-radius:12px;
    overflow:hidden;
}
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap:.35rem;
    border-bottom:1px solid var(--sr-stroke);
    overflow-x:auto;
    scrollbar-width:thin;
}
[data-testid="stTabs"] button[role="tab"] {
    font-weight:620;
    padding:.85rem .9rem;
    white-space:nowrap;
    border-radius:9px 9px 0 0;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color:var(--sr-accent);
    background:rgba(98,150,233,.1);
}
[data-testid="stExpander"] {
    border-radius:12px;
    overflow:hidden;
}
[data-testid="stButton"] button,
[data-testid="stLinkButton"] a,
[data-testid="stDownloadButton"] button {
    border-radius:10px;
    min-height:2.6rem;
    font-weight:640;
    letter-spacing:.008em;
}
[data-testid="stButton"] button:hover,
[data-testid="stLinkButton"] a:hover {border-color:rgba(117,173,248,.65)}
[data-testid="stSelectbox"] {max-width:none}
hr {border-color:var(--sr-stroke)!important;opacity:.65}
.sr-hero {
    border:1px solid var(--sr-stroke);
    border-radius:18px;
    padding:27px 28px 24px;
    background:linear-gradient(117deg,rgba(59,111,189,.17),rgba(53,112,191,.035) 70%);
    margin:2px 0 16px;
}
.sr-kicker {
    color:var(--sr-accent);
    font-size:.68rem;
    letter-spacing:.16em;
    font-weight:800;
    text-transform:uppercase;
    margin-bottom:8px;
}
.sr-hero__title {
    color:var(--text-color);
    font-size:clamp(1.75rem,3.2vw,2.45rem);
    font-weight:790;
    letter-spacing:-.045em;
    line-height:1.2;
    margin:0 0 8px;
}
.sr-hero__subtitle {
    color:var(--text-color);
    font-size:.91rem;
    line-height:1.65;
    opacity:.77;
    margin:0;
}
.sr-hero__meta {
    margin-top:12px;
    font-size:.7rem;
    letter-spacing:.09em;
    color:var(--sr-ink-muted);
}
.sr-section-heading {
    margin:24px 0 11px;
    padding:0 0 0 13px;
    border-left:3px solid var(--sr-accent);
}
.sr-section-heading__label {
    font-size:.65rem;
    letter-spacing:.13em;
    color:var(--sr-accent);
    font-weight:760;
    margin-bottom:3px;
}
.sr-section-heading__title {
    color:var(--text-color);
    font-weight:750;
    font-size:1.15rem;
    letter-spacing:-.025em;
    line-height:1.36;
}
.sr-section-heading__description {
    color:var(--text-color);
    opacity:.64;
    font-size:.82rem;
    line-height:1.58;
    margin-top:4px;
}
.sr-info-card {
    border:1px solid var(--sr-stroke);
    border-radius:var(--sr-radius);
    padding:17px 18px 18px;
    margin:6px 0 12px;
    background:color-mix(in srgb,var(--secondary-background-color) 42%,transparent);
    overflow-wrap:anywhere;
}
.sr-info-card--primary {
    background:linear-gradient(113deg,rgba(75,134,225,.14),rgba(75,134,225,.025));
    border-color:rgba(117,173,248,.43);
}
.sr-info-card__label {
    font-size:.64rem;
    color:var(--sr-accent);
    letter-spacing:.1em;
    font-weight:770;
    margin-bottom:9px;
}
.sr-info-card__title {
    color:var(--text-color);
    font-size:1.01rem;
    font-weight:750;
    letter-spacing:-.015em;
    margin-bottom:8px;
}
.sr-info-card__body {
    color:var(--text-color);
    opacity:.81;
    font-size:.9rem;
    line-height:1.75;
    white-space:pre-line;
}
.sr-status-row {
    display:flex;
    flex-wrap:wrap;
    align-items:center;
    column-gap:16px;
    row-gap:6px;
    padding:6px 0 11px;
    color:var(--text-color);
    opacity:.73;
    font-size:.78rem;
}
.sr-status-dot {
    width:6px;
    height:6px;
    border-radius:50%;
    background:#7ec8b0;
    display:inline-block;
    margin-right:6px;
}
.sector-card {
    border-radius:12px;
    min-height:227px;
}
.sector-card--selected .sector-card__title {color:var(--sr-accent)}
.sector-card__tagline {line-height:1.6}
@media(max-width:750px){
    [data-testid="stAppViewContainer"] .block-container {
        padding:.75rem .75rem 3.5rem;
    }
    .sr-hero {padding:18px 17px 17px;border-radius:14px;margin-top:0}
    .sr-hero__title {font-size:1.65rem}
    .sr-hero__subtitle {font-size:.84rem}
    .sr-section-heading {margin-top:19px}
    .sr-section-heading__title {font-size:1.06rem}
    .sr-info-card {padding:15px 15px 16px}
    .sr-info-card__body {font-size:.87rem}
    [data-testid="stMetric"] {min-height:94px;padding:12px 12px 10px}
    [data-testid="stMetricValue"] {font-size:1.14rem}
    [data-testid="stTabs"] button[role="tab"] {padding:.72rem .66rem;font-size:.84rem}
    [data-testid="stButton"] button {font-size:.83rem;min-height:2.8rem}
    .sector-card {min-height:0}
}
</style>
"""


def _html(value):
    """Safe text for the HTML-only presentational components."""
    return escape(str(value if value is not None else "—"), quote=True)


def hero_markup(title, subtitle, kicker="SECTOR INTELLIGENCE", meta=""):
    extra = '<div class="sr-hero__meta">' + _html(meta) + '</div>' if meta else ""
    return (
        '<header class="sr-hero">'
        '<div class="sr-kicker">' + _html(kicker) + '</div>'
        '<h1 class="sr-hero__title">' + _html(title) + '</h1>'
        '<p class="sr-hero__subtitle">' + _html(subtitle) + '</p>'
        + extra + '</header>'
    )


def heading_markup(title, label="RESEARCH", description=""):
    extra = (
        '<div class="sr-section-heading__description">' + _html(description) + '</div>'
        if description else ""
    )
    return (
        '<div class="sr-section-heading">'
        '<div class="sr-section-heading__label">' + _html(label) + '</div>'
        '<div class="sr-section-heading__title">' + _html(title) + '</div>'
        + extra + '</div>'
    )


def info_card_markup(label, title, body, tone="standard"):
    variant = "primary" if tone == "primary" else "standard"
    return (
        '<div class="sr-info-card sr-info-card--' + variant + '">'
        '<div class="sr-info-card__label">' + _html(label) + '</div>'
        '<div class="sr-info-card__title">' + _html(title) + '</div>'
        '<div class="sr-info-card__body">' + _html(body) + '</div>'
        '</div>'
    )


def apply_theme():
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_hero(title, subtitle, kicker="SECTOR INTELLIGENCE", meta=""):
    import streamlit as st
    st.markdown(hero_markup(title, subtitle, kicker, meta), unsafe_allow_html=True)


def section_heading(title, label="RESEARCH", description=""):
    import streamlit as st
    st.markdown(heading_markup(title, label, description), unsafe_allow_html=True)


def info_card(label, title, body, tone="standard"):
    import streamlit as st
    st.markdown(info_card_markup(label, title, body, tone), unsafe_allow_html=True)


def status_line(items):
    """Render metadata only; never claim a timestamp is live."""
    import streamlit as st
    spans = "".join("<span>" + _html(item) + "</span>" for item in items)
    st.markdown('<div class="sr-status-row">' + spans + '</div>', unsafe_allow_html=True)
