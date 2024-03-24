from setuptools import setup, find_packages

VERSION = '1.0.5'
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
        install_requires=["Pyro5", "loguru"],
        keywords=['python', 'StreamController', "plugin"],
        classifiers= [
            "Development Status :: 3 - Beta",
            "Environment :: Plugins",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3 :: Only",
            "Operating System :: Unix",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Natural Language :: English"
        ],
        url="https://github.com/StreamController/streamcontroller-plugin-tools",
)