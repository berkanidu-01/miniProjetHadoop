#!/usr/bin/env python3
# post_processor_html.py
import sys
import json
from collections import defaultdict

# Structures
# grouped_data[(annee, sexe)] = list of (prenom, total)
grouped_data = defaultdict(list)
# Read input: annee_sexe_prenom \t total
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        key_part, total_str = line.split('\t')
        annee, sexe, prenom = key_part.split('_', 2)
        total = int(total_str)
    except ValueError as e:
        sys.stderr.write(f"Erreur parsing ligne: {line} -> {e}\n")
        continue
    grouped_data[(annee, sexe)].append((prenom, total))

# Prepare top 5 per year & gender
top5 = {}  # { annee: { sexe_label: [ {prenom, total}, ... ] } }
for (annee, sexe), names in grouped_data.items():
    # sort by total desc, then prenom asc
    sorted_names = sorted(names, key=lambda x: (-x[1], x[0]))[:5]
    sexe_label = 'Masculin' if sexe == '1' else 'Féminin' if sexe == '2' else f'Inconnu({sexe})'
    top5.setdefault(annee, {})[sexe_label] = [ {'prenom': p, 'total': t} for p, t in sorted_names ]

# Generate HTML with filters
html = []
html.append('<!DOCTYPE html>')
html.append('<html lang="fr">')
html.append('<head>')
html.append('  <meta charset="UTF-8">')
html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
html.append('  <title>Top 5 prénoms par année et sexe</title>')
html.append('  <style>')
html.append('    body { font-family: Arial, sans-serif; margin: 20px; }')
html.append('    select { margin-right: 10px; padding: 5px; }')
html.append('    table { border-collapse: collapse; width: 50%; margin-top: 20px; }')
html.append('    th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }')
html.append('    th { background: #f4f4f4; }')
html.append('  </style>')
html.append('</head>')
html.append('<body>')
html.append('  <h1>Top 5 prénoms par année et sexe</h1>')
# Filter controls
years = sorted(top5.keys())
genders = set()
for g in top5.values():
    genders.update(g.keys())
html.append('  <div>')
html.append('    <label for="yearSelect">Année:</label>')
html.append('    <select id="yearSelect"></select>')
html.append('    <label for="genderSelect">Sexe:</label>')
html.append('    <select id="genderSelect"></select>')
html.append('  </div>')
# Table placeholder
html.append('  <table id="resultsTable">')
html.append('    <thead>')
html.append('      <tr><th>Rang</th><th>Prénom</th><th>Total</th></tr>')
html.append('    </thead>')
html.append('    <tbody></tbody>')
html.append('  </table>')
# Embed data as JSON
html.append('  <script>')
html.append('    const data = ' + json.dumps(top5, ensure_ascii=False) + ';')
html.append('    const yearSel = document.getElementById("yearSelect");')
html.append('    const genderSel = document.getElementById("genderSelect");')
html.append('    const tableBody = document.querySelector("#resultsTable tbody");')
# Populate dropdowns
html.append('    // fill year options');
html.append('    Object.keys(data).sort().forEach(year => {')
html.append('      const opt = document.createElement("option"); opt.value = year; opt.textContent = year; yearSel.appendChild(opt);')
html.append('    });')
html.append('    // fill gender options based on first year');
html.append('    function updateGenderOptions(){')
html.append('      genderSel.innerHTML = "";')
html.append('      const yr = yearSel.value;')
html.append('      const genders = Object.keys(data[yr] || {});')
html.append('      genders.forEach(g => {')
html.append('        const opt = document.createElement("option"); opt.value = g; opt.textContent = g; genderSel.appendChild(opt);')
html.append('      });')
html.append('    }')
# Function to update table
html.append('    function updateTable(){')
html.append('      tableBody.innerHTML = "";')
html.append('      const yr = yearSel.value;')
html.append('      const g = genderSel.value;')
html.append('      const list = (data[yr] && data[yr][g]) || [];')
html.append('      list.forEach((item, idx) => {')
html.append('        const row = document.createElement("tr");')
html.append('        row.innerHTML = `<td>${idx+1}</td><td>${item.prenom}</td><td>${item.total}</td>`;')
html.append('        tableBody.appendChild(row);')
html.append('      });')
html.append('    }')
# Event listeners
html.append('    yearSel.addEventListener("change", () => { updateGenderOptions(); updateTable(); });')
html.append('    genderSel.addEventListener("change", updateTable);')
# Initialize UI
html.append('    // init');
html.append('    updateGenderOptions();')
html.append('    updateTable();')
html.append('  </script>')
html.append('</body>')
html.append('</html>')

# Write to file
with open("top_names.html", "w", encoding="utf-8") as f:
    f.write("\n".join(html))
sys.stderr.write("Fichier 'top_names.html' généré.\n")
