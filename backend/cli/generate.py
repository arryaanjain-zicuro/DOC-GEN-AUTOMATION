from alpha_parser.word_parser import parse_term_sheet
from generator.excel_generator import generate_excel_from_mapping

def run_static_flow():
    alpha_path = "Term Sheet - Series 129.docx"
    mapping_path = "configs/mis_mappings.json"
    template_path = "templates/MIS_template.xlsx"
    output_path = "output/generated_MIS.xlsx"

    # Step 1: Extract fields
    alpha_data = parse_term_sheet(alpha_path)

    # Step 2: Generate output Excel
    generate_excel_from_mapping(alpha_data, mapping_path, template_path, output_path)

    print("[✔] Beta document generated:", output_path)
