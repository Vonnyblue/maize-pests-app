import re
import csv

# --- File paths ---
prolog_file = "maize_pests.v " 
csv_file = "maize.csv"     

# --- Dictionaries to store mapping ---
pests = {}
categories = {}

# --- Lists to store facts ---
facts = []

# --- Regular expressions ---
pest_pattern = re.compile(r"pest\((\w+),\s*'([^']+)'\)\.")
category_pattern = re.compile(r"category\((\w+),\s*'([^']+)'\)\.")
fact_pattern = re.compile(
    r"fact\((\d+),\s*(\w+),\s*(\w+),\s*'([^']*)',\s*'([^']*)'\)\."
)

# --- Read Prolog file ---
with open(prolog_file, "r", encoding="utf-8") as f:
    content = f.read()

# --- Extract pests ---
for match in pest_pattern.finditer(content):
    pest_atom, pest_name = match.groups()
    pests[pest_atom] = pest_name

# --- Extract categories ---
for match in category_pattern.finditer(content):
    cat_atom, cat_name = match.groups()
    categories[cat_atom] = cat_name

# --- Extract facts ---
for match in fact_pattern.finditer(content):
    fact_id, pest_atom, cat_atom, bio, damage = match.groups()
    facts.append({
        "FactID": fact_id,
        "PestAtom": pest_atom,
        "PestName": pests.get(pest_atom, ""),
        "CategoryAtom": cat_atom,
        "CategoryName": categories.get(cat_atom, ""),
        "BiologyDetail": bio,
        "DamageEffect": damage
    })

# --- Write CSV ---
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["FactID", "PestAtom", "PestName",
                                           "CategoryAtom", "CategoryName",
                                           "BiologyDetail", "DamageEffect"])
    writer.writeheader()
    for fact in facts:
        writer.writerow(fact)

print(f"CSV file created: {csv_file} ({len(facts)} facts)")
