import json
from docx import Document
from pathlib import Path

def is_heading(paragraph):
    # paragraph is DocumentParagraph instance
    style = paragraph.style_name
    return style.startswith("Heading")

def is_list_item(paragraph):
    style = paragraph.style_name.lower()
    text = paragraph.text.strip()
    bullets = ["•", "-", "*", "–"]
    return ("list" in style) or any(text.startswith(b) for b in bullets)

def docx_to_json(docx_path):
    doc = Document(docx_path)
    result = {
        "content": []
    }

    body = doc.element.body
    for child in body.iterchildren():
        if child.tag.endswith('}p'):
            p = DocumentParagraph(child, doc)
            para_obj = {
                "type": "paragraph",
                "text": p.text,
                "style": p.style_name
            }
            if is_heading(p):
                para_obj["type"] = "heading"
                try:
                    para_obj["level"] = int(p.style_name.replace("Heading ", ""))
                except:
                    para_obj["level"] = None
            elif is_list_item(p):
                para_obj["type"] = "list_item"
            result["content"].append(para_obj)

        elif child.tag.endswith('}tbl'):
            tbl = DocumentTable(child, doc)
            table_data = []
            for row in tbl.rows:
                row_data = []
                for cell in row.cells:
                    row_data.append(cell.text.strip())
                table_data.append(row_data)
            result["content"].append({
                "type": "table",
                "data": table_data
            })

    return result

class DocumentParagraph:
    def __init__(self, element, doc):
        from docx.text.paragraph import Paragraph
        self.paragraph = Paragraph(element, doc)
        self.text = self.paragraph.text
        self.style_name = self.paragraph.style.name

class DocumentTable:
    def __init__(self, element, doc):
        from docx.table import Table
        self.table = Table(element, doc)

    @property
    def rows(self):
        return self.table.rows
