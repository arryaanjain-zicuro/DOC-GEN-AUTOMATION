from openpyxl import Workbook
from pathlib import Path
import json
import re, os

def generate_excel_sheet_from_json(excel_json: dict, file_path: str = "generated_output.xlsx"):
    """
    Generate an Excel file from a structured JSON dict and save it in the 'generated/' directory.
    Creates the directory if it doesn't exist.
    """
    # Ensure 'generated/' directory exists
    output_dir = os.path.dirname(file_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "Extracted Data"

    # dict branch
    if isinstance(data, dict):
        ws.append(list(data.keys()))
        ws.append(list(data.values()))

    # list-of-lists branch
    elif isinstance(data, list) and all(isinstance(r, (list, tuple)) for r in data):
        for row in data:
            ws.append(row)

    else:
        raise ValueError("Unsupported data structure for Excel generation")

    wb.save(file_path)
    print(f"Excel saved at: {file_path}")
    
ROOT_DIR = Path(__file__).parent.parent
CONFIGS_DIR = ROOT_DIR / "configs"
EXCEL_JSON = CONFIGS_DIR / "beta_excel.json"

def _load_excel_json():
    with open(EXCEL_JSON, encoding="utf-8") as f:
        return json.load(f)
    
if __name__ == "__main__":
    excel_json = _load_excel_json()
    generate_excel_sheet_from_json(excel_json)