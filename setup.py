from setuptools import setup, find_packages
from denigma.utils.utils import (
    Constants,
    get_charlist_json,
    get_config_json,
    save_charlist_json,
    save_config_json,
)

setup(
    name="denigma",
    version=Constants.VERSION,
    packages=find_packages(),
    install_requires=[
        "pandas",
    ],
    entry_points={
        "console_scripts": [
            "denigma=denigma.main:main",
        ],
    },
    author="Antoni Bertolin Monferrer",
    author_email="tonibm1220@gmail.com",
    url="https://github.com/tobe2098/denigma",
    python_requires=">=3.6",
    description="ENIGMA machine emulator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

save_charlist_json(dictionary=get_charlist_json())
save_config_json(dictionary=get_config_json())
