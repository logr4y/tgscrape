#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DB class"""

import json
import os
import config

class DB:
    """ Output handling """
    logfile = ''

    def __init__(self, lgroup):
        """ Class constructor """
        self.logfile = '{}{}.json'.format(config.output_folder, lgroup.lower())
        if not os.path.exists(config.output_folder):
            os.makedirs(config.output_folder)

    def load_data(self, create=True):
        """ Returns current conversation """
        try:
            with open(self.logfile) as fp:
                return {int(key): value for key, value in json.load(fp).items()} 
        except IOError:
            if create:
                with open(self.logfile, 'w') as fp:
                    pass
            return {}

    def write_data(self, ldb):
        """ Saves conversation to file """
        print('Writing to {}...'.format(self.logfile))
        with open(self.logfile, 'w') as fp:
            json.dump(ldb, fp)
