"""Tests for `democritus_pypi` module."""

from democritus_pypi import pypi_package_data, pypi_packages_new, pypi_packages_all_names, pypi_packages_recent


def test_pypi_package_data_1():
    results = pypi_package_data('ioc-finder')
    assert results['info']['author'] == 'Floyd Hightower'
    assert results['info']['description'].startswith('# Observable Finder')
    assert '2.1.0' in results['releases']

    # try requesting details about a package using a specific version
    results = pypi_package_data('ioc-finder', version='1.0.5')
    assert results['info']['author'] == 'Floyd Hightower'
    assert results['info']['description'].startswith('Copyright (c) 2018, Floyd Hightower')
    assert results['info']['version'] == '1.0.5'


def test_pypi_packages_new_1():
    results = pypi_packages_new()
    assert len(results) == 10


def test_pypi_packages_recent_1():
    results = pypi_packages_recent()
    assert len(results) == 10
