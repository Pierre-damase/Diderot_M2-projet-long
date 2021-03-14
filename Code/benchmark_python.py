"""
Ce proramme permet de benchmark les différentes méthodes mise en place dans le module prot_py.
"""

import os
import re
import sys
import time

import pandas as pd

from prot_py.alignment import alignment as ali
from prot_py.files import files as f
from prot_py.maps import maps


def block_print():
    """
    Bloquer l'affichage des print dans le terminal.
    """
    sys.stdout = open(os.devnull, 'w')


def enable_print():
    """
    Autoriser l'affichage des print dans le terminal.
    """
    sys.stdout = sys.__stdout__


def execution_time(fonction, *args, samples=100, max_time=10):
    """
    Détermine le temps d'éxécution d'une fonction f donné pour x samples (par défaut 100).

    Il est préféré la méthode process_time() que time(), deux méthodes du module time.

      - time(): détermine le temps écoulé en seconde depuis le 1/01/1979, si le temps
        d'éxécution est trop cours il vaudra 0.0
      - process_time(): détermine le CPU time en seconde, plus précis que la méthode time()

    Parameter
    ---------
    fonction:
        la méthode à évaluer
    params:
        les paramètres de la méthode
    samples:
        le nombre de fois que la méthode est exécutée
    max_time:
        arrêt du benchmark si le temps d'éxécution dépasse une valueur, indépendamment du
        nombre de samples - par défault 10s
    """
    block_print()

    execution = []
    for _ in range(samples):
        start_time = time.process_time()  # mesure le CPU time
        fonction(*args)
        end_time = time.process_time() - start_time
        execution.append(end_time)

        if end_time > max_time:
            return execution

    enable_print()
    return execution


def main():
    # Path data
    path_data = "./data/pdb/Benchmark/"

    # Liste des structures triée dans l'ordre naturel
    pdb = os.listdir(path_data)
    pdb = [ele.split('.')[0] for ele in pdb]
    pdb.sort(
        key=lambda fichier: [int(ele) if ele.isdigit() else ele.lower() for ele in
                             re.split('(\d+)', fichier)]
    )

    dico = {'Residues': [], 'Load': [], 'Alignement seq': {'region': [], 'global': []},
            'Alignement 3d': [], 'Contact maps': []}

    # START BENCHMARK #

    ##########################################
    # Benchmark: chargement des structures   #
    ##########################################
    print("Benchmark - chargement des structures", end="\t")

    structures = []
    for struct in pdb:
        block_print()
        structures.append(f.load_pdb([struct, struct], path=path_data))

        dico['Load'].append(
            execution_time(f.load_pdb, [struct], path_data)
        )

    # Calcul du nombre de résidues par structure
    for struct in structures:
        count = 0
        for chain in struct[0][0]:
            for res in chain:
                count += 1
        dico['Residues'].append(count)

    print("Over")

    ##########################################
    # Benchmark: alignement des séquences    #
    ##########################################
    print("Benchmark - alignements des séquences", end="\t")

    for align_param in dico['Alignement seq'].keys():
        for struct in structures:
            dico['Alignement seq'][align_param].append(
                execution_time(ali.sequences_alignment, struct, align_param)
            )

    print("Over")

    ##########################################
    # Benchmark: alignement des structures   #
    ##########################################
    print("Benchmark - alignements des structures", end="\t")

    for struct in structures:
        dico['Alignement 3d'].append(
            execution_time(ali.structures_alignment, struct)
        )

    print("Over")

    ##########################################
    # Benchmark: carte de contacts           #
    ##########################################
    print("Benchmark - carte de contacts", end="\t")

    cutoff = 6
    for struct in structures:
        dico['Contact maps'].append(
            execution_time(maps.compute_contact_map, struct[0],  struct[0].id, cutoff)
        )

    print("Over")

    # END BENCHMARK #

    # Save data to pandas DataFrame
    data = pd.DataFrame(columns=dico.keys())
    data = data.append(dico, ignore_index=True)

    # Export data to json
    data.to_json('./data/benchmark-python.json')


if __name__ == "__main__":
    main()
