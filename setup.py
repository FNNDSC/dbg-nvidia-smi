from setuptools import setup

setup(
    name             = 'dbg-nvidia-smi',
    version          = '1.0.1',
    description      = 'A ChRIS fs plugin wrapper for nvidia-smi',
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/dbg-nvidia-smi',
    py_modules       = ['nvwrapper'],
    install_requires = ['chris_plugin~=0.0.10'],
    license          = 'MIT',
    python_requires  = '>=3.8.2',
    entry_points     = {
        'console_scripts': [
            'nvidia-smi-wrapper = nvwrapper:main'
            ]
        }
)
