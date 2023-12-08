from setuptools import setup, find_packages

setup(
    name="rest_framework_api_paginate",
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
        "drf-spectacular>=0.17.2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Django",
        "Framework :: Django :: 3.0",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
