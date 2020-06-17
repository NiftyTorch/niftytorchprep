from setuptools import setup

setup(
    name = 'niftytorchprep',
    version = '0.0.1',
    packages = ['niftytorchprep'],
    entry_points = {
        'console_scripts': [
            'niftytorchprep = niftytorchprep.__main__:cli'
        ]
    })
