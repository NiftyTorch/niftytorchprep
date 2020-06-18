from setuptools import setup

requirements = [
    'click>=7.1.1',
    'invoke>=1.4.1',
    'scikit-learn>=0.22.1'
]

setup(
    name = 'niftytorchprep',
    version = '0.0.1',
    packages = ['niftytorchprep'],
    install_requires = requirements,
    entry_points = {
        'console_scripts': [
            'niftytorchprep = niftytorchprep.__main__:cli'
        ]
    })
