from setuptools import setup, find_packages
import sys, os

VERSION = '0.1.2'

if os.path.exists('README.md'):
    long_description = open('README.md').read()
else:
    long_description = ''

setup(
	name='tornado-NCTU-OAuth',
	version=VERSION,
	description="adds NCTU-OAuth support to tornado",
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

