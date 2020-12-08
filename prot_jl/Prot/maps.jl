#=
Ce module permet de générer les cartes de contact pour une protéine donnée
=#

using BioStructures


function compute_contact_map(structure, pdb, cutoff)
    #=
    Détermine la carte de contacte pour une protéine donnée (ici pdb).
    =#
    contact_map = ContactMap(collectatoms(structure, calphaselector), cutoff)

    open("../data/contact_maps/$(pdb)_$(cutoff)A-julia", "w") do filout
        showcontactmap(filout, contact_map)
    end

    # Problèmes avec le package Plots - crash de Julia
end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    exit()  # Aucune action souhaitée
end
