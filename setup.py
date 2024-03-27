from setuptools import setup, find_packages

VERSION = '2.0.0'
DESCRIPTION = 'Base for StreamController plugins'
LONG_DESCRIPTION = 'This package contains the base for StreamController plugins.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="streamcontroller-plugin-tools", 
        version=VERSION,
        author="Core447",
        author_email="core447@proton.me",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["rpyc", "loguru"],
        keywords=['python', 'StreamController', "plugin"],
        classifiers= [
            "Development Status :: 4 - Beta",
            "Environment :: Plugins",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3 :: Only",
            "Operating System :: Unix",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Natural Language :: English"
        ],
        url="https://github.com/StreamController/streamcontroller-plugin-tools",
)