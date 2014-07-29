#!/usr/bin/env python

""" comments go here
"""

import urllib2

vsus = urllib2.urlopen("https://softwareupdate.vmware.com/cds/vmw-desktop/fusion.xml")
print vsus.info()
fusion = vsus.read()


vsus.close()
