#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains metadata disk-based storage routines.

Note
    sdmts means 'SynDa Metadata Temporary Storage'
"""

import os
import copy
import sdconfig
import sdsqlitedict

def get_metadata_tmp_storage():

    cleanup() # empty previous storage if any

    d = sdsqlitedict.SqliteDict(path=dbfile)

    return d

def cleanup():
    if os.path.isfile(dbfile):
        os.unlink(dbfile)

class MemoryStorage():

    def __init__(self):
        self.files=[]

    def set_files(self,files):
        self.files=files

    def count(self):
        return len(self.files)

    def get_files(self):
        return self.files

    def add_attached_parameters(self,attached_parameters):
        for f in self.files:
            assert 'attached_parameters' not in f
            f['attached_parameters']=copy.deepcopy(attached_parameters)

class DatabaseStorage():
    pass

def get_store(lowmem=False):
    if lowmem:
        return DatabaseStorage()
    else:
        return MemoryStorage()

# init.

dbfilename='sdt_transient_storage.db'
dbfile=os.path.join(sdconfig.db_folder,dbfilename)
