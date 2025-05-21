import openpyxl
from utils.beta_excel_json_struct import read_excel_json
from openpyxl.styles import PatternFill, Font

def apply_style(cell, style):
    fill = style.get("fill")
    if fill:
        if fill.startswith("theme:"):
            # openpyxl does not support setting theme colors directly, so skip or map as needed
            pass
        elif len(fill) == 8:  # ARGB
            cell.fill = PatternFill(start_color=fill, end_color=fill, fill_type="solid")
        elif len(fill) == 6:  # RGB
            cell.fill = PatternFill(start_color="FF"+fill, end_color="FF"+fill, fill_type="solid")
        else:
            # fallback, try as is
            cell.fill = PatternFill(start_color=fill, end_color=fill, fill_type="solid")

    font_kwargs = {
        "bold": style.get("bold", False),
        "italic": style.get("italic", False)
    }
    font_color = style.get("font_color", None)
    if font_color:
        # Only use if it's a valid 8-char ARGB hex
        if isinstance(font_color, str) and len(font_color) == 8 and all(c in "0123456789ABCDEFabcdef" for c in font_color):
            font_kwargs["color"] = font_color
        # If it's 6-char RGB, prepend 'FF'
        elif isinstance(font_color, str) and len(font_color) == 6 and all(c in "0123456789ABCDEFabcdef" for c in font_color):
            font_kwargs["color"] = "FF" + font_color
        # Otherwise, skip setting color

    cell.font = Font(**font_kwargs)

def generate_xlsx_from_json(sheets, output_path):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for sheet in sheets:
        ws = wb.create_sheet(title=sheet['sheet_name'])
        data = sheet['data']
        styles = sheet.get('styles', [])
        for i, row in enumerate(data):
            ws.append(row)
            if styles:
                for j, style in enumerate(styles[i]):
                    apply_style(ws.cell(row=i+1, column=j+1), style)
        # Re-apply merged cells if present
        if 'merged_cells' in sheet:
            for merge_range in sheet['merged_cells']:
                ws.merge_cells(merge_range)
    wb.save(output_path)

def run_json_excel_flow():
    json_path = "configs/beta_excel.json"
    output_path = "output/generated_from_json.xlsx"

    sheets = read_excel_json(json_path)
    generate_xlsx_from_json(sheets, output_path)
    print("[✔] Excel generated from JSON:", output_path)

if __name__ == "__main__":
    run_json_excel_flow()