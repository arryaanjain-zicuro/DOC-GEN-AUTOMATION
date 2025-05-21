import openpyxl
from utils.beta_excel_json_struct import read_excel_json
def generate_xlsx_from_json(sheets, output_path):
    wb = openpyxl.Workbook()
    # Remove the default sheet
    wb.remove(wb.active)
    for sheet in sheets:
        ws = wb.create_sheet(title=sheet['sheet_name'])
        for row in sheet['data']:
            ws.append(row)
    wb.save(output_path)

def run_json_excel_flow():
    json_path = "configs/beta_excel.json"
    output_path = "output/generated_from_json.xlsx"

    sheets = read_excel_json(json_path)
    generate_xlsx_from_json(sheets, output_path)
    print("[✔] Excel generated from JSON:", output_path)

if __name__ == "__main__":
    run_json_excel_flow()