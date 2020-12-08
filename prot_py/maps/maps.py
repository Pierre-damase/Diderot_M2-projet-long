"""
Ce module permet de générer les cartes de contact pour une protéine donnée.
"""

import matplotlib.pyplot as plt
import numpy as np
import sys


def compute_distance_matrice(atoms):
    """
    Détermine la matrice de distance euclidienne en trois dimensions entre tous les atomes.

    Il n'est pris en compte que les carbones alpha.

    Soit d la distance euclidienne entre deux points A et B tel que:

      d = sqrt((x_b - x_a)^2 + (y_b - y_a)^2 + (z_b - z_a)^2)
    """
    dist_mat = np.zeros((len(atoms), len(atoms)))

    for i, atom1 in enumerate(atoms):
        for j, atom2 in enumerate(atoms):
            dist_mat[i][j] = \
                np.sqrt(
                    np.power((atom2.coord[0] - atom1.coord[0]), 2) +
                    np.power((atom2.coord[1] - atom1.coord[1]), 2) +
                    np.power((atom2.coord[2] - atom1.coord[2]), 2)
                )
    return dist_mat


def compute_contact_map(struct, pdb, cutoff):
    """
    Détermine la carte de contacte pour une protéine donnée (ici pdb).
    """
    amino_acid = [
        'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE',
        'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL'
    ]
    atoms = []

    # Sélection de l'ensemble des CA
    for chaine in struct[0]:  # [0] pour travailler sur le 1er modèle
        for res in chaine:
            if res.get_resname() in amino_acid:
                atoms.append(res['CA'])

    dist_mat = compute_distance_matrice(atoms)

    contact_map = dist_mat < cutoff  # transformation de la matrice de distance en carte de contact

    plot_contact_map(contact_map, pdb, cutoff)


def plot_contact_map(contact_map, pdb, cutoff):
    """
    Génère le graphe d'une carte de contacts donnée.
    """
    fig, axs = plt.subplots(1, 1, figsize=(12, 10), constrained_layout=True)
    axs.imshow(contact_map, aspect="auto", cmap=plt.cm.gray, interpolation='nearest')

    title = "Carte de contacts de la protéine {} pour un cutoff de {}A".format(pdb, cutoff)
    fig.suptitle(title, fontsize="xx-large")

    name = "./data/contact_maps/{}_{}A-python.png".format(pdb, cutoff)
    plt.savefig(name)
    plt.clf()


if __name__ == "__main__":
    sys.exit()  # Aucune action souhaitée
