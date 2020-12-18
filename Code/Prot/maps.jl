#=
Ce module permet de générer les cartes de contact pour une protéine donnée
=#

using BioStructures


function compute_contact_map(structure, pdb, cutoff)
    #=
    Détermine la carte de contacte pour une protéine donnée (ici pdb).
    =#
    contact_map = ContactMap(collectatoms(structure, calphaselector), cutoff)

    return contact_map
end


function save_contact_map(contact_map, pdb, cutoff)
    open("./data/contact_maps/$(pdb)_$(cutoff)A-julia", "w") do filout
        showcontactmap(filout, contact_map)
    end
end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    exit()  # Aucune action souhaitée
end
