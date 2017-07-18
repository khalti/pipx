from pip.commands import InstallCommand, UninstallCommand
from yaml import load, dump
import sys

PROJECT_FILE = "project.yml"

def add_dependency(pkg, dev=False):
	pass

def remove_dependency(pkg):
	pass

def install(pkgs, update=False):
	c = InstallCommand()
	for pkg in pkgs:
		args = [pkg]
		if update:
			args.append("--upgrade")

		if c.main(args) == 0:
			add_dependency(pkg)

def uninstall(pkgs):
	c = UninstallCommand()
	for pkg in pkgs:
		if c.main(pkg) == 0:
			remove_dependency(pkg)

def main():
	args = sys.argv[1:]
	command = args.pop(0)
	if command == "install":
		install(args)
	elif command == "uninstall":
		uninstall(args)
	elif command == "update":
		install(args, update=True)
	else:
		raise Exception("Unknown command '{}'".format(command))

if __name__ == "__main__":
	main()
