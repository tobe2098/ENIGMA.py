from setuptools import setup, find_packages
from utils.utils import (
    Constants,
    get_charlist_json,
    get_config_json,
    save_charlist_json,
    save_config_json,
)

# find_packages() automatically finds all Python packages in your project
# It looks for folders containing __init__.py files
# In your case it will find: cli, core, docs, gui, scripts
# You can exclude packages with the 'exclude' parameter if needed
setup(
    name="denigma",
    version=Constants.VERSION,
    packages=find_packages(),  # This finds cli/, core/, etc.
    install_requires=[
        # Add any external dependencies your project needs
    ],
    entry_points={
        "console_scripts": [
            "denigma=denigma.main:main",  # This creates the 'denigma' command
        ],
    },
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/your_username/your_library_repo",
    classifiers=[
        "Programming Language :: Python :: 3",
        # Add other classifiers as needed
    ],
)

save_charlist_json(dictionary=get_charlist_json())
save_config_json(dictionary=get_config_json())
