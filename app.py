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
import os

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Maize Pest Knowledge Base", layout="wide")
st.title("🌽 Maize Pest and Their Effects on Plants Knowledge Base")

# -----------------------------
# Load CSV file safely
# -----------------------------
csv_file = os.path.join(os.path.dirname(__file__), "maize.csv")
#  Load CSV into DataFrame
df_facts = pd.read_csv(csv_file)

try:
    df_facts = pd.read_csv(csv_file)
except FileNotFoundError:
    st.error(f"Cannot find {csv_file}. Make sure it exists in the same folder as app.py.")
    st.stop()

# Ensure required columns exist
required_columns = ["FactID", "PestAtom", "PestName", "CategoryAtom", "CategoryName", "BiologyDetail", "DamageEffect"]
for col in required_columns:
    if col not in df_facts.columns:
        st.error(f"Column '{col}' is missing from the CSV file.")
        st.stop()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# Category filter
categories = ["All"] + sorted(df_facts["CategoryName"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Pest/ filter
pests = ["All"] + sorted(df_facts["PestName"].unique().tolist())
selected_pest = st.sidebar.selectbox("Select Pest", pests)

# Search box
search_text = st.sidebar.text_input("Search in BiologyDetail or DamageEffect")

# -----------------------------
# Apply filters
# -----------------------------
df_display = df_facts.copy()
df_facts.columns = df_facts.columns.str.strip()

if selected_category != "All":
    df_display = df_display[df_display["CategoryName"] == selected_category]

if selected_pest != "All":
    df_display = df_display[df_display["PestName"] == selected_pest]

if search_text:
    df_display = df_display[
        df_display["BiologyDetail"].str.contains(search_text, case=False, na=False) |
        df_display["DamageEffect"].str.contains(search_text, case=False, na=False)
    ]

# -----------------------------
# Display filtered table
# -----------------------------
st.dataframe(df_display.reset_index(drop=True), use_container_width=True)

# -----------------------------
# Download filtered CSV
# -----------------------------
csv = df_display.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_maize_pests.csv",
    mime="text/csv"
)

