from setuptools import setup, find_packages

setup(
    name='pyhaproxy',
    version='0.2.2',
    keywords=('haproxy', 'parse'),
    description='A Python library to parse haproxy configuration file',
    license='MIT License',
    install_requires=[],

    include_package_data=True,
    package_data={
        'pyhaproxy': ['*.peg'],
    },

    author='Joey',
    author_email='majunjiev@gmail.com',

    url='https://github.com/imjoey/pyhaproxy',

    packages=find_packages(),
    platforms='any',
)
