"""
Ce module définis les arguments nécessaires et optionnels.

   - ID: l'id du fichier.s pdb à étudier
   - ARG: l'étude à réaliser, view pour la visualisation, rmsd pour la comparaison de structures
          (rmsd), align pour l'alignement de séquences et carte pour carte de contact
   - ALIGN (optionnel): region pour un alignement des régions ou global pour un alignement global
   - CUTOFF (optionnel): le cutoff de la carte de contacts - entre 6 et 12A (vaut 10 par défaut)
"""

import argparse
import sys


def required_length(nmin, nmax):
    """
    Permet de limiter le nombre de fichier pdb renseigné, ici entre 1 et 2.
    """
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin <= len(values) <= nmax:
                msg = "Veuillez renseigner entre {} and {} arguments".format(nmin, nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength


def arguments():
    """
    Définis les arguments nécessaires.
    """
    parser = argparse.ArgumentParser()

    # Arguments requis
    required = parser.add_argument_group('required', "les arguments requis")

    required.add_argument('-i', '--id', dest="id", nargs="+", action=required_length(1, 2),
                          required=True, help="L'id du/des fichier.s pdb à analyser")

    required.add_argument('-e', '--etude', dest="etude", required=True,
                          choices=['view', 'rmsd', 'align', 'maps'],
                          help="""L'étude à réaliser: view pour la visualisation avec nglview,
                           rmsd pour la comparaison de deux structures (alignement & rsmd), align
                           pour l'alignement de deux séquences, et maps pour carte de contact""")

    # Arguments optionnels
    optional = parser.add_argument_group('optional', "les arguments optionnels")

    optional.add_argument('-a', '--align', dest="align", default="global",
                          choices=['region', 'global'],
                          help="""Type d'alignement à réaliser: region pour alignement des régions
                           et global (défaut) pour l'alignement global""")

    optional.add_argument('-c', '--cutoff', dest="cutoff", default=10, choices=range(6, 13),
                          help="""Le cutoff pour la carte de contact - entre 6 et 12 A, vaut par
                           défaut 10)""")

    return parser.parse_args()


if __name__ == "__main__":
    sys.exit()  # Aucune action souhaitée
