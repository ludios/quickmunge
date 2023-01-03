#!/usr/bin/env python

from distutils.core import setup
import glob

setup(
	name="quickmunge",
	version="2.2.0",
	description="Utilities for munging data",
	packages=["quickmunge"],
	scripts=glob.glob("bin/*"),
)
