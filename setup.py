from setuptools import setup, find_packages

setup(
    name="restframework_api_paginate",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A collection of useful Django mixins",
    long_description=open("README.md").read(),
    url="https://github.com/arnelglez/restframework_api_paginate",
    author="Arnel Gonzalez Rodriguez",
    author_email="arnel.glez@gmail.com",
    license="MIT",
    install_requires=[
        "Django>=3.0",
        "djangorestframework>=3.11",
    ],
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
