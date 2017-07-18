from pip.commands import InstallCommand, UninstallCommand
import yaml
import sys

command_map = {"install": InstallCommand, "uninstall": UninstallCommand}

def add_dependency(pkg, dev=False):
	pass

def remove_dependency(pkg):
	pass

def install(args):
	c = InstallCommand()
	if c.main(args) == 0:
		add_dependency()

def uninstall(args):
	c = UninstallCommand()
	if c.main(args) == 0:
		remove_dependency()

def main():
	args = sys.argv[1:]
	command = args.pop(0)
	if command == "install":
		install(args)
	elif command == "uninstall":
		uninstall(args)
	else:
		raise Exception("Unknown command '{}'".format(command))

if __name__ == "__main__":
	main()
