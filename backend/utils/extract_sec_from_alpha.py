import re
from datetime import datetime

#helper function for extract_securityy_info_from_alpha_json
def extract_keywords_from_text(text: str, keywords: list[str]) -> list[str]:
    extracted = []
    for kw in keywords:
        # Use word boundary regex, case-insensitive
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, text, re.IGNORECASE):
            extracted.append(kw)
    return extracted

def extract_security_info_from_alpha_json(alpha_json: dict):
    keywords_to_extract = ["Secured", "Unsecured", "Listed", "Unlisted", "Rated", "Unrated"]

    extracted_keywords = []
    raw_description = ""
    year_for_sheet = ""
    sheet_name = ""
    date_found = None

    # Date fields to check
    date_fields = [
        "Issue Opening Date",
        "Issue Closing Date",
        "Pay-in-Date",
        "Date of Allotment",
        "Deemed Date of Allotment"
    ]

    tables = [block["data"] for block in alpha_json.get("content", []) if block.get("type") == "table"]

    # Look for Security Name row and extract description & keywords
    for table in tables:
        for row in table:
            if len(row) >= 2 and isinstance(row[1], str) and "Security Name" in row[1]:
                raw_description = row[2] if len(row) >= 3 else ""
                extracted_keywords = extract_keywords_from_text(raw_description, keywords_to_extract)

    # Now extract dates from the date fields (first non-empty valid date)
    for table in tables:
        for row in table:
            if len(row) >= 2 and isinstance(row[1], str):
                field_name = row[1].strip()
                if field_name in date_fields:
                    date_str = row[2].strip() if len(row) >= 3 else ""
                    if date_str:
                        try:
                            # Parse dates of format: "April 09, 2025"
                            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
                            # Calculate financial year (Indian FY Apr-Mar)
                            fy_start = parsed_date.year if parsed_date.month >= 4 else parsed_date.year - 1
                            fy_end = fy_start + 1
                            year_for_sheet = f"{str(fy_start)[-2:]}-{str(fy_end)[-2:]}"
                            date_found = parsed_date.strftime("%Y-%m-%d")
                            break  # Found a valid date, exit inner loop
                        except ValueError:
                            continue
        if date_found:
            break  # Exit outer loop if date found

    prefix = "secured" if "Secured" in extracted_keywords else \
             "unsecured" if "Unsecured" in extracted_keywords else \
             "general"

    sheet_name = f"{prefix} {year_for_sheet}" if year_for_sheet else prefix

    return {
        "security_description": raw_description,
        "keywords": extracted_keywords,
        "sheet_name": sheet_name,
        "date_found": date_found
    }

def extract_series_from_product_code(alpha_json: dict) -> str:
    """
    Searches alpha_json for 'Product Code', extracts the product code string,
    then extracts and returns the 'Series' part like 'Series 129'.
    Returns empty string if not found.
    """
    tables = [block["data"] for block in alpha_json.get("content", []) if block.get("type") == "table"]

    for table in tables:
        for row in table:
            if len(row) >= 2 and isinstance(row[1], str) and "Product Code" in row[1]:
                product_code = row[2].strip() if len(row) >= 3 else ""
                match = re.search(r"(Series\s*\d+)", product_code, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
                else:
                    return ""
    return ""

import re

def extract_issue_size_details(alpha_json: dict) -> dict:
    """
    Extract numeric details from the Issue Size field in alpha_json.
    
    Returns a dict with keys:
    - units (int)
    - face_value (int)
    - issue_price (int)
    - total_amount (int)
    - nominal_value (int) calculated as units * face_value
    Returns empty dict if Issue Size not found or parsing fails.
    """
    issue_size_label = "Issue Size"
    tables = [block["data"] for block in alpha_json.get("content", []) if block.get("type") == "table"]
    
    issue_text = ""
    # Find the row for Issue Size and get the text (usually 3rd column)
    for table in tables:
        for row in table:
            if len(row) >= 2 and isinstance(row[1], str) and row[1].strip() == issue_size_label:
                issue_text = row[2].strip() if len(row) >= 3 else ""
                break
        if issue_text:
            break

    if not issue_text:
        return {}

    # Regex pattern to extract required numbers (with commas)
    pattern = (
        r"(\d+)\s*\(.*?\)\s*Debentures.*?face value of Rs\.\s*([\d,]+)/-.*?"
        r"issued at Rs\.([\d,]+)/-.*?total amounting to Rs\.([\d,]+)/-"
    )
    match = re.search(pattern, issue_text, re.IGNORECASE | re.DOTALL)
    
    if not match:
        return {}

    try:
        units = int(match.group(1).replace(",", ""))
        face_value = int(match.group(2).replace(",", ""))
        issue_price = int(match.group(3).replace(",", ""))
        total_amount = int(match.group(4).replace(",", ""))
        nominal_value = units * face_value

        return {
            "units": units,
            "face_value": face_value,
            "issue_price": issue_price,
            "total_amount": total_amount,
            "nominal_value": nominal_value
        }
    except Exception:
        return {}

def extract_underlying(alpha_json: dict) -> str:
    """
    Extracts the 'Underlying' field value from alpha_json tables.
    
    Returns the string value if found, else empty string.
    """
    tables = [block["data"] for block in alpha_json.get("content", []) if block.get("type") == "table"]

    for table in tables:
        for row in table:
             for i, cell in enumerate(row):
                if isinstance(cell, str) and cell.strip().lower() == "underlying":
                    # Return next cell if exists
                    if i + 1 < len(row):
                        return row[i + 1].strip()
                    else:
                        return ""
    return ""

def extract_date_of_maturity(alpha_json: dict) -> str:
    """
    Extracts the value corresponding to 'Coupon / Dividend payment dates' from tables
    in the alpha_json and returns it as 'Date Of Maturity'.
    """
    target_field = "Coupon / Dividend payment dates"
    tables = [block["data"] for block in alpha_json.get("content", []) if block.get("type") == "table"]

    for table in tables:
        for row in table:
            for i, cell in enumerate(row):
                if isinstance(cell, str) and cell.strip().lower() == target_field.lower():
                    # Return the next cell if exists
                    if i + 1 < len(row):
                        return row[i + 1].strip()
                    else:
                        return ""
    return ""

