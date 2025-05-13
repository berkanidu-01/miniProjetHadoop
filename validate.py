#!/usr/bin/env python3
# validation.py
import csv
import sys

INPUT_CSV_FILE = 'nat2022.csv'

def validate_row(row_number, row_data):
    if len(row_data) != 5:
        return False

    sexe = row_data[0]
    annais = row_data[2]
    dept = row_data[3]
    nombre_str = row_data[4]

    if not (sexe and annais and dept and nombre_str):
        return False

    try:
        int(nombre_str)
        int(annais)
    except ValueError:
        return False

    return True

def main():
    valid_lines_count = 0
    invalid_lines_count = 0

    with open(INPUT_CSV_FILE, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter=';')

        try:
            header = next(reader)
            print(f"En-tête ignoré: {';'.join(header)}", file=sys.stderr)
        except StopIteration:
            print("Fichier d'entrée vide.", file=sys.stderr)
            return

        for i, row in enumerate(reader, start=2):
            if validate_row(i, row):
                # Écrire vers stdout pour que le pipeline continue
                print(';'.join(row))
                valid_lines_count += 1
            else:
                invalid_lines_count += 1

    print(f"\nValidation terminée.", file=sys.stderr)
    print(f"Lignes valides transmises au pipeline: {valid_lines_count}", file=sys.stderr)
    print(f"Lignes ignorées: {invalid_lines_count}", file=sys.stderr)

if __name__ == "__main__":
    main()
