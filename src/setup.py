import os
import glob
import shutil
from setuptools import setup, find_packages, Command
from pathlib import Path
from typing import List


class CompleteClean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree('./build', ignore_errors=True)
        shutil.rmtree('./dist', ignore_errors=True)
        shutil.rmtree('./' + project + '.egg-info', ignore_errors=True)
        temporal = glob.glob('./' + project + '/*.pyc')
        for t in temporal:
            os.remove(t)


def get_install_requires() -> List[str]:
    """Returns requirements.txt parsed to a list"""
    # pasar toml a requirements

    fname = Path(__file__).parent / 'requirements.txt'
    targets = []
    if fname.exists():
        with open(fname, 'r', encoding="utf-8") as f:
            targets = f.read().splitlines()
    return targets


VERSION = '1.0.0'
DESCRIPTION = 'Engie_challenge'
LONG_DESCRIPTION = 'Engie_challenge'

project = "engie_api_package"
# Configurando
setup(
    name=project,
    python_requires='>=3.9.13',
    version=VERSION,
    author="rosalia Contreras Moreira",
    author_email="<rosalia@email.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_dir={'engie_api_package': 'engie_api'},
    # data_files=[('config', ['extractor_api/config/config.yaml']), ('data', ['extractor_api/config/data.json'])],
    entry_points={'console_scripts': ['extractor_api_package=extractor_api :main']},
    include_package_data=True,
    zip_safe=False,
    install_requires=get_install_requires(),
    cmdclass={'clean': CompleteClean},
    test_suite='nose.collector'
)