from flask import Flask, jsonify, request
from scraper import scrape_annonces  # <-- on mettra le scraping dans un fichier à part
import os
import json

app = Flask(__name__)

DATA_FILE = "annonces_2025.json"

@app.route('/annonces', methods=['GET'])
def get_annonces():
    if not os.path.exists(DATA_FILE):
        return jsonify([])

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)
    return jsonify(data)

@app.route('/scrape', methods=['POST'])
def post_scrape():
    annonces = scrape_annonces()
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(annonces, file, ensure_ascii=False, indent=2)
    return jsonify({"message": "Scraping terminé", "total": len(annonces)}), 201


if __name__ == '__main__':
    app.run(debug=True)