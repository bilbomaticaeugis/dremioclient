#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Ryan Murray.
#
# This file is part of Dremio Client
# (see https://github.com/rymurr/dremio_client).
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

"""The setup script."""

from setuptools import find_packages, setup


requirements = ["Click>=6.0", "requests>=2.21.0", "pyarrow", "confuse", "simplejson", "attrs", "six"]

requirements_noarrow = ["pandas>=0.24.2", "requests-futures==1.0.0", "markdown"]

requirements_full = ["pyarrow", "pandas>=0.24.2", "requests-futures==1.0.0", "markdown"]

setup_requirements = []

test_requirements = []

setup(
    author="Bilbomatica",
    author_email="oesparza@bilbomatica.es",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Python client for Dremio with fixed flight connector  . See https://dremio.com",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description="",
    include_package_data=True,
    keywords="dremio_client_eea",
    name="dremio_client_eea",
    packages=find_packages(
        include=[
            "dremio_client_eea",
            "dremio_client_eea.flight",
            "dremio_client_eea.auth",
            "dremio_client_eea.model",
            "dremio_client_eea.util",
            "dremio_client_eea.conf",
        ]
    ),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/bilbomaticaeugis/dremioclient",
    version="0.1.0",
    zip_safe=False,
    extras_require={
        ':python_version == "2.7"': ["futures"],
        "full": requirements_full,
        "noarrow": requirements_noarrow,
    },
    entry_points={"console_scripts": ["dremio_client_eea=dremio_client_eea.cli:cli"]},
)