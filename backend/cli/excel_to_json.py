from openpyxl import load_workbook
from openpyxl.styles import PatternFill

def get_rgb(color):
    """Extract RGB hex string from openpyxl color object, if possible."""
    if color is None:
        return None
    if hasattr(color, "rgb") and color.rgb is not None:
        return str(color.rgb)  # Ensure it's a string
    if hasattr(color, "index") and color.index is not None:
        return str(color.index)
    if hasattr(color, "theme") and color.theme is not None:
        return f"theme:{color.theme}"
    return None

def get_cell_style(cell):
    style = {}
    if cell.fill and isinstance(cell.fill, PatternFill):
        fg = get_rgb(cell.fill.fgColor)
        start = get_rgb(cell.fill.start_color)
        fill_color = start or fg
        if fill_color and fill_color != "00000000":
            style["fill"] = fill_color
    if cell.font:
        style["bold"] = cell.font.bold
        style["italic"] = cell.font.italic
        if cell.font.color:
            font_color = get_rgb(cell.font.color)
            if font_color:
                style["font_color"] = font_color
    return style

def excel_to_json_file(excel_path):
    workbook = load_workbook(excel_path, data_only=True)
    result = {"sheets": []}

    for sheet in workbook.sheetnames:
        ws = workbook[sheet]
        sheet_data = []
        style_data = []
        for row in ws.iter_rows():
            row_values = []
            row_styles = []
            for cell in row:
                row_values.append(str(cell.value).strip() if cell.value is not None else "")
                row_styles.append(get_cell_style(cell))
            # Only add non-empty rows
            if any(cell != "" for cell in row_values):
                sheet_data.append(row_values)
                style_data.append(row_styles)
        merged_cells = [str(merge) for merge in ws.merged_cells.ranges]
        result["sheets"].append({
            "sheet_name": sheet,
            "data": sheet_data,
            "styles": style_data,
            "merged_cells": merged_cells
        })
    return result
