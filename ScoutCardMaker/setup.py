from setuptools import setup, find_packages

setup(
    name= "scout-card-maker",
    version= '0.1',
    packages= find_packages(),
    install_requires= [
        'ply',
    ]
)