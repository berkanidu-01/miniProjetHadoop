#!/usr/bin/env python3
# post_processor.py
import sys
import csv
from collections import defaultdict

# Structure for per-year-gender top 5: { (année, sexe): [ (prénom, total_nombre_for_that_year_gender), ... ] }
grouped_data = defaultdict(list)

# Structure for overall top 5: { prénom: total_nombre_overall }
overall_name_counts = defaultdict(int)

# Input format: année_sexe_prénom \t total_nombre
for line in sys.stdin:
    line = line.strip()
    try:
        key_part, total_nombre_str = line.split('\t')
        annais, sexe, prenom = key_part.split('_', 2)
        total_nombre = int(total_nombre_str)
    except ValueError as e:
        sys.stderr.write(f"Erreur de parsing ligne: {line} - {e}\n")
        continue
        
    # For per-year-gender grouping
    grouped_data[(annais, sexe)].append((prenom, total_nombre))
    
    # For overall name counting
    overall_name_counts[prenom] += total_nombre

# --- Processing and writing top 5 names by year and gender ---
# Sort group keys by (année, sexe)
sorted_group_keys = sorted(grouped_data.keys(), key=lambda x: (x[0], x[1]))

# Open CSV file for writing
with open("top_names_by_year_and_gender.csv", "w", newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Année", "Sexe", "Rang", "Prénom", "Total"])

    for annais, sexe in sorted_group_keys:
        names_in_group = grouped_data[(annais, sexe)]
        # Sort names within group by total_nombre (desc) then prenom (asc for ties)
        sorted_names = sorted(names_in_group, key=lambda x: (-x[1], x[0]))
        
        sexe_str = "Masculin" if sexe == "1" else "Féminin" if sexe == "2" else f"Inconnu ({sexe})"
        
        for i, (prenom, total_nombre) in enumerate(sorted_names[:5]): # Top 5 for this group
            writer.writerow([annais, sexe_str, i + 1, prenom, total_nombre])

sys.stderr.write("Fichier 'top_names_by_year_and_gender.csv' généré.\n")

# --- Processing and printing overall top 5 names ---
print("\n--- Top 5 des prénoms (toutes années et sexes confondus) ---")

# Sort overall names by total_nombre (desc) then prenom (asc for ties)
# .items() gives a list of (key, value) tuples
sorted_overall_names = sorted(overall_name_counts.items(), key=lambda item: (-item[1], item[0]))

for i, (prenom, total_nombre) in enumerate(sorted_overall_names[:5]): # Top 5 overall
    print(f"{i + 1}. {prenom}: {total_nombre}")