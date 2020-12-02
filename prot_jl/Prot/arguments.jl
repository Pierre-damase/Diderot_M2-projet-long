# Ce module permet de définir les arguments nécessaires et otpionnels

using ArgParse


function isin(x::Int)::Bool
    in(x, 6:12) && return true
    return false
end


function arguments()
    parser = ArgParseSettings()

    @add_arg_table! parser begin
        "-i", "--id"
            dest_name = "id"
            action => :append_arg
            nargs => '+'
            required = true
            help = "L'id du/des fichier.s pdb à analyser"
        "-e", "--etude"
            dest_name = "etude"
            required = true
            range_tester = (x->x=="view"||x=="rmsd"||x=="align"||x=="maps")
            help = "L'étude à réaliser: view (visualisation), rmsd (alignement structures + rmsd), align (alignement séquences), maps (carte de contact)"
        "-a", "--align"
            dest_name = "align"
            default = "global"
            range_tester = (x->x=="global"||x=="region")
            help = "Type d'alignement: region pour celui des régions ou global"
        "-c", "--cutoff"
            dest_name = "cutoff"
            default = 10
            arg_type = Int
            range_tester = isin
    end

    return parse_args(parser)
end


if abspath(PROGRAM_FILE) == @__FILE__
    exit()  # Aucune action souhaitée
end
