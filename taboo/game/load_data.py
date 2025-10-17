import json
from pathlib import Path

path_to_data = Path(__file__).parent.parent / 'taboo_words.json'

with open(path_to_data, encoding='utf-8') as file:
    data = json.load(file)

data_formatted = []

for idx, item in enumerate(data, start=1):
    data_formatted.append(
        {
            "pk": idx,
            "model": "game.Word",
            "fields": item
        }
    )

formatted_data_path = Path(__file__).parent.parent / "taboo_words_formatted.json"
with open(formatted_data_path, 'w', encoding='utf-8') as file:
    json.dump(data_formatted, file, ensure_ascii=False, indent=4)
