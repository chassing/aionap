import setuptools

setuptools.setup(
    name="aionap",
    version="0.1",
    url="https://github.com/chassing/aionap",

    author="Christian Assing",
    author_email="chris@ca-net.org",

    description="Python Asyncio REST Client",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
