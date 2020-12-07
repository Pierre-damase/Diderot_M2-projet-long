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
   Être situé dans le dossier ./Projet-julia/prot_jl

   $ julia main.jl

   - ID: l'id du fichier.s pdb à étudier
   - ARG: l'étude à réaliser, view pour la visualisation, rmsd pour la comparaison de structures
          (rmsd), align pour l'alignement de séquences et maps pour carte de contact
   - ALIGN (optionnel): region pour un alignement des régions ou global pour un alignement global
=#

include("Prot/prot.jl")
using .Prot


function main()
    # https://biojulia.net/BioStructures.jl/stable/documentation/
    # http://thegrantlab.org/bio3d/articles/online/intro_vignette/Bio3D_introduction.html
    args = Prot.arguments()

    length(args["id"][1]) > 2 && error("Veuillez renseigner 1 ou 2 fichier.s pdb")
    Prot.fetch_pdb(args["id"][1])

    if args["etude"] == "view"
        for id in args["id"][1]
            run(`./sed $id`)
            run(`jupyter lab ./Prot/view.ipynb`)
        end

    elseif args["etude"] == "maps"
        structure = Prot.load_pdb(args["id"][1])

    else
        # Vérifier que 2 protéines ont été renseignées
        if length(args["id"][1]) != 2
            error("Veuillez renseigner 2 protéines")
        end
        structure = Prot.load_pdb(args["id"][1])

        if args["etude"] == "align"
            align, scores = Prot.sequences_alignment(structure, args["align"], args["id"][1])
            Prot.save_sequences_alignment(align, scores, args["align"], args["id"][1])
        end

    end

end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    main()
end
