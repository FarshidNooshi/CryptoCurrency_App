from setuptools import setup, find_packages

setup(
    name='CryptoCurrency App',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'uvicorn',
        'fastapi',
        'databases',
        'sqlalchemy',
        'httpx',
    ],
)
