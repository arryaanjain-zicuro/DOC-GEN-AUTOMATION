import json
from pathlib import Path
from openpyxl import load_workbook

def excel_to_json_file(excel_path):
    workbook = load_workbook(excel_path, data_only=True)
    result = {
        "sheets": []
    }

    for sheet in workbook.sheetnames:
        ws = workbook[sheet]
        sheet_data = []

        for row in ws.iter_rows(values_only=True):
            sheet_data.append([str(cell).strip() if cell is not None else "" for cell in row])

        result["sheets"].append({
            "sheet_name": sheet,
            "data": sheet_data
        })

    return result
