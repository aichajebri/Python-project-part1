import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd
import time


def scrape_annonces():
    base_url = "http://www.tunisie-annonce.com/"
    url = "AnnoncesImmobilier.asp"
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    date_limite = datetime(2025, 1, 1)

    annonces_liste = []
    page_count = 1

    while url:
        full_url = base_url + url
        print(f"🔄 Scraping page {page_count}: {full_url}")

        response = session.get(full_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        annonces = soup.find_all("a", href=True)

        for annonce in annonces:
            titre = annonce.text.strip()
            lien = annonce["href"]

            if "DetailsAnnonceImmobilier.asp?cod_ann=" in lien:
                ann_url = base_url + lien
                detail_response = session.get(ann_url, headers=headers)
                detail_soup = BeautifulSoup(detail_response.text, "html.parser")

                adresse = prix = surface = description = contact = "Non trouvé"
                date_insertion = "Non trouvée"

                contact_span = detail_soup.find("span", class_="da_contact_value")
                if contact_span:
                    contact = contact_span.text.strip()

                label_cells = detail_soup.find_all("td", class_="da_label_field")
                for label in label_cells:
                    label_text = label.text.strip()
                    value_cell = label.find_next_sibling("td", class_="da_field_text")
                    if not value_cell:
                        continue

                    if label_text == "Adresse":
                        adresse = value_cell.text.strip()
                    elif label_text == "Prix":
                        prix = value_cell.text.strip()
                    elif label_text == "Surface":
                        surface = value_cell.text.strip()
                    elif label_text == "Texte":
                        description = value_cell.text.strip()
                    elif label_text == "Insérée le":
                        date_insertion = value_cell.text.strip()

                try:
                    date_obj = datetime.strptime(date_insertion, "%d/%m/%Y")
                    if date_obj < date_limite:
                        continue
                except:
                    continue

                annonces_liste.append({
                    "Titre": titre,
                    "Lien": ann_url,
                    "Adresse": adresse,
                    "Prix": prix,
                    "Surface": surface,
                    "Description": description,
                    "Insérée le": date_insertion,
                    "Contact": contact
                })

                time.sleep(0.5)

        next_page = soup.find("img", {"src": "/images/n_next.gif"})
        if next_page:
            next_link = next_page.find_parent("a")
            url = next_link["href"] if next_link and "href" in next_link.attrs else None
        else:
            url = None

    return annonces_liste


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    data = scrape_annonces()
    df = pd.DataFrame(data)
    df.to_csv("data/annonces.csv", index=False, encoding="utf-8-sig")
