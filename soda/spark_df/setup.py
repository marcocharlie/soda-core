#!/usr/bin/env python

from setuptools import find_namespace_packages, setup

package_name = "soda-core-spark-df"
package_version = "3.0.48"
description = "Soda Core Spark Dataframe Package"

requires = [
    f"soda-core-spark=={package_version}",
    "pyspark",
]
# TODO Fix the params
setup(
    name=package_name,
    version=package_version,
    install_requires=requires,
    packages=find_namespace_packages(include=["soda*"]),
)
