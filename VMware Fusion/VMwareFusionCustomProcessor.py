#!/usr/bin/env python

""" comments go here
"""

import urllib, urllib2, gzip

from xml.etree import ElementTree
from StringIO import StringIO

# variables 
base_url = 'https://softwareupdate.vmware.com/cds/vmw-desktop/'
fusion = 'fusion.xml'

# functions
def core_metadata(url): 
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
    return core[0]

    vsus.close()

def zip_tar(metadataXML):
    request = urllib2.Request(base_url+metadataXML)
    # request.add_header('Accept-encoding', 'gzip')
    vLatest = urllib2.urlopen(request)
    buf = StringIO( vLatest.read())
    f = gzip.GzipFile(fileobj=buf)
    data = f.read()
    # print data

    try:
        metadataResponse = ElementTree.fromstring(data)
    except ExpatData:
        print "Unable to parse XML data from string"

    relativePath = metadataResponse.find("bulletin/componentList/component/relativePath")
    return relativePath.text

print base_url
metadataXML = core_metadata(base_url+fusion)
print metadataXML
ziptar = zip_tar(metadataXML)
print ziptar
download = metadataXML.replace("metadata.xml.gz", ziptar)
print download
# urllib.urlretrieve(base_url + download)

