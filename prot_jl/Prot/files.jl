# Ce module permet de manipuler des fichiers pdb.
#
#  - Fetch (télécharger) le fichier pdb renseigner en argument (si non présent) à partir de RCSB PDB
#  - Charger la structure des fichiers pdb renseignés

using BioStructures


function fetch_pdb(pdb)
    for id in pdb
        if !isfile("../data/pdb/$(id).pdb")
            run(`wget https://files.rcsb.org/view/$(id).pdb -O ../data/pdb/$(id).pdb`)
            print("Structure $(id) téléchargée\n")
        end
    end
end


function load_pdb(pdb)
    structure = []
    for id in pdb
        append!(structure, read("../data/pdb/$(id).pdb", PDB))
        print("\nStructure $(id) chargée\n")
    end
    return structure
end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    exit()  # Aucune action souhaitée
end
