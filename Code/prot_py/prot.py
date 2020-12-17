"""
Ce programme permet la manipulation de fichier PDB en python:

  - Lecture de fichier .pdb
  - Visualisation de structures
  - Comparaison de deux structures: alignement & rmsd
  - Alignement de séquences
  - Carte de contact (contact maps)


Usage
-----
    Être situé dans le dosier ./Projet-julia

    $ python -m prot -i ID -e ARG -a ALIGN

   - ID: l'id du fichier.s pdb à étudier
   - ARG: l'étude à réaliser, view pour la visualisation, rmsd pour la comparaison de structures
          (rmsd), align pour l'alignement de séquences et maps pour carte de contact
   - ALIGN (optionnel): region pour un alignement des régions ou global pour un alignement global
"""

import os


from prot_py.alignment import alignment as ali
from prot_py.arguments import arguments as arg
from prot_py.files import files as f
from prot_py.maps import maps


def main():
    args = arg.arguments()

    f.fetch_pdb(args.id)

    if args.etude == "view":
        for prot in args.id:
            os.system("nglview ./data/pdb/{}.pdb".format(prot))  # Visualisation avec nglview
            os.system("rm tmpnb_ngl.ipynb")  # Suppression du notebook créé

    elif args.etude == "maps":
        struct = f.load_pdb(args.id)
        contact_map = maps.compute_contact_map(struct[0], args.id[0], args.cutoff)
        maps.plot_contact_map(contact_map, args.id[0], args.cutoff)

    else:
        # Vérifier que 2 protéines ont été renseignées
        if not len(args.id) == 2:
            msg = "Veuillez renseigner 2 protéines"
            raise ValueError(msg)

        struct = f.load_pdb(args.id)  # Chargé les structures

        if args.etude == "align":
            align = ali.sequences_alignment(struct, args.align)
            f.save_sequences_alignment(align, args.id, args.align)

        elif args.etude == "rmsd":
            rmsd, aligned_struct = ali.structures_alignment(struct)
            f.save_structures_alignment(aligned_struct, args.id)

            print("Le rmsd vaut {:.3f} Angstom".format(rmsd))


if __name__ == "__main__":
    main()
