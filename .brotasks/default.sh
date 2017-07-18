#!/bin/sh

project=$(basename `pwd`)

init () {
	bro setup_tmux
	echo "Happy hacking !!!"
}

env () {
	source .env/bin/activate
}

setup_tmux () {
	structure $project
	window editor
		run "bro env"
		run "nvim"
	window terminal
		run "bro env"

	focus editor
	connect $project
}

test () {
	py.test tests/*
}

$@
