from pip.commands import InstallCommand, UninstallCommand
from yaml import load, dump
import sys

def update_project_file(data):
	f = open("project.yaml", "w")
	f.write(dump(data, default_flow_style=False))
	f.close()

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

def update(pkgs):
	install(pkgs, update=True)

def init(pkgs):
	to_ask = \
			{ "name": {"label": "Name", "default": None}
			, "description": {"label": "Description", "default": None}
			, "version": {"label": "Version", "default": "0.0.0"}
			}
	to_dump = {}
	for key, value in to_ask.items():
		default = value["default"]
		if default:
			to_dump[key] = input("{} ({}): ".format(value["label"], default)) or default
		else:
			to_dump[key] = input("{}: ".format(value["label"]))


	update_project_file(to_dump)
	

COMMAND_MAP = \
		{ "install": install
		, "uninstall": uninstall
		, "update": update
		, "init": init
		}

def main():
	args = sys.argv[1:]
	command = args.pop(0)
	try:
		COMMAND_MAP[command](args)
	except KeyError:
		raise Exception("Unknown command '{}'".format(command))

if __name__ == "__main__":
	main()
