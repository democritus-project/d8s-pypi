"""Democritus functions for interacting with Pypi."""

from typing import Iterable, List, Tuple

from democritus_core import get, html_elements_with_tag, chunk

BASE_URL_WITHOUT_VERSION = 'https://pypi.org/pypi/{}/json'
BASE_URL_WITH_VERSION = 'https://pypi.org/pypi/{}/{}/json'
DOWNLOAD_LIST_URL = 'https://pypi.org/simple/{}/'


# todo: write a function to determine if something is a pypi package


def pypi_package_data(package_name: str, *, version: str = None):
    if version:
        url = BASE_URL_WITH_VERSION.format(package_name, version)
    else:
        url = BASE_URL_WITHOUT_VERSION.format(package_name)

    result = get(url)
    return result


# TODO: would like to support a version for the pypi_package_download... functions


def pypi_package_download_links(package_name: str) -> Iterable[List[Tuple[str, str]]]:
    """Get the download links for the given package."""
    download_list_url = DOWNLOAD_LIST_URL.format(package_name)
    html_content = get(download_list_url)
    links = html_elements_with_tag(html_content, 'a')
    hrefs = [a['href'] for a in links]
    # we chunk the links to group the .tar.gz and .whl files for the same version
    grouped_hrefs = chunk(hrefs, 2)
    return grouped_hrefs


def pypi_package_download(package_name: str, download_path: str):
    """Download the given package into the given directory."""
    download_links = pypi_package_download_links(package_name)


# TODO: I would like the response from pypi_packages_all to be similar to the response from pypi_packages_new


def pypi_packages_new():
    from rss import rss_parse

    url = 'https://pypi.org/rss/packages.xml'
    results = rss_parse(url)
    return results


def pypi_packages_all_names():
    from democritus_core import get, html_text, list_delete_empty_items

    url = 'https://pypi.org/simple/'
    html_results = get(url)
    text = html_text(html_results)
    all_names = list_delete_empty_items([i.strip() for i in text.split('\n')])
    # we go from [2:] because the top two items in all_names are not the names of packages (they are metadata from the html page)
    all_names = all_names[2:]
    return all_names


def pypi_packages_recent():
    from rss import rss_parse

    url = 'https://pypi.org/rss/updates.xml'
    results = rss_parse(url)
    return results
