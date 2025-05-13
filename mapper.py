#!/usr/bin/env python3
# mapper.py
import sys

# L'entrée vient de nat2022_valid.csv, donc on s'attend à des lignes valides.
# Format d'entrée: sexe;preusuel;annais;dept;nombre

for line in sys.stdin:
    line = line.strip()
    parts = line.split(';')

    # Une vérification de base, bien que validation.py devrait avoir tout nettoyé
    if len(parts) == 5:
        sexe = parts[0]
        preusuel = parts[1] if parts[1] else "INCONNU" # Gérer prénom vide, si besoin
        annais = parts[2]
        # dept = parts[3] # Non utilisé dans la clé ou la valeur
        nombre_str = parts[4]

        try:
            nombre = int(nombre_str) # Doit être un entier
            # Clé: année_sexe_prénom
            key = f"{annais}_{sexe}_{preusuel}"
            # Sortie: clé <TAB> valeur
            print(f"{key}\t{nombre}")
        except ValueError:
            # Ce cas ne devrait pas arriver si validation.py a bien fonctionné
            # et a vérifié que 'nombre' est un entier.
            sys.stderr.write(f"Erreur: impossible de convertir '{nombre_str}' en entier pour la ligne: {line}\n")
            continue