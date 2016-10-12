import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='flowbot-barebones',
    version='0.1',
    package_dir={"flowbot": "src"},
    packages=["flowbot"],
    license='MPL 2.0',
    description='A boilerplate for flowbots.',
    long_description=README,
    url='https://github.com/SpiderOak/flowbot-barebones',
    author='Quentin Donnellan',
    author_email='quentin@spideroak.com'
)
