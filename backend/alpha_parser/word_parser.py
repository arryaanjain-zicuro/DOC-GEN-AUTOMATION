from docx import Document

#not in use rn
def parse_term_sheet(path: str) -> dict:
    doc = Document(path)
    data = {}

    for para in doc.paragraphs:
        text = para.text.strip()
        if "Security Name" in text:
            data["Security Name"] = text.split("Security Name")[-1].strip(": ").strip()
        elif "Issuer" in text:
            data["Issuer"] = text.split("Issuer")[-1].strip(": ").strip()
        elif "Initial Fixing Date" in text:
            data["Initial Fixing Date"] = text.split("Initial Fixing Date")[-1].strip()
        elif "Final Fixing Date" in text:
            data["Final Fixing Date"] = text.split("Final Fixing Date")[-1].strip()
        elif "Participation Rate" in text:
            data["Participation Rate"] = text.split("Participation Rate")[-1].strip()
        elif "Face Value" in text:
            data["Face Value"] = text.split("Face Value")[-1].strip()
        elif "Issue Size" in text:
            data["Issue Size"] = text.split("Issue Size")[-1].strip()

    return data
