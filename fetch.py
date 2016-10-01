#!/usr/bin/env python
# -*- coding: utf-8 -*-
__date__= '10 01, 2016 '
__author__= 'mkfsn'


import os
import requests
from pyquery import PyQuery
import urllib
from urllib2 import URLError, HTTPError
from socket import error as socket_error


def download(resource, location=None):

    if os.path.isfile(resource):
        return

    if resource.startswith("http") or location is None:
        location, resource = resource.rsplit("/", 1)

    link = (location + "/" + resource).encode('utf8')
    try:
        if '/' in resource:
            directories, resource = resource.rsplit('/', 1)
            os.makedirs(directories)
        urllib.urlretrieve(link, resource)
    except IOError as e:
        print "resource=%s, location=%s" % (resource, location)
        print e


def download_page(url, prefix=None, deep=True):

    if prefix is not None:
        url = prefix + "/" + url
    print "Fetching ... %s" % url

    r = requests.get(url)
    r.encoding = 'UTF-8'
    prefix, filename = url.rsplit("/", 1)

    if os.path.isfile(filename):
        print "[Done] %s" % url
        return
   
    pq = PyQuery(r.text)
    for link in pq("link[rel=stylesheet]"):
        download(pq(link).attr("href"), prefix)

    for script in pq("script"):
        src = pq(script).attr("src")
        if src is not None:
            download(src, prefix)

    for img in pq("img"):
        download(pq(img).attr("src"), prefix)

    if deep:
        for a in pq("a"):
            download_page(pq(a).attr("href"), prefix, deep=False)

    with open(filename, "w") as f:
        f.write(r.text.encode('utf-8'))
     
    print "[Done] %s" % url


def main():
    download_page("http://www.csie.ntnu.edu.tw/~u91029/index.html")


if __name__ == '__main__':
    main()
