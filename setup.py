from setuptools import setup, find_packages

setup(
    name='agrosmart',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'psycopg2-binary',
    ],
)
