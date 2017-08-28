import setuptools
import sys

if sys.version_info < (3, 6, 0):
    raise RuntimeError("aiohttp requires Python 3.6.0+")


setuptools.setup(
    name="aionap",
    version="0.3",
    url="https://github.com/chassing/aionap",

    author="Christian Assing",
    author_email="chris@ca-net.org",

    description="Python Asyncio REST Client",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(exclude=['docs', 'tests*']),

    install_requires=open('requirements.txt').readlines(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
