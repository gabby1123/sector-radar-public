"""Verified illustrative asset index for Sector Radar's technical education pages.

Three optional photos come from Wikimedia Commons; every sector has an offline SVG schematic.
Creator and exact license must be shown adjacent to each image. Avoid claiming the
generic object in a photo is an AI server, a CoWoS package, or a CPO product.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LICENSE_CC_BY_SA_30 = "https://creativecommons.org/licenses/by-sa/3.0/"

VISUAL_ATLAS = {
    "server": {
        "diagram": "assets/diagrams/ai_server_architecture.svg",
        "diagram_title": "AI 伺服器系統與機櫃架構",
        "diagram_caption": "本地自製示意：運算晶片、記憶體、PCB、高速互連與機櫃電力、散熱的關係；不代表單一廠商規格。",
        "investment_signals": [
            ("整櫃價值", "單櫃售價上升是否真的轉成代工毛利？"),
            ("供應鏈", "GPU、HBM、電力和液冷設備的交付瓶頸是什麼？"),
            ("認列時點", "機櫃出貨、驗收與營收認列是否同步？"),
        ],
    },
    "equipment": {
        "diagram": "assets/diagrams/semiconductor_equipment_flow.svg",
        "diagram_title": "半導體設備製程與驗收",
        "diagram_caption": "本地自製示意：薄膜、蝕刻、清洗、量測、封裝的簡化設備路線；不是單一實際製程流程或機台規格。",
        "investment_signals": [
            ("設備認列", "訂單、交貨、裝機、驗收何時進入營收？"),
            ("景氣循環", "晶圓廠資本支出會在哪些設備環節反映？"),
            ("利潤品質", "耗材、維保與自有品牌服務比重能否改善毛利？"),
        ],
    },
    "pcb": {
        "diagram": "assets/diagrams/pcb_ccl_layers.svg",
        "diagram_title": "PCB / CCL 多層板剖面",
        "diagram_caption": "自行繪製的教學示意：銅箔、樹脂介電層、玻纖芯材與鍍通孔；層數與厚度不按比例。",
        "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Printed_circuit_board.jpg/960px-Printed_circuit_board.jpg",
        "photo_title": "一般電子產品中的 PCB 實物",
        "photo_context": "這是數位萬用電表的已裝配 PCB，僅示範板材與電子元件外觀，並非 AI 伺服器高多層板。",
        "photo_author": "Cjp24",
        "photo_source": "https://commons.wikimedia.org/wiki/File:Printed_circuit_board.jpg",
        "photo_license": "CC BY-SA 3.0",
        "photo_license_url": LICENSE_CC_BY_SA_30,
        "investment_signals": [
            ("材料升級", "CCL 低損耗等級升級是否轉成實際 ASP／產品組合？"),
            ("量產難度", "層數、鑽孔與層間壓合良率是否改善？"),
            ("營收驗證", "AI 高階 PCB 出貨量、稼動率與毛利率是否同步提升？"),
        ],
    },
    "packaging": {
        "diagram": "assets/diagrams/advanced_packaging_2_5d.svg",
        "diagram_title": "2.5D 先進封裝互連剖面",
        "diagram_caption": "自行繪製的教學示意：邏輯晶粒、HBM、Interposer／RDL、微凸塊、有機載板；不同封裝製程不一定包含所有層。",
        "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Chips_on_6-Inch-Wafer_01.jpg/960px-Chips_on_6-Inch-Wafer_01.jpg",
        "photo_title": "矽晶圓與晶粒實物",
        "photo_context": "照片是 150 mm 晶圓上的晶粒，並不是已完成的 CoWoS／2.5D 封裝成品；用於認識封裝前的實體晶粒。",
        "photo_author": "Armin Kübelbeck",
        "photo_source": "https://commons.wikimedia.org/wiki/File:Chips_on_6-Inch-Wafer_01.jpg",
        "photo_license": "CC BY-SA 3.0",
        "photo_license_url": LICENSE_CC_BY_SA_30,
        "investment_signals": [
            ("良率與密度", "RDL、微凸塊與高密度互連良率能否長期量產？"),
            ("產能瓶頸", "設備交期、客戶驗證、載板供應何者限制出貨？"),
            ("獲利傳導", "先進封裝高階收入比重是否足以超過折舊及費用增加？"),
        ],
    },
    "optical": {
        "diagram": "assets/diagrams/optical_engine_path.svg",
        "diagram_title": "光通訊電光轉換路徑",
        "diagram_caption": "自行繪製的教學示意：ASIC 電訊號經驅動／光源／探測器與光纖傳送；實際光模組或 CPO 位置依產品架構不同。",
        "photo_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/SFP_board.jpg/960px-SFP_board.jpg",
        "photo_title": "SFP 光收發模組內部電路板",
        "photo_context": "這是可插拔 SFP 元件示例，非 800G／1.6T 光引擎，也不是 CPO 量產產品。",
        "photo_author": "Christophe.Finot",
        "photo_source": "https://commons.wikimedia.org/wiki/File:SFP_board.jpg",
        "photo_license": "CC BY-SA 3.0",
        "photo_license_url": LICENSE_CC_BY_SA_30,
        "investment_signals": [
            ("規格轉換", "400G／800G／1.6T 認證進程是否真正反映在營收？"),
            ("成本與良率", "耦光精度、測試成本、耗電量會如何影響毛利率？"),
            ("CPO 時程", "新架構目前仍在送樣驗證，或已正式量產並認列收入？"),
        ],
    },
}


def local_diagram_for(sector_id):
    """Return an in-repository diagram, not an untrusted remote path."""
    record = VISUAL_ATLAS.get(sector_id)
    if record is None:
        return None
    relative = Path(record["diagram"])
    if relative.is_absolute() or ".." in relative.parts or relative.suffix != ".svg":
        return None
    result = ROOT / relative
    return result if result.is_file() else None
