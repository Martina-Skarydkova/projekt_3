"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Martina Škarydková
email: mskarydkova@gmail.com
"""

import sys
import csv
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# Globální zásobníky
registered_voters = []
envelopes_issued = []
valid_votes = []

def fetch_html(url, max_attempts=3, wait_time=2):
    for attempt in range(max_attempts):
        try:
            print(f"Načítání dat z: {url}")
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            return BeautifulSoup(resp.text, "html.parser")
        except RequestException as error:
            print(f"Chyba při přístupu k {url}: {error}")
            if attempt < max_attempts - 1:
                print(f"Zkouším znovu za {wait_time} sekund... ({attempt + 1}/{max_attempts})")
                time.sleep(wait_time)
            else:
                print("Překročen počet pokusů.")
                raise

if len(sys.argv) != 3:
    print("Použití: python skript.py \"URL\" výstup.csv")
    sys.exit(1)

main_html = fetch_html(sys.argv[1])

def extract_municipalities():
    return [cell.text for cell in main_html.select("td.overflow_name")]

def extract_codes():
    return [cell.text for cell in main_html.select("td.cislo")]

def extract_subpages():
    base = "https://volby.cz/pls/ps2017nss/"
    return [base + link.a["href"] for link in main_html.select("td.cislo") if link.a]

def fetch_party_names():
    detail_url = extract_subpages()[0]
    detail_html = fetch_html(detail_url)
    return [party.text for party in detail_html.select("td.overflow_name")]

def aggregate_voter_stats():
    for url in extract_subpages():
        detail = fetch_html(url)
        registered = detail.select_one("td[headers='sa2']")
        envelopes = detail.select_one("td[headers='sa3']")
        valid = detail.select_one("td[headers='sa6']")
        registered_voters.append(registered.text.replace('\xa0', ' ') if registered else "")
        envelopes_issued.append(envelopes.text.replace('\xa0', ' ') if envelopes else "")
        valid_votes.append(valid.text.replace('\xa0', ' ') if valid else "")
        time.sleep(1)

def extract_vote_data():
    results = []
    for url in extract_subpages():
        page = fetch_html(url)
        vote_cells = page.find_all("td", class_="cislo", headers=["t1sb4", "t2sb4"])
        row = [cell.text + " %" for cell in vote_cells]
        results.append(row)
        time.sleep(1)
    return results

def build_data_matrix():
    aggregate_voter_stats()
    codes = extract_codes()
    towns = extract_municipalities()
    votes = extract_vote_data()
    final_rows = []

    for meta, result in zip(zip(codes, towns, registered_voters, envelopes_issued, valid_votes), votes):
        final_rows.append(list(meta) + result)

    return final_rows

def export_to_csv(source_url, output_path):
    try:
        header = ["Obecní kód", "Název", "Registrovaní", "Obálky vydané", "Platné hlasy"]
        header += fetch_party_names()
        print(f"Ukládám výsledky do: {output_path}")
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(build_data_matrix())
        print("Export dokončen.")
    except Exception as e:
        print(f"Nastala chyba: {e}")
        sys.exit(1)

if __name__ == "__main__":
    export_to_csv(sys.argv[1], sys.argv[2])
