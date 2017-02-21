alias ls='ls --color'
alias grep='grep --color'
alias ...='cd ../..'
alias ....='cd ../../..'
alias agu='apt-get update'
alias agi='apt-get install'
alias agg='apt-get upgrade'
alias agd='apt-get dist-upgrade'
alias acs='apt-cache search'

alias bb='bitbake -f -c compile'
alias bbc='bitbake axis-image-cvp'
alias bbr='bitbake -g axis-image-cvp && cat pn-depends.dot | grep -v -e "-native" | grep -v digraph | grep -v -e "-image" | awk '\''{print $1}'\'' | sort | uniq'
alias blr='bitbake-layers show-recipes | grep'
alias ds='devtool search'

function de() {
    devtool extract $1 sources/$1
}

function dm() {
    devtool modify -x $1 sources/$1
}

function dmake() {
	endpath=$(basename $(pwd))
	devtool build $(basename $(pwd))
}

function dur() {
    devtool update-recipe $1 -a ../../$2
}

function db() {
    devtool build $1
}

function dd() {
    devtool deploy-target --no-check-space $1 root@192.168.77.$2 -c
}

#export VIRTUAL_ENV_DISABLE_PROMPT=y
#source /home/chenhuiz/virtual_envs/prod-python-2.7.3/bin/activate
#alias pip='http_proxy=http://wwwproxy:3128 https_proxy=http://wwwproxy:3128 pip'

source ~/.git-completion.bash

source ~/work/tools/oe-setup/oe-setup.sh 2> /dev/null

export HISTSIZE=4000
export HISTIGNORE="&"
export PATH=$PATH:/sbin:/usr/sbin

#export AXIS_DIST_HOST=shcndev-dist.sh.cn.axis.com
export AXIS_DIST_HOST=dev-dist.se.axis.com
export CVS_RSH=ssh

export https_proxy="http://wwwproxy.se.axis.com:3128"
export http_proxy="http://proxycluster.se.axis.com:3128"

#export PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig

PS1='${debian_chroot:+($debian_chroot)}\[\e[0;39m\]\u@\h\[\e[m\]:\[\e[0;36m\]\w\[\e[m\]\$ '
