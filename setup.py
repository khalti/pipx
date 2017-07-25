from setuptools import setup, find_packages
import sys, os
from pipx import gen_setup_kwargs


setup(**gen_setup_kwargs())
