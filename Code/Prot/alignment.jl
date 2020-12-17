#=
Ce module permet de réaliser l'alignement des séquences & des structures (plus calcul rmsd).
=#

using BioStructures
using BioAlignments


function structures_alignment(structure)
    #=
    Alignement des structures & calcul du rmsd

    rms: le rmsd calculé entre les deux structures
    structure: les coordonnées modifiées du premier élément (structure[1]) calculées à partir de la
               "Transformation" qui map le premier élément aux deuxième
    =#
    superimpose!(structure[1], structure[2], standardselector)
    rms = rmsd(structure[1], structure[2], standardselector)

    return rms, structure[1]
end


function sequences_alignment(structure, type_align, pdb)
    #=
    Alignement deux à deux des séquences.

    Soit alignement global des deux protéine soit un alignement global des régions.

      - Utilisation de la matrice BLOSUM62 pour les scores de match.
      - Même open et extend gap pour les deux séquences, -10 & -1 respectivement
    =#
    println("Alignement $(type_align) des séquences de $(pdb[1]) et  $(pdb[2])")

    score_model = AffineGapScoreModel(BLOSUM62, gap_open=-10, gap_extend=-1)

    if type_align == "global"
        seq1, seq2 = "", ""

        for (chain1, chain2) in zip(chainids(structure[1]), chainids(structure[2]))
            seq1 *= String(LongAminoAcidSeq(structure[1][chain1], standardselector))
            seq2 *= String(LongAminoAcidSeq(structure[2][chain2], standardselector))
        end

        tmp = pairalign(GlobalAlignment(), seq1, seq2, score_model)
        alignments, scores = alignment(tmp), score(tmp)
    else
        alignments, scores = [], Int[]

        for (chain1, chain2) in zip(chainids(structure[1]), chainids(structure[2]))
            seq1 = String(LongAminoAcidSeq(structure[1][chain1], standardselector))
            seq2 = String(LongAminoAcidSeq(structure[2][chain2], standardselector))

            tmp = pairalign(GlobalAlignment(), seq1, seq2, score_model)
            push!(alignments, alignment(tmp))
            push!(scores, score(tmp))
        end
    end

    return alignments, scores
end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    exit()  # Aucune action souhaitée
end
