
from setuptools import setup, find_packages

version = '0.0.2'

setup(
    name="athena-cli",
    version=version,
    description='Presto-like CLI for AWS Athena',
    url='https://github.com/guardian/ophan-data-lake',
    license='MIT',
    author='Nick Satterly',
    author_email='nick.satterly@theguardian.com',
    packages=find_packages(),
    py_modules=['athena_cli'],
    install_requires=[
        'boto3',
        'cmd2',
        'tabulate'
    ],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'athena = athena_cli:main'
        ]
    },
    keywords='aws athena presto cli',
    classifiers=[
        'Topic :: System :: BigData'
    ]
)