# Le main du programme.
#
# Ce programme permet la manipulation de fichier PDB en julia:
#   - Lecture de fichier .pdb
#   - Visualisation de structures
#   - Comparaison de deux structures: alignement & rmsd
#   - Alignement de séquences
#   - Carte de contact (contact maps)
#
# Usage
# -----
#    Être situé dans le dossier ./Projet-julia/prot_jl
#
#    $ julia main.jl
#
#    - ID: l'id du fichier.s pdb à étudier
#    - ARG: l'étude à réaliser, view pour la visualisation, rmsd pour la comparaison de structures
#           (rmsd), align pour l'alignement de séquences et maps pour carte de contact
#    - ALIGN (optionnel): region pour un alignement des régions ou global pour un alignement global
#

include("Prot/prot.jl")
using .Prot

function main()
    # https://biojulia.net/BioStructures.jl/stable/documentation/
    args = Prot.arguments()

    length(args["id"][1]) > 2 && error("Veuillez renseigner 1 ou 2 fichier.s pdb")
    Prot.fetch_pdb(args["id"][1])

    if args["etude"] == "view"
        # https://nbviewer.jupyter.org/github/jgreener64/Bio3DView.jl/blob/master/examples/tutorial.ipynb
    end

    structure = Prot.load_pdb(args["id"][1])
    print(args)
end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    main()
end
