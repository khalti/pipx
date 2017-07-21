import sys
import re

from pip.commands import InstallCommand, UninstallCommand
from pip.commands.show import search_packages_info
from yaml import load, dump

PROJECT_FILE="project.yaml"

def get_version(pkg):
	for i, dist in enumerate(search_packages_info([pkg])):
		version = dist.get("version")
		if version:
			return version

def update_project_file(data):
	f = open(PROJECT_FILE, "w")
	f.write(dump(data, default_flow_style=False))
	f.close()

def read_project_file():
	f = open(PROJECT_FILE, "r") 
	data = f.read()
	f.close()
	return load(data)

def register_dependency(pkg, dev=False):
	key = None
	deregister_dependency(pkg)
	data = read_project_file()
	if dev:
		key = "dev-dependencies"
	else:
		key = "dependencies"
	data[key][pkg] = get_version(pkg)
	update_project_file(data)

def deregister_dependency(pkg):
	data = read_project_file()
	keys = ["dependencies", "dev-dependencies"]
	for key in keys:
		try:
			data[key].pop(pkg)
		except KeyError:
			continue
	update_project_file(data)

def install(pkgs, update=False, register=True):
	dev = False
	if "-d" in pkgs or "--dev" in pkgs:
		dev = True
	c = InstallCommand()
	for pkg in pkgs:
		if pkg in ["-d", "--dev"]:
			continue
		args = [pkg]
		if update:
			args.append("--upgrade")

		if c.main(args) == 0 and register:
			register_dependency(pkg, dev=dev)

def uninstall(pkgs):
	c = UninstallCommand()
	for pkg in pkgs:
		if c.main([pkg]) == 0:
			deregister_dependency(pkg)

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


	to_dump["dependencies"] = {}
	to_dump["dev-dependencies"] = {}
	update_project_file(to_dump)

def setup(args, dev=False):
	keys = ["dependencies"]
	if "-d" in args or "--dev" in args:
		keys.append("dev-dependencies")

	data = read_project_file()
	for key in keys:
		for pkg in data[key]:
			install([pkg], register=False)


COMMAND_MAP = \
		{ "install": install
		, "uninstall": uninstall
		, "update": update
		, "init": init
		, "setup": setup
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
