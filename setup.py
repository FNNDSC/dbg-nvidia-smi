from setuptools import setup

setup(
    name             = 'dbg-nvidia-smi',
    version          = '1.0.10',
    description      = 'A ChRIS fs plugin wrapper for nvidia-smi',
    author           = 'FNNDSC',
    author_email     = 'dev@babyMRI.org',
    url              = 'https://github.com/FNNDSC/dbg-nvidia-smi',
    py_modules       = ['nvwrapper'],
    install_requires = ['chris_plugin==0.0.17', 'importlib_metadata'],
    license          = 'MIT',
    entry_points     = {
        'console_scripts': [
            'nvidia-smi-wrapper = nvwrapper:main'
            ]
        }
)
