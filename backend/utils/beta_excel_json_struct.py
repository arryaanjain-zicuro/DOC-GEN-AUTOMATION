import ijson

def get_json_sample(json_path: str, num_items: int = 2):
    sample = []
    with open(json_path, 'rb') as f:
        try:
            for item in ijson.items(f, 'sheets.item'):
                sample.append(item)
                if len(sample) >= num_items:
                    break
            return sample
        except Exception as e:
            print(f"Error reading JSON sample: {e}")
            return None

def read_excel_json(json_path):
    sheets = []
    with open(json_path, 'rb') as f:
        for sheet in ijson.items(f, 'sheets.item'):
            sheets.append(sheet)
    return sheets

if __name__ == "__main__":
    sample = get_json_sample('configs/beta_excel.json', num_items=2)
    print(sample)

