from setuptools import setup, find_packages

setup(
    name="CosmicWatchSerial",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyserial",
        "numpy",
        "matplotlib"
    ],
    entry_points={
        "console_scripts": [
            "cosmic_watch_serial=CosmicWatchSerial.__main__:main",
        ],
    },
    author="John Meneghini",
    author_email="jp.meneghini412@gmail.com",
    description="A utility to handle data from the Cosmic Watch Detector.",
    keywords="cosmic watch, detector, serial communication",
    url="https://github.com/jmeneghini/Updating-Cosmic-Watch",
)

