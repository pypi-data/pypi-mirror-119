# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tzar']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['tzar = tzar.cli:run']}

setup_kwargs = {
    'name': 'tzar',
    'version': '0.1.5',
    'description': 'Manage: Tar, Zip, Anything Really!',
    'long_description': '# Tzar: Tar, Zip, Anything Really\n\nEasy compression and extraction for any compression or archival format.\n\n![Demo GIF](../assets/tzar.gif?raw=true)\n\n## Usage/Examples\n\n```bash\ntzar compress large-dir compressed.tar.gz\ntzar extract compressed.tar.gz large-dir\ntzar list compressed.tar.gz\n```\n\nIt\'s always `tzar <command> <source> [<destination>]`\n\n## Installation\n\nThe package is published in PyPi under `tzar`. You can install it with the following methods\n\n### [Pipx](https://pypa.github.io/pipx/) (recommended)\n\n```bash\npipx install tzar\n```\n\n### Pip\n\n```bash\npip3 install tzar\n```\n\n### Dev\n\n```\ngit clone git@github.com:DanielVZ96/tzar\ncd tzar\npoetry install\nexport TZAR_CONFIG=$PWD/config\n```\n\n## Configuration\n\nConfiguration is read from the standard directories for each OS (~/.config/tzar/*.toml). You\n can add any number of toml files to that directory and they will all be read by tzar at runtime.\n \nThe configuration file has the following format:\n\n``` toml\n[command or format]\nextract = "command extract ${verbose} ${filename} ${directory}" \ncompress = "command compress ${verbose} ${directory} ${filename}" \nshow = "command list ${verbose} ${filename}" \nextensions = [".ext1",".ext2"]\nverbose = "-v" \n\n[another command or format]\nextract = "another x${verbose} ${filename} ${directory}" \ncompress = "another c${verbose} ${directory} ${filename}" \nshow = "another list ${verbose} ${filename}" \nextensions = [".anoth"]\nverbose = "v" \n```\n\nAll commands should have the `extract`, `compress`, `show`, `extensions` and `verbose` values defined.\nThey are all self explanatory; they define templates for the commands to run, the extensions\nfor these commands, and how you can ask for a verbose output.\n\nThey can all contain the following template variables that will be replaced at runtime:\n\n-`verbose`: Defines how and where to ask for a verbose output (defined in the `verbose =` variable definition). \n\n-`filename`: The name of the compressed file. Corresponds to `<source>` in the `extract` and `list` subcommands, and to `<destination>` in the `compress` subcommand\n\n-`directory`: The target directory. Corresponds to `<destination>` in the `extract` and `list` subcommands, and to `<source>` in the `compress` subcommand\n\n## Why?\n\n1) Because I think it\'s simpler\n\nYou may think that this should be doable with aliases, but I tried and I couldn\'t. Maybe you can use the [`fuck`](https://github.com/nvbn/thefuck) app \nor [`tldr`](https://github.com/tldr-pages/tldr) but I still feel it could be simpler to extract files (*wtf does xvzf even mean?*).\n\n2) Because I wanted to try the idea of Code as Configuration\n\nMaybe this sounds crazy, but I started this project by exploring the idea of storing the main behaviour of code in configuration files (in this case TOML), in order to \nease extensibility, reduce posible errors, and keep things simple. In my dayjob we tried this idea with my colleagues and the result is that changes that previously\nspawned several files or lines of code, are now reduced into 2 or 3 hard-to-fuck-up yaml lines. If this project gains traction I may write a blog post about this.\n\n## TODO\n\n- [-] Add a ton of new file formats\n- [ ] Document code\n- [ ] Interactive prompt\n- [ ] Tests (Don\'t judge, I\'m coding this in the spare time I have during my lunch breaks.)\n\n## Authors\n\n- [@danielvalenzuela](https://www.github.com/danielvz96)\n',
    'author': 'Daniel Valenzuela',
    'author_email': 'daniel@admetricks.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DanielVZ96/tzar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
