#=
Ce proramme permet de benchmark les différentes méthodes mise en place dans le module Prot. 
=#

include("Prot/prot.jl")
using .Prot

using BioStructures
using NaturalSort


function write_dico(dico, path)
    open(path, "w") do filout
    
        for (key, value) in dico
            write(filout, "$key: $value\n")
        end
        
    end
end


function main()
    samples, max_time = 100, 10

    # Path data
    path_data = "./data/pdb/Benchmark/"

    # Liste des strucutres triée dans l'ordre naturel
    pdb = readdir(path_data)
    pdb = [split(ele, ".")[1] for ele in pdb]
    pdb = sort(pdb, lt=natural)

    dico = Dict(
        "Residues" => [], "Load" => [],
        "Alignement seq" => Dict("region" => [], "global" => []),
        "Alignement 3d" => [], "Contact maps" => []
    )

    # START BENCHMARK #

    ##########################################
    # Benchmark: chargement des structures   #
    ##########################################
    print("Benchmark - chargement des structures\t")

    structures = []
    for struc in pdb
        push!(structures, Prot.load_pdb([struc, struc], "./data/pdb/Benchmark/", false))
    
        execution = []
        for _ in 1:samples
            time = @elapsed Prot.load_pdb([struc, struc], "./data/pdb/Benchmark/", false)
            append!(execution, time)
            if time > max_time
                break
            end
        end
    
        push!(dico["Load"], execution)
    end

    for struc in structures
        append!(dico["Residues"], countresidues(struc[1], standardselector))
    end

    println("Over")

    ##########################################
    # Benchmark: alignement des séquences    #
    ##########################################
    print("Benchmark - alignement des séquences\t")

    for align_param in ["region", "global"]
        for struc in structures
            name = split(structurename(struc[1]), ".")[1]
        
            execution = []
            for _ in 1:samples
                time = @elapsed Prot.sequences_alignment(struc, align_param, [name, name],
                                                         false)
                append!(execution, time)
                if time > max_time
                    break
                end
            end
             
            push!(dico["Alignement seq"][align_param], execution)
        end
    end

    println("Over")

    ##########################################
    # Benchmark: alignement des structures   #
    ##########################################
    print("Benchmark - alignement des structures\t")

    for struc in structures
        
        execution = []
        for _ in 1:samples
            time = @elapsed Prot.structures_alignment(struc, false)
            append!(execution, time)
            if time > max_time
                break
            end
        end
        
        push!(dico["Alignement 3d"], execution)
    end

    println("Over")

    ##########################################
    # Benchmark: carte de contacts           #
    ##########################################
    print("Benchmark - carte de contacts\t")

    for struc in structures
        name = split(structurename(struc[1]), ".")[1]
        cutoff = 6

        execution = []
        for _ in 1:samples
            time = @elapsed Prot.compute_contact_map(struc[1], name, cutoff)
            append!(execution, time)
            if time > max_time
                break
            end
        end
        
        push!(dico["Contact maps"], execution)
    end

    println("Over")

    # Export data to text file
    write_dico(dico, "./data/benchmark-julia.txt")
end


if abspath(PROGRAM_FILE) == @__FILE__  # Equivalent to if __name__ == "__main__"
    main()
end
