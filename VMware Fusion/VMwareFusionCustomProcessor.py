#!/usr/bin/env python

""" comments go here
"""

import urllib, urllib2

from xml.etree import ElementTree

url = 'https://softwareupdate.vmware.com/cds/vmw-desktop/fusion.xml'
request = urllib2.Request(url)

try:
    vsus = urllib2.urlopen(request)
except URLError, e:
    print e.reason

data = vsus.read()
# print data

try:
    metaList = ElementTree.fromstring(data)
except ExpatData:
    print "Unable to parse XML data from string"

versions = []
for metadata in metaList:
    version = metadata.find("version")
    versions.append(version.text)

versions.sort()
latest = versions[-1]
# print latest

urls = []
for metadata in metaList:
    url = metadata.find("url")
    urls.append(url.text)

matching = [s for s in urls if latest in s]
core = [s for s in matching if "core" in s]
print core[0]

vsus.close()
