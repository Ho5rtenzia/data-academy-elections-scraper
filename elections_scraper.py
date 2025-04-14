"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Eva Vallušová
email: eva.vallusova@gmail.com
discord: energetic_avocado_65638
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
from typing import List, Tuple, Dict

base_url = "https://www.volby.cz/pls/ps2017nss/"


def is_valid_url(url: str) -> bool:
    """
    Verifies that the specified URL is from the volby.cz domain and contains xjazyk=CZ.
    """
    return url.startswith(base_url) and "xjazyk=CZ" in url


def get_soup(url: str) -> BeautifulSoup:
    """
    Downloads the HTML page and returns it as a BeautifulSoup object.
    Includes basic exception handling for network issues.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = "utf-8"
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error: Failed to load URL {url} – {e}")
        sys.exit(1)


def clean_number(value: str) -> str:
    """
    Removes non-breaking and normal spaces from number strings.
    """
    return value.replace("\xa0", "").replace(" ", "")


def get_municipality_links_and_info(soup: BeautifulSoup) -> List[Tuple[str, str, str]]:
    """
    Returns a list of municipalities in [(code, name, detail URL)] format 
    from the landing page.
    """
    data = []
    for tr in soup.find_all("tr")[2:]:
        tds = tr.find_all("td")
        if len(tds) >= 2:
            a_tag = tds[0].find("a")
            if a_tag and "href" in a_tag.attrs:
                kod_obce = a_tag.text.strip()
                nazev_obce = tds[1].text.strip()
                link = base_url + a_tag["href"]
                data.append((kod_obce, nazev_obce, link))
    return data


def extract_main_numbers(soup: BeautifulSoup) -> Tuple[str, str, str]:
    """
    Returns 3 main numbers from the table: (voters on the list, 
    envelopes issued, valid votes)
    """
    try:
        table = soup.find("table", {"id": "ps311_t1"})
        row = table.find_all("tr")[2]
        tds = row.find_all("td")
        voters = clean_number(tds[3].text.strip())
        envelopes = clean_number(tds[4].text.strip())
        valid_votes = clean_number(tds[7].text.strip())
        return voters, envelopes, valid_votes
    except Exception:
        return "", "", ""


def extract_party_votes_dict(soup: BeautifulSoup) -> Dict[str, str]:
    """
    Returns the dictionary {party name: number of votes} 
    from the tables on the page.
    """
    votes = {}
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            columns = row.find_all("td")
            if len(columns) >= 3:
                name_td = row.find("td", class_="overflow_name")
                if name_td:
                    name = name_td.text.strip()
                    vote_td = clean_number(columns[2].text.strip())
                    if name and vote_td.isdigit():
                        votes[name] = vote_td
    return votes


def extract_party_names(soup: BeautifulSoup) -> List[str]:
    """
    Returns a list of page names in the correct order for the CSV header.
    """
    return list(extract_party_votes_dict(soup).keys())


def scrape_municipality_data(
    code: str, name_municipality: str, detail_url: str, party_names: List[str]
) -> List:
    """
    Returns a list of data for one municipality: 
    [code, name, voters, envelopes, valid votes, ...votes for each party]
    Converts vote numbers to integers.
    """
    soup = get_soup(detail_url)
    voters, envelopes, valid_votes = extract_main_numbers(soup)
    party_votes = extract_party_votes_dict(soup)
    votes = [int(party_votes.get(name, 0)) for name in party_names]
    return [
        code,
        name_municipality,
        int(voters),
        int(envelopes),
        int(valid_votes),
    ] + votes


def main():
    if len(sys.argv) != 3:
        print("Error: Specify exactly 2 arguments: [URL] [filename.csv]")
        return

    url, output_file = sys.argv[1], sys.argv[2]

    if not is_valid_url(url):
        print(
            "Error: Invalid link. Must be from the domain volby.cz and contain the parameter xjazyk=CZ"
        )
        return

    print("Loading the main page...")
    main_soup = get_soup(url)
    municipality_data = get_municipality_links_and_info(main_soup)

    if not municipality_data:
        print("Error: No references to municipalities found.")
        return

    print(
        f"Found {len(municipality_data)} municipalities. I'm checking candidate parties..."
    )
    party_names = extract_party_names(get_soup(municipality_data[0][2]))
    header = ["code", "location", "registered", "envelopes", "valid"] + party_names

    print("I'm processing the results...")
    with open(output_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(header)

        for code, name, link in municipality_data:
            row = scrape_municipality_data(code, name, link, party_names)
            writer.writerow(row)

    print(f"Done! The results have been saved to a file: {output_file}")


if __name__ == "__main__":
    main()
