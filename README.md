# Elections Scraper – Stažení volebních výsledků z roku 2017

TTento projekt je vypracováním úkolu pro Engeto Academy, kde vytvářím scraper, který automatizovaně stahuje a ukládá výsledky voleb do Poslanecké sněmovny ČR z roku 2017 přímo z oficiálního webu [volby.cz](https://www.volby.cz).

## Popis programu

Program stáhne výsledky hlasování pro všechny obce vybraného územního celku (např. okres) a uloží je do `.csv` souboru.

Vstupem je:
- **1. argument** – URL adresa konkrétního územního celku z webu [volby.cz](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) (např. Benešov) 
- **2. argument** – název výstupního souboru


### Co program umí

- Ověří správnost zadané URL adresy
- Stáhne seznam všech obcí daného celku
- Pro každou obec:
  - Získá počet registrovaných voličů, vydaných obálek a platných hlasů
  - Získá počet hlasů pro každou kandidující stranu
- Vygeneruje `.csv` soubor se strukturovanými výsledky

Výstupní CSV obsahuje:
- Kód obce
- Název obce
- Registrovaní voliči
- Vydané obálky
- Platné hlasy
- Hlasování pro jednotlivé politické strany

Ukázka výstupu (`vysledky_benesov.csv`):

| code   | location        | registered | envelopes | valid | ANO 2011 | ČSSD | ODS | ... |
|--------|------------------|------------|-----------|-------|----------|------|-----|-----|
| 529303 | Bystřice         | 3600       | 2400      | 2350  | 1025     | 320  | 450 | ... |
| 529311 | Čechtice         | 890        | 650       | 645   | 220      | 150  | 115 | ... |

## Instalace

1. **Naklonujte repozitář:**

```bash
git clone https://github.com/Ho5rtenzia/data-academy-elections-scraper.git cd data-academy-elections-scraper
```

2. **Vytvořte virtuální prostředí (doporučeno):**
```bash
python -m venv venv source venv/bin/activate # na Windows: venv\Scripts\activate
```

3. **Nainstalujte potřebné knihovny:**
```bash
pip install -r requirements.txt
```

## Spuštění programu

Program spouštíte z příkazové řádky:
```bash
python elections_scraper.py [URL_adresa_uzemniho_celku] [nazev_vystupniho_csv]
```

### Příklad:
```bash
python elections_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"
```

## Struktura projektu
Projekt obsahuje následující soubory:

```
data-academy-elections-scraper/
├── elections_scraper.py              # Hlavní skript programu
├── requirements.txt                  # Přehled knihoven
├── vysledky_benesov.csv              # Ukázka výstupního soubor


## Autor

**Eva Vallušová**  




