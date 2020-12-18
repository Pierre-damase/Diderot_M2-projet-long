#=
Le main du programme.

Ce programme permet la manipulation de fichier PDB en julia:
  - Lecture de fichier .pdb
  - Visualisation de structures
  - Comparaison de deux structures: alignement & rmsd
  - Alignement de séquences
  - Carte de contact (contact maps)

Usage
-----
   Être situé dans le dossier ./Projet-julia/Code

   $ julia main.jl -i ID -e ARG -a ALIGN -c CUTOFF

   - ID: l'id du fichier.s pdb à étudier
   - ARG: l'étude à réaliser, view pour la visualisation, rmsd pour la comparaison de structures
          (rmsd), align pour l'alignement de séquences et maps pour carte de contact
   - ALIGN (optionnel): region pour un alignement des régions ou global pour un alignement global
   - CUTOFF (optionnel): le cutoff de la carte de contacts - entre 6 et 12A (vaut 10 par défaut)
=#

include("Prot/prot.jl")
using .Prot


function main()
    args = Prot.arguments()

    length(args["id"][1]) > 2 && error("Veuillez renseigner 1 ou 2 fichier.s pdb")
    Prot.fetch_pdb(args["id"][1])

    if args["etude"] == "view"
        id = args["id"][1][1]
        cmd = `sed -i "s/[0-9A-Z]\{4\}.pdb/$(id).pdb/" ./Prot/view.ipynb`
        run(cmd)
        run(`jupyter lab ./Prot/view.ipynb`)

    elseif args["etude"] == "maps"
        structure = Prot.load_pdb(args["id"][1])
        contact_map = Prot.compute_contact_map(structure[1], args["id"][1][1], args["cutoff"])

        Prot.save_contact_map(contact_map, args["id"][1][1], args["cutoff"])

    else
        # Vérifier que 2 protéines ont été renseignées
        if length(args["id"][1]) != 2
            error("Veuillez renseigner 2 protéines")
        end
        structure = Prot.load_pdb(args["id"][1])

        if args["etude"] == "align"
            align, scores = Prot.sequences_alignment(structure, args["align"], args["id"][1])
            Prot.save_sequences_alignment(align, scores, args["align"], args["id"][1])

        else
            rms, aligned_struct = Prot.structures_alignment(structure)
            Prot.save_structures_alignment(aligned_struct, args["id"][1])

            println("Le rmsd vaut $(rms)")
        end

    end

end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    main()
end
