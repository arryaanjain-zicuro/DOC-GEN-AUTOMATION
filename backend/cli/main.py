import json
from pathlib import Path
from docx_to_json import docx_to_json
from excel_to_json import excel_to_json

def main():
    root_dir = Path(__file__).parent.parent
    templates_dir = root_dir / "templates"
    configs_dir = root_dir / "configs"

    # Ensure configs folder exists
    configs_dir.mkdir(parents=True, exist_ok=True)

    # === WORD ===
    input_docx = templates_dir / "alpha_doc.docx"
    if input_docx.exists():
        print(f"Processing Word: {input_docx}")
        word_json = docx_to_json(input_docx)
        with open(configs_dir / "alpha_doc.json", "w", encoding="utf-8") as f:
            json.dump(word_json, f, indent=2, ensure_ascii=False)
        print("Saved: configs/alpha_doc.json")
    else:
        print(f"Missing Word file: {input_docx}")

    # === EXCEL ===
    input_excel = templates_dir / "MIS.xlsx"
    if input_excel.exists():
        print(f"Processing Excel: {input_excel}")
        excel_json = excel_to_json(input_excel)
        with open(configs_dir / "beta_excel.json", "w", encoding="utf-8") as f:
            json.dump(excel_json, f, indent=2, ensure_ascii=False)
        print("Saved: configs/beta_excel.json")
    else:
        print(f"Missing Excel file: {input_excel}")

if __name__ == "__main__":
    main()
