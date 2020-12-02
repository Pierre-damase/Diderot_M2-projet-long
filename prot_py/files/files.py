"""
Ce module permet de manipuler les fichiers pdb:

  - Fetch (télécharger) le fichier pdb renseigner en argument (si non présent) à partir de RCSB PDB
  - Charger la structure des fichiers pdb renseignés
"""

import Bio.PDB as PDB
import os


def fetch_pdb(pdb):
    """
    Télécharge les fichiers pdb dans le dossier ./data/pdb/

    Parameter
    ---------
    pdb: list
        le.s id passé.s en paramètre
    """
    for id in pdb:
        if not os.path.exists("./data/pdb/{}.pdb".format(id)):
            os.system("wget https://files.rcsb.org/view/{id}.pdb -O ./data/pdb/{id}.pdb".
                      format(id=id))
            print("Strucutre {} téléchargée\n".format(id))


def load_pdb(pdb):
    """
    Charge à l'aide du module Bio.PDB les structures à analyser.

    Parameter
    ---------
    pdb: list
        le.s id passé.s en paramètre

    Return
    ------
    struct: tuple
        tuple d'objets de type structure
    """
    parser = PDB.PDBParser()

    struct = tuple()
    for id in pdb:
        struct += (parser.get_structure(f"{id}", "./data/pdb/{}.pdb".format(id)),)
        print("\nStructure {} chargée\n".format(id))

    return struct


def align_format(text, width=80):
    """
    Permet de limiter l'affichage à 80 caractères par ligne (défaut)

    Parameter
    ---------
    text: str
        le texte à formater
    width: int (par défaut vaut 80)
        le nombre de caractère maximum à écrire par ligne
    """
    seq = [text[i:i+width] for i in range(0, len(text), width)]
    return "\n".join(seq)


def align_block(align, filout):
    """
    Ecrit un block alignement dans le fichier texte.

    Ce block est constitué de la seqA, seqB, de l'indentité entre ces deux séquences, du score de
    l'alignement.
    """
    identity = ""
    for amino1, amino2 in zip(align.seqA, align.seqB):
        if amino1 == amino2:
            identity += "|"
        else:
            identity += " "

    filout.write("\nAlignement - score: {} - Start: {} - End: {}\n".
                 format(align.score, align.start, align.end))
    filout.write("{}\n".format(align_format(align.seqA)))
    filout.write("{}\n".format(align_format(identity)))
    filout.write("{}\n".format(align_format(align.seqB)))


def save_sequences_alignment(alignments, pdb, type_align):
    """
    Ecrit l'alignement obtenu dans un fichier texte - dossier ./data/alignments/

    Parameter
    ---------
    alignments: Bio.pairwise2.Alignment
        alignement de séquences
    pdb: list
        l'id des deux protéines étudiées
    type_align: str
        alignement global ou par régions
    """
    fichier = "./data/alignments/{}_alignment-{}_{}.txt".format(type_align, pdb[0], pdb[1])

    with open(fichier, "w") as filout:
        filout.write("Alignement {} de {} & {}\n\n".format(type_align, pdb[0], pdb[1]))

        if type_align == "global":
            for align in alignments:
                align_block(align, filout)
        else:
            for align in alignments:
                align_block(align, filout)


def save_structures_alignment(aligned_struct, pdb):
    """
    Sauvegarde la version alignée de la protéine.
    """
    io = PDB.PDBIO()
    io.set_structure(aligned_struct)
    io.save("./data/pdb/{}_aligned_to_{}.pdb".format(pdb[0], pdb[1]))


if __name__ == "__main__":
    pass  # Aucune action souhaitée
