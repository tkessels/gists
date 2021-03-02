PS1='\[\033[44;37m\]'$(printf '_%.0s' $(seq 1 $(tput cols)))'\[\033[1;0m\]\r\n\t \w :\n\$ '
alias mv="mv -vi"
alias cp="cp -vi"
alias '+'='pushd .'
alias -- '-'='popd'
[[ -f ~/.shell_aliases ]] && . ~/.shell_aliases
[[ -f ~/.config/z.sh ]] && . ~/.config/z.sh
