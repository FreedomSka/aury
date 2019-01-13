#!/usr/bin/env python3

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs4
import re
import sys
import argparse
from subprocess import Popen, PIPE

base_link = "https://aur.archlinux.org/packages/"

def de_html(item):
    return re.sub("<[^>]*>", '', str(item))

def parse_package(package):
    package = package.findAll('td')
    return { "title": de_html(package[0]),
             "version": de_html(package[1]),
             "description": de_html(package[4]),
             "link": package[0].a['href'] }

def get_packages(data):
    data = data.find('tbody')
    packages = [parse_package(package) for package in data.findAll('tr')]
    return packages

def get_data(url):
    data = urlopen(url)
    return bs4(data.read(), 'lxml') if data.status == 200 else None

def search(keywords):
    keywords.replace(' ', '+')
    query_link = "%s?O=0&SeB=nd&K=%s&outdated=&SB=n&SO=a&PP=50&do_Search=Go" % (base_link, keywords)
    while True:
        data = get_data(query_link)
        if data != None:
            break
    return get_packages(data)

def define_arguments():
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--search',
        metavar='<package>', required=False,
        help='search for a package in aur repo')
    
    p.add_argument('-i', '--install',
        metavar='<package>', required=False,
        help='install an aur package')
    return p

def is_installed(title):
    proc = Popen(['pacman', '-Q', title], stdout=PIPE,
                                           stderr=PIPE).communicate()
    return True if proc[0] else False

def pprint(package):
    installed = "[installed]" if is_installed(package['title']) else ""
    print('%s %s (%s) %s\n    %s' %
        (package['link'], package['version'],
         package['title'], installed, package['description']))


def get_args():
    p = define_arguments()
    if len(sys.argv) < 2:
            p.print_help()
            exit(0)
    return p.parse_args()

if __name__ == "__main__":
    args = get_args()

    if args.search:
        [pprint(package) for package in search(args.search)]
    if args.install:
        """ __TO IMPLEMENT__ """
