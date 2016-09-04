from setuptools import setup, find_packages
import sys, os

VERSION = '0.1.0'

with open('README.md') as f:
    long_description = f.read()

setup(
	name='NCTU-OAuth',
	version=VERSION,
	description="adds NCTU-Oauth support to tornado",
	long_description=long_description,
	classifiers=[],
	keywords='python tornado nctu oauth nctu-oauth',
	author='allenwhale',
	author_email='allencat850502@gmail.com',
	url='https://github.com/allenwhale/NCTU-OAuth',
	license='BSD',
	packages=['nctu_oauth'],
	include_package_data=True,
	zip_safe=True,
	install_requires=['tornado'])

