#!/usr/bin/env python3
# plot_names_trends.py
"""
Script pour visualiser l'évolution des prénoms les plus populaires selon les années.
Usage:
    python plot_names_trends.py --csv top_names_by_year_and_gender.csv --top 5 [--sex Masculin|Féminin]
"""
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(
        description="Visualise les prénoms les plus populaires par année en utilisant matplotlib."
    )
    parser.add_argument(
        '--csv', required=True,
        help='Chemin vers le fichier CSV généré (Année,Sexe,Rang,Prénom,Total)'
    )
    parser.add_argument(
        '--top', type=int, default=5,
        help='Nombre de prénoms à afficher (par défaut: 5)'
    )
    parser.add_argument(
        '--sex', choices=['Masculin', 'Féminin'], default=None,
        help="Filtrer par sexe (optionnel)"
    )
    args = parser.parse_args()

    # Chargement des données
    df = pd.read_csv(args.csv, encoding='utf-8')
    if args.sex:
        df = df[df['Sexe'] == args.sex]

    # Somme des totals par année et prénom
    df_sum = (
        df.groupby(['Année', 'Prénom'])['Total']
          .sum()
          .reset_index()
    )

    # Sélection des top N prénoms globalement
    top_names = (
        df_sum.groupby('Prénom')['Total']
              .sum()
              .nlargest(args.top)
              .index
              .tolist()
    )
    df_top = df_sum[df_sum['Prénom'].isin(top_names)]

    # Préparation pour tracé : pivot
    pivot = df_top.pivot(index='Année', columns='Prénom', values='Total')
    pivot = pivot.fillna(0)
    pivot.index = pivot.index.astype(int)
    pivot = pivot.sort_index()

    # Tracé
    plt.figure()
    for name in pivot.columns:
        plt.plot(pivot.index, pivot[name], marker='o', label=name)
    plt.xlabel('Année')
    plt.ylabel('Nombre de naissances')
    title = f'Évolution des {args.top} prénoms les plus populaires'
    if args.sex:
        title += f' ({args.sex})'
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
