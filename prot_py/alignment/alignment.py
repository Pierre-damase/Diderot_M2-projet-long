"""
Ce module permet de réaliser l'alignement des séquences & des structures (plus calcul rmsd).
"""

import Bio.Align.substitution_matrices as mat
import Bio.PDB as PDB
import Bio.pairwise2 as pairwise
import Bio.Seq as Seq
import sys


def structures_alignment(struct):
    """
    Alignement des structures & calcul du rmsd.

    Return
    ------
    rmsd: float
    struct: la version aligné de la 2ème protéines avec la première
    """
    amino_acid = [
        'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE',
        'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL'
    ]
    fixed, moving = [], []

    print("Alignement des structures de {} & {}".format(struct[0].id, struct[1].id))

    for chaine1, chaine2 in zip(struct[0][0], struct[1][0]):  # [0] pour travailler sur le 1er mdl
        for res1, res2 in zip(chaine1, chaine2):

            if res1.get_resname() in amino_acid and res2.get_resname() in amino_acid:

                # Si même résidus à une position donnée, on prend en compte tous les backbone atoms
                if res1.get_resname() == res2.get_resname():
                    for atom1, atom2 in zip(res1.get_unpacked_list(), res2.get_unpacked_list()):
                        fixed.append(atom1)
                        moving.append(atom2)
                # Sinon on ne prend en compte que les CA
                else:
                    fixed.append(res1['CA'])
                    moving.append(res2['CA'])

    super_imposer = PDB.Superimposer()  # Attention, listes de même taille
    super_imposer.set_atoms(fixed, moving)  # détermine les matrices de rotation/translation
    super_imposer.apply(struct[1].get_atoms())  # applique les matrices à la molécule

    return super_imposer.rms, struct[1]


def sequences_alignment(struct, type_align):
    """
    Permet de réaliser un alignement deux à deux (pairwise) des séquences.

    Soit alignement global des deux protéine soit un alignement global des régions.

    Utilisation de globalds:
      - global: alignement global
      - d: utilisation de la matrice BLOSUM62 pour les scores de match
      - s: même open et extend gap pour les deux séquences, -10 & -1 respectivement
    """
    peptides = PDB.PPBuilder()
    matrix = mat.load("BLOSUM62")

    print("Alignement {} des séquences de {} & {}".format(type_align, struct[0].id, struct[1].id))

    if type_align == "global":
        seq1, seq2 = Seq.Seq(''), Seq.Seq('')

        for peptide1, peptide2 in zip(peptides.build_peptides(struct[0]),
                                      peptides.build_peptides(struct[1])):
            seq1 += peptide1.get_sequence()
            seq2 += peptide2.get_sequence()

        alignments = pairwise.align.globalds(seq1, seq2, matrix, -10, -1)[0]
    else:
        alignments = []

        for peptide1, peptide2 in zip(peptides.build_peptides(struct[0]),
                                      peptides.build_peptides(struct[1])):
            seq1, seq2 = peptide1.get_sequence(), peptide2.get_sequence()

            tmp = pairwise.align.globalds(seq1, seq2, matrix, -10, -1)
            alignments.append(tmp[0])

    return alignments


if __name__ == "__main__":
    sys.exit()  # Aucune action souhaitée
