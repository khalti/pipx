import sys
import re
import json

from setuptools import find_packages
from pip.commands import InstallCommand, UninstallCommand
import pip
from pkg_resources import get_distribution

PROJECT_FILE="project.json"
DEFAULT_STRUCT = {"dependencies": [], "dev-dependencies": []}

def get_version(pkg):
	return get_distribution(pkg).version

def update_project_file(data):
	f = open(PROJECT_FILE, "w")
	f.write(json.dumps(data, indent=2))
	f.close()

def read_project_file():
	try:
		f = open(PROJECT_FILE, "r") 
		data = f.read()
		f.close()
	except FileNotFoundError:
		update_project_file(DEFAULT_STRUCT)
		return read_project_file()

	if not data:
		return DEFAULT_STRUCT
	return json.loads(data)

def register_dependency(pkg, dev=False):
	key = None
	deregister_dependency(pkg)
	data = read_project_file()
	if dev:
		key = "dev-dependencies"
	else:
		key = "dependencies"
	data[key].append("{}=={}".format(pkg, get_version(pkg)))
	update_project_file(data)

def deregister_dependency(pkg):
	data = read_project_file()
	keys = ["dependencies", "dev-dependencies"]
	for key in keys:
		try:
			index = [i for i, item in enumerate(data[key]) if re.search(r'^{}[=><]'.format(pkg), item)][0]
			data[key].pop(index)
		except (ValueError, IndexError):
			continue
	update_project_file(data)

def separate_packages_n_options(command, args):
	_, packages = command.parse_args(args)
	return list(set(args).difference(set(packages))), packages

def install(args, update=False, register=True):
	c = InstallCommand()
	dev = False
	try:
		dev_option_index = args.index("-d") or args.index("--dev")
		dev = True
		args.pop(dev_option_index)
	except ValueError:
		pass

	options, packages = separate_packages_n_options(c, args)
	for pkg in packages:
		if pkg == "install":
			continue
		per_package_args = [pkg] + options
		if update:
			per_package_args.append("--upgrade")

		if c.main(per_package_args) == 0 and register:
			register_dependency(pkg, dev=dev)

def uninstall(args):
	c = UninstallCommand()
	options, packages = separate_packages_n_options(c, args)
	for pkg in packages:
		if pkg == "uninstall":
			continue
		per_package_args = [pkg] + options
		if c.main(per_package_args) == 0:
			deregister_dependency(pkg)

def update(pkgs):
	install(pkgs, update=True)

# def init(pkgs):
# 	to_ask = \
# 			{ "name": {"label": "Name", "default": None}
# 			, "description": {"label": "Description", "default": None}
# 			, "version": {"label": "Version", "default": "0.0.0"}
# 			}
# 	to_dump = {}
# 	for key, value in to_ask.items():
# 		default = value["default"]
# 		if default:
# 			to_dump[key] = input("{} ({}): ".format(value["label"], default)) or default
# 		else:
# 			to_dump[key] = input("{}: ".format(value["label"]))


# 	to_dump["dependencies"] = {}
# 	to_dump["dev-dependencies"] = {}
# 	update_project_file(to_dump)

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
		# , "init": init
		, "setup": setup
		}

def main():
	args = sys.argv[1:]
	command = args[0]
	try:
		COMMAND_MAP[command](args)
	except KeyError:
		pip.main(args)
