# ######################################################################
# 
# Program:  set_environment.py
#
# Purpose:  Creates global environment variables and dictionaries
#
# Notes:
#
# ######################################################################

# Import core libraries
import os
import sys
import datetime
import json
import logging
from pprint import pprint

# Import internal libraries
from lib import utils
#import config.definitions

class Init_Env:

    def __init__(self):

        #globals.ginit()
        # global env dict and variables
        self.pgmname = os.path.splitext(os.path.basename(sys.argv[0]))[0]

        env_dict = {}
        env_dict['pgmname'] = self.pgmname
        env_dict['runid'] = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        #env_dict['CONFIG_DIR'] = config.definitions.CONFIG_DIR
        #env_dict['ROOT_DIR'] = config.definitions.ROOT_DIR
        env_dict['LOG_DIR'] = 'logs'
        env_dict['LOG_LEVEL'] = 'logging.info'

        # TODO Sort of a placeholder for now
        MANDATORY_ENV_VARS = ['PATH']

        for var in MANDATORY_ENV_VARS:
            if var not in os.environ:
                raise EnvironmentError("Failed because {} is not set.".format(var))
            env_dict[var] = os.environ[var]

        # optional environment variables
        # TODO support LOG_LEVEL as an optional environment variables
        if 'LOG_LEVEL' in os.environ:
            env_dict = {'LOG_LEVEL': os.environ['LOG_LEVEL']}
        if 'LOG_DIR' in os.environ:
            env_dict = {'LOG_DIR': os.environ['LOG_DIR']}

        # create globals dictionary
        self.globals_dict = {'globals': env_dict}
        self.env_dict = env_dict

        return

    def getPgmName(self):
        return self.pgmname

    def getGlobal(self, key):
        return self.globals_dict['globals'][key]

    def setGlobal(self, key, value):
        self.globals_dict['globals'][key] = value
        return

    def listGlobals(self):
        # display list of global setting
        #for x in self.globals_dict:
        for y in self.globals_dict['globals']:
            print("\t", y, ":", self.globals_dict['globals'][y])
        return

    def getGlobals(self):
        # return just the k:v pairs in globals
        return self.globals_dict['globals']

    def addGlobal(self, dict):
        return self.globals_dict['globals'].update(dict)

if __name__ == '__main__':
    pgmname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    print(f'\n**** Running main Program [{pgmname}]\n')

    sys.path.append('.')

    pg_env = Init_Env()

    print(f'program name:[{pg_env.getPgmName()}]')
    
    print('\n**** Listing globals')
    pg_env.listGlobals()

    print(f'\n**** Main clean exit [{pgmname}]\n')
    sys.exit(0)