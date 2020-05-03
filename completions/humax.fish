
function __fish_humax_no_command_yet
    set -l cmdln (commandline -poc)
    for i in (commandline -poc)
        if contains -- $i post list-methods config-path ip get-port-forwarding
            return 1
        end
    end
    return 0
end


# do not offer file completion
complete -c humax -f

# general switches
complete -c humax -s h -l help --description "Display help and exit" -f
complete -c humax -s r -l router --description "Specify the section in config file to use. Defaults to DEFAULT" -x
complete -c humax -s V -l version --description "Display program version" -f

# main subcommand list
complete -c humax -n '__fish_use_subcommand' -xa post --description "Make a post request to /api"
complete -c humax -n '__fish_use_subcommand' -fa list-methods --description "List available post methods."
complete -c humax -n '__fish_use_subcommand' -fa config-path --description "Print config file path."
complete -c humax -n '__fish_use_subcommand' -fa ip --description "Display WAN IP."
complete -c humax -n '__fish_use_subcommand' -fa get-port-forwarding --description "Display port forwarding rules."

complete -c humax -n 'contains post (commandline -poc)' -a "(command humax list-methods)"
