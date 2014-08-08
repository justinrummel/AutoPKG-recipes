#!/usr/bin/python
#
# Copyright 2014 Justin Rummel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import shutil
import subprocess

from xml.etree import ElementTree
from autopkglib import Processor, ProcessorError

__all__ = ["FlatPkgFromBundle"]

class FlatPkgFromBundle(Processor):
    
    # Modifies the Bundle installer pkg so that:
    #
    # The basic set of operations:
    #
    # 1) pax -rzf Archive.pax.gz
    # 2) Reflatten the pkg with pkgutil --flatten
    #
    # Note that this will remove any signing that is present. This is actually
    # OK; it should not prevent any distribution system (Munki, Casper, etc)
    # from installing this package.
    #
    # Lots of code "borrowed" from AdobereaderRepackager.py by Greg Neagle
    #

    description = "Finds the Bundle.PKG from a pkg recipe, expands by pax -rzf, then flattens to a Flat PKG for automated deployment (like the Casper Suite)."
    input_variables = {
        "pkg_path": {
            "required": True,
            "description": "Path to a bundle PKG.",
        },
    }
    output_variables = {
        "flat_pkg_path": "Path to the repackaged package."
    }

    __doc__ = description

    def expand(self, pkg_path, expand_dir):
        '''Uses pax to expand a bundle package.'''

        if os.path.isdir(expand_dir):
            try:
                shutil.rmtree(expand_dir)
            except (OSError, IOError), err:
                raise ProcessorError(
                    "expand Can't remove %s: %s" % (expand_dir, err))
        try:
            subprocess.check_call(
                ['/bin/pax', '-rzf', pkg_path+"/Contents/Archive.pax.gz"])
        except subprocess.CalledProcessError, err:
            raise ProcessorError("%s expanding %s" % (err, pkg_path))

    def flatten(self, expanded_pkg, destination):
        '''Flatten an expanded flat pkg'''
        if os.path.exists(destination):
            try:
                os.unlink(destination)
            except OSError, err:
                raise ProcessorError(
                    "flatten Can't remove %s: %s" % (destination, err))
        try:
            subprocess.check_call(
                ['/usr/sbin/pkgutil', '--flatten', expanded_pkg, destination])
        except subprocess.CalledProcessError, err:
            raise ProcessorError(
                "%s flattening %s" % (err, expanded_pkg))

    def main(self):
        expand_dir = os.path.join(self.env["RECIPE_CACHE_DIR"], "NAME")
        modified_pkg = os.path.join(self.env["RECIPE_CACHE_DIR"], os.path.basename(self.env["pkg_path"]))
        expanded_pkg = self.expand(self.env["pkg_path"], expand_dir)
        self.flatten(expanded_pkg, modified_pkg)
        self.env["pkg_path"] = modified_pkg

if __name__ == "__main__":
    processor = FlatPkgFromBundle()
    processor.execute_shell()
