from openpyxl import load_workbook

def generate_excel_from_mapping(alpha_data: dict, mapping_file: str, template_file: str, output_file: str):
    import json

    with open(mapping_file) as f:
        config = json.load(f)

    wb = load_workbook(template_file)

    for alpha_field, rule in config["mappings"].items():
        value = alpha_data.get(alpha_field, "")
        if not value:
            continue

        sheet = wb[rule["sheet"]]
        cell = rule["cell"]

        if rule["action"] == "write":
            sheet[cell] = value
        # You can extend logic here for append or calculations

    wb.save(output_file)
