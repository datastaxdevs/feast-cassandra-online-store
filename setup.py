from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="feast-cassandra",
    version="0.1.3",
    author="Stefano Lottini",
    author_email="stefano.lottini@datastax.com",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    # entry_points={
    #     "console_scripts": [
    #         "command=importable:function",
    #     ],
    # },
    url="https://github.com/datastaxdevs/feast-cassandra-online-store",
    license="LICENSE.txt",
    description="Cassandra/Astra DB support for Feast online store",
    long_description=(here / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    python_requires=">=3.7.0",
    install_requires=[
        "cassandra-driver>=3.24.0,<4",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        #
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="feast, cassandra, mlops",
)
