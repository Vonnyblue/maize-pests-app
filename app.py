# import re
# import csv

# # --- File paths ---
# prolog_file = "maize_pests.v " 
# csv_file = "maize.csv"     

# # --- Dictionaries to store mapping ---
# pests = {}
# categories = {}

# # --- Lists to store facts ---
# facts = []

# # --- Regular expressions ---
# pest_pattern = re.compile(r"pest\((\w+),\s*'([^']+)'\)\.")
# category_pattern = re.compile(r"category\((\w+),\s*'([^']+)'\)\.")
# fact_pattern = re.compile(
#     r"fact\((\d+),\s*(\w+),\s*(\w+),\s*'([^']*)',\s*'([^']*)'\)\."
# )

# # --- Read Prolog file ---
# with open(prolog_file, "r", encoding="utf-8") as f:
#     content = f.read()

# # --- Extract pests ---
# for match in pest_pattern.finditer(content):
#     pest_atom, pest_name = match.groups()
#     pests[pest_atom] = pest_name

# # --- Extract categories ---
# for match in category_pattern.finditer(content):
#     cat_atom, cat_name = match.groups()
#     categories[cat_atom] = cat_name

# # --- Extract facts ---
# for match in fact_pattern.finditer(content):
#     fact_id, pest_atom, cat_atom, bio, damage = match.groups()
#     facts.append({
#         "FactID": fact_id,
#         "PestAtom": pest_atom,
#         "PestName": pests.get(pest_atom, ""),
#         "CategoryAtom": cat_atom,
#         "CategoryName": categories.get(cat_atom, ""),
#         "BiologyDetail": bio,
#         "DamageEffect": damage
#     })

# # --- Write CSV ---
# with open(csv_file, "w", newline="", encoding="utf-8") as f:
#     writer = csv.DictWriter(f, fieldnames=["FactID", "PestAtom", "PestName",
#                                            "CategoryAtom", "CategoryName",
#                                            "BiologyDetail", "DamageEffect"])
#     writer.writeheader()
#     for fact in facts:
#         writer.writerow(fact)

# print(f"CSV file created: {csv_file} ({len(facts)} facts)")
import streamlit as st
import pandas as pd
import re
import os

st.set_page_config(page_title="Maize Pest Knowledge Base", layout="wide")
st.title("🌽 Maize Pest and Disease Knowledge Base")

# --- Locate the Prolog file safely ---
prolog_file = os.path.join(os.path.dirname(__file__), "maize_pests.v")

# --- Function to parse facts from .v file ---
def parse_prolog_file(file_path):
    """
    Reads the Prolog .v file and extracts facts into a list of dictionaries.
    Each dictionary corresponds to a fact:
    {'ID', 'Pest', 'Category', 'BiologyDetail', 'DamageEffect'}
    """
    pattern = re.compile(
        r"fact\((\d+),\s*(\w+),\s*(\w+),\s*'(.*?)',\s*'(.*?)'\s*\)\.",
        re.DOTALL
    )
    facts = []

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = pattern.findall(content)
    for match in matches:
        fact_id, pest, category, bio, damage = match
        facts.append({
            "ID": int(fact_id),
            "Pest/Disease": pest.replace("_", " ").title(),
            "Category": category.replace("_", " ").title(),
            "Biology / Symptoms": bio,
            "Damage / Effects": damage
        })

    return pd.DataFrame(facts)

# --- Load facts ---
try:
    df_facts = parse_prolog_file(prolog_file)
except FileNotFoundError:
    st.error(f"Cannot find {prolog_file}. Make sure it exists in the repo folder.")
    st.stop()

# --- Sidebar filters ---
st.sidebar.header("Filters")
categories = ["All"] + sorted(df_facts["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

pests = ["All"] + sorted(df_facts["Pest/Disease"].unique().tolist())
selected_pest = st.sidebar.selectbox("Select Pest/Disease", pests)

# --- Apply filters ---
df_display = df_facts.copy()

if selected_category != "All":
    df_display = df_display[df_display["Category"] == selected_category]

if selected_pest != "All":
    df_display = df_display[df_display["Pest/Disease"] == selected_pest]

# --- Search box ---
search_text = st.sidebar.text_input("Search in Biology/Symptoms or Damage/Effects")

if search_text:
    df_display = df_display[
        df_display["Biology / Symptoms"].str.contains(search_text, case=False) |
        df_display["Damage / Effects"].str.contains(search_text, case=False)
    ]

# --- Display table ---
st.dataframe(df_display.reset_index(drop=True), use_container_width=True)

# --- Optional: Download filtered CSV ---
csv = df_display.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_maize_pests.csv",
    mime="text/csv"
)
