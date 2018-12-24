#!/usr/bin/env python

from distutils.core import setup

setup(
	name="quickmunge",
	version="2.0.0",
	description="Utilities for munging data",
	packages=["quickmunge"],
	scripts=["bin/*"],
)
