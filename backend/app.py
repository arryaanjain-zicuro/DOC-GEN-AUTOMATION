from flask import Flask, jsonify, render_template_string
import json
from pathlib import Path

app = Flask(__name__)

CONFIGS_DIR = Path(__file__).parent / "configs"

def load_json(file_name):
    file_path = CONFIGS_DIR / file_name
    if not file_path.exists():
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{ title }}</title>
  <style>
    body { font-family: monospace; white-space: pre-wrap; background: #f9f9f9; padding: 20px; }
    .container { max-width: 1000px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
  </style>
</head>
<body>
  <div class="container">
    <h2>{{ title }}</h2>
    <pre>{{ content }}</pre>
  </div>
</body>
</html>
"""

@app.route("/alpha")
def view_alpha_json():
    data = load_json("alpha_doc.json")
    if data is None:
        return "alpha_doc.json not found", 404
    pretty = json.dumps(data, indent=2, ensure_ascii=False)
    return render_template_string(HTML_TEMPLATE, title="Alpha DOC JSON", content=pretty)

@app.route("/beta")
def view_beta_json():
    data = load_json("beta_excel.json")
    if data is None:
        return "beta_excel.json not found", 404
    pretty = json.dumps(data, indent=2, ensure_ascii=False)
    return render_template_string(HTML_TEMPLATE, title="Beta Excel JSON", content=pretty)

@app.route("/")
def index():
    return '''
    <h3>JSON Viewer</h3>
    <ul>
      <li><a href="/alpha">View Alpha DOC JSON</a></li>
      <li><a href="/beta">View Beta Excel JSON</a></li>
    </ul>
    '''

if __name__ == "__main__":
    app.run(debug=True)
