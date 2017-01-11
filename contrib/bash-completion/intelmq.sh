# Thanks to Steve https://debian-administration.org/article/317/An_introduction_to_bash_completion_part_2

_intelmqctl ()
{
    local cur prev opts base;
    COMPREPLY=();
    cur="${COMP_WORDS[COMP_CWORD]}";
    prev="${COMP_WORDS[COMP_CWORD-1]}";

    generic_pre="-h --help -v --version"
    generic_post="-q --quiet -t --type"

    if [[ "$prev" == -t ]] || [[ "$prev" == --type ]]; then
        COMPREPLY=( $( compgen -W "json text"  -- "$cur" ) )
        return 0
    fi

    case $COMP_CWORD in
        1)
            opts="start stop restart reload run status clear list check";
            COMPREPLY=($(compgen -W "${opts} ${generic_pre}" -- ${cur}));
            return 0
        ;;
        2)
            pipeline='/opt/intelmq/etc/pipeline.conf';
            case "${COMP_WORDS[1]}" in
                start | stop | restart | status | reload | log | run)
                    runtime='/opt/intelmq/etc/runtime.conf';
                    local bots=$(jq 'keys[]' $runtime);
                    COMPREPLY=($(compgen -W "${bots}" -- ${cur}));
                    return 0
                ;;
                clear)
                    local bots=$(jq '.[] | .["source-queue"]' $pipeline | grep -v '^null$'; jq '.[] | .["destination-queues"]'  $pipeline | grep -v '^null$' | jq '.[]');
                    COMPREPLY=($(compgen -W "${bots}" -- ${cur}));
                    return 0
                ;;
                list)
                    COMPREPLY=($(compgen -W "bots queues" -- ${cur}));
                    return 0
                ;;
                *)
                    COMPREPLY=($(compgen -W "${generic_post}" -- ${cur}));
                    return 0
                ;;
            esac
        ;;
        3)
            COMPREPLY=($(compgen -W "${generic_post}" -- ${cur}));
            return 0
        ;;
        4)
            if [[ "${COMP_WORDS[1]}" == "log" ]]; then
                COMPREPLY=( $( compgen -W "DEBUG INFO WARNING ERROR CRITICAL"  -- "$cur" ) )
                return 0
            fi
        ;;
    esac
}
complete -F _intelmqctl intelmqctl

_intelmqdump ()
{
    local cur prev opts base;
    COMPREPLY=();
    cur="${COMP_WORDS[COMP_CWORD]}";
    logpath=/opt/intelmq/var/log;
    # TODO: handle no dumps
    local dumps=$(for filename in $logpath/*.dump; do b=${filename##*/}; echo ${b%%.*}; done);
    COMPREPLY=($(compgen -W "${dumps} -h --help" -- ${cur}))
}
complete -F _intelmqdump intelmqdump
