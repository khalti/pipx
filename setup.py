from setuptools import setup, find_packages
import sys, os
import json

# https://docs.python.org/2/distutils/setupscript.html

def read_file(filename):
	f = open(filename)
	data = f.read()
	f.close
	return data

kwargs =  {
  "keywords": "pip",
  "version": "0.1.0",
  "packages": find_packages(exclude=["tests"]),
  "url": "https://github.com/janakitech/pipx",
  "entry_points": {
    "console_scripts": [
      "pipx=pipx:main",
      "px=pipx:main",
    ]
  },
  "description": "pip extended",
  "install_requires": json.loads(read_file("project.json"))["dependencies"],
  "long_description": read_file("readme.md"),
  "name": "pipx",
  "license": read_file("license.txt"),
  "author_email": "sth.srn@gmail.com",
  "author": "ludbek"
}

setup(**kwargs)
