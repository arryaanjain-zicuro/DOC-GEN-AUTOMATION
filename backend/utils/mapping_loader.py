# cli/mapping_utils.py
import json
import re
from datetime import datetime
from pathlib import Path

from extract_sec_from_alpha import extract_security_info_from_alpha_json, extract_series_from_product_code, extract_issue_size_details
from extract_sec_from_alpha import extract_underlying, extract_date_of_maturity
SECURITY_KEYWORDS = {
    "secured": re.compile(r"\bsecured\b", re.I),
    "unsecured": re.compile(r"\bunsecured\b", re.I),
    "listed": re.compile(r"\blisted\b", re.I),
    "unlisted": re.compile(r"\bunlisted\b", re.I),
    "rated": re.compile(r"\brated\b", re.I),
    "unrated": re.compile(r"\bunrated\b", re.I),
}

DATE_PAT = re.compile(
    r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})"            # “15 May 2025”
    r"|(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"              # “15/05/25” or “15-05-2025”
    r"|([A-Za-z]{3,9}\s+\d{4})"                      # “May 2025”
)

ROOT_DIR = Path(__file__).parent.parent
CONFIGS_DIR = ROOT_DIR / "configs"
ALPHA_JSON = CONFIGS_DIR / "alpha_doc.json"

series = ""

product_code = ""  # get this from your data source

def _load_alpha_json():
    with open(ALPHA_JSON, encoding="utf-8") as f:
        return json.load(f)

def derive_mapping():
    alpha_json = _load_alpha_json()
    extracted = extract_security_info_from_alpha_json(alpha_json)
    series = extract_series_from_product_code(alpha_json)
    details = extract_issue_size_details(alpha_json)
    underlying_value = extract_underlying(alpha_json)
    date_of_maturity = extract_date_of_maturity(alpha_json)
    return {
    "qualified_keywords": extracted["keywords"],
    "date_found": extracted["date_found"],
    "sheet_name": extracted["sheet_name"],
    "series" : series,
    "details" : details,
    "underlying_value": underlying_value,
    "date_of_maturity" : date_of_maturity
    }


# If run directly, print the mapping for quick inspection
if __name__ == "__main__":
    print(json.dumps(derive_mapping(), indent=2))
