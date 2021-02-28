#=
Ce module permet de manipuler des fichiers pdb.

  - Fetch (télécharger) le fichier pdb renseigner en argument (si non présent) à partir de RCSB PDB
  - Charger la structure des fichiers pdb renseignés
=#

using BioStructures


function fetch_pdb(pdb)
    for id in pdb
        if !isfile("./data/pdb/$(id).pdb")
            run(`wget https://files.rcsb.org/view/$(id).pdb -O ./data/pdb/$(id).pdb`)
            print("Structure $(id) téléchargée\n")
        end
    end
end


function load_pdb(pdb, verbose=true)
    structure = []

    for id in pdb
        append!(structure, read("./data/pdb/$(id).pdb", PDB))
        if verbose
            print("\nStructure $(id) chargée\n")
        end
    end
    return structure
end


function align_format(text, width=80)
    #=
    Permet de limiter l'affichage à 80 caractères par ligne (défaut)
    =#
    seq = Array{String, 1}()

    for i in 1:width:length(text)
        if i+width > length(text)
            push!(seq, text[i:end])
        else
            push!(seq, text[i:i+width-1])
        end
    end

    return join(seq, "\n")
end


function align_block(align, scores, filout)
    #=
    Ecrit un block alignement dans le fichier texte.

    Ce block est constitué de la séquence seq, celle de référence ref et du score d'alignement.
    =#
    seq, ref, identity = "", "", ""
    for amino_acid in collect(align)
        seq *= amino_acid[1]
        ref *= amino_acid[2]
        amino_acid[1] == amino_acid[2] ? identity *= "|" : identity *= " "
    end

    write(filout, "\nAlignement - score: $(scores)\n")
    write(filout, "$(align_format(seq))\n")
    write(filout, "$(align_format(identity))\n")
    write(filout, "$(align_format(ref))\n")
end


function save_sequences_alignment(alignments, scores, type_align, pdb)
    fichier = "./data/alignments/$(type_align)_alignment-$(pdb[1])_$(pdb[2])-julia.txt"

    open(fichier, "w") do filout
        write(filout, "Alignement $type_align de $(pdb[1]) & $(pdb[2])\n\n")

        if type_align == "global"
            align_block(alignments, scores, filout)
        else
            for i in 1:length(alignments)
                align_block(alignments[i], scores[i], filout)
            end
        end
    end

end


function save_structures_alignment(aligned_struct, pdb)
    file = "./data/pdb/$(pdb[1])_aligned_to_$(pdb[2])-julia.pdb"
    writepdb(file, aligned_struct)
end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    exit()  # Aucune action souhaitée
end
