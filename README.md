API REST - Scraping Annonces Immobilières

Ce projet est une API REST développée en Python avec Flask. Elle permet de scraper les annonces immobilières du site tunisie-annonce.com, de filtrer celles publiées à partir du 1er janvier 2025, et de les mettre à disposition via une API.


📚 Installation

1. Cloner le dépôt
git clone https://github.com/aichajebri/Python-project-part1
cd ton-repo
2. Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
3. Installer les dépendances
pip install -r requirements.txt
4. Lancer l'application
python app.py
L'application sera disponible sur http://127.0.0.1:5000


📍 Endpoints de l'API

POST /scrape
Lance une session de scraping
Récupère les annonces immobilières publiées après le 01/01/2025
Sauvegarde les résultats dans annonces_2025.json et annonces_tunisie_2025.csv
Exemple avec curl
curl.exe -X POST http://127.0.0.1:5000/scrape

GET /annonces
Retourne toutes les annonces collectées au format JSON
Exemple avec curl
curl http://127.0.0.1:5000/annonces

📚 Fichiers générés

annonces_tunisie_2025.csv : fichier contenant toutes les annonces au format tabulaire
annonces_2025.json : fichier JSON utilisé par l'API pour le GET /annonces


📁 Contenu d'une annonce

Chaque annonce contient :

Titre
Lien
Adresse
Prix
Surface
Description
Date d'insertion ("Insérée le")
Contact
💼 Requirements
Le fichier requirements.txt contient :

flask
requests
beautifulsoup4
Tu peux le générer automatiquement avec :

pip freeze > requirements.txt


📅 Auteur

Projet réalisé dans le cadre d'un projet de Python for Data Science.

-Aicha Jebri
-Ons Hamouda
-Yasmine Messaoudi
