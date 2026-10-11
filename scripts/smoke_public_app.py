"""Offline smoke test for all public routes and company picker."""
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def keyed(at, category, key):
    return next(widget for widget in getattr(at, category) if widget.key == key)


def assert_page(at, page):
    if at.exception:
        raise AssertionError(f"{page}: " + "; ".join(str(x.message) for x in at.exception))
    assert at.session_state["public_page"] == page


def main():
    with patch("requests.get", side_effect=RuntimeError("Network access not allowed in smoke test")):
        at = AppTest.from_file(str(ROOT / "public_app.py"), default_timeout=60).run()
        assert_page(at, "🏠 總覽")
        for page in ("🧭 產業導覽", "📡 產業輪動", "📚 公司基本面"):
            keyed(at, "radio", "public_page").set_value(page).run()
            assert_page(at, page)
        company = keyed(at, "selectbox", "public_company")
        assert "2368" in company.options, "Missing public company selector data"
        company.set_value("2368").run()
        assert_page(at, "📚 公司基本面")
        keyed(at, "radio", "public_page").set_value("🧭 產業導覽").run()
        keyed(at, "selectbox", "public_sector").set_value("pcb").run()
        assert_page(at, "🧭 產業導覽")
    print("Public Sector Radar: all four pages, company and industry navigation passed")


if __name__ == "__main__":
    main()
