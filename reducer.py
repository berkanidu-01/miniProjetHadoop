#!/usr/bin/env python3
# reducer.py
import sys

current_key = None
current_sum = 0

# L'entrée est triée par clé (année_sexe_prénom)
for line in sys.stdin:
    line = line.strip()
    
    try:
        key, value_str = line.split('\t', 1)
    except ValueError:
        # Ligne mal formée, ignorer
        sys.stderr.write(f"Erreur: Ligne mal formée: {line}\n")
        continue

    try:
        count = int(value_str)
    except ValueError:
        # Valeur non entière, ignorer
        sys.stderr.write(f"Erreur: Valeur non entière '{value_str}' pour la clé '{key}'\n")
        continue

    if current_key == key:
        current_sum += count
    else:
        if current_key:
            # Écrire le résultat pour la clé précédente
            print(f"{current_key}\t{current_sum}")
        current_key = key
        current_sum = count

# Ne pas oublier d'écrire la dernière clé traitée
if current_key:
    print(f"{current_key}\t{current_sum}")