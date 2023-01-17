
# Import core packages
import sys
import os import environ as env
import logging
import config

# Import internal packages
from lib import exceptions
from lib.logger import loggerPlus

# Import Third party packages

def main():

    # check version
    if not sys.version_info >=(3,):
        sys.stdout.write('Error: Requires Python version >3\n')
        sys.exit(1)

    args = sys.argv[1:]
    if len(args) < 1:
        print('Not enoug input parameters.\n' \
              'Usage python common-best-practices.py <name>')
        sys.exit(1)

    print(f'{config.REQUIREMENTS}')

if __name__ == '__main__':

    #
    # Run kickstart and build session dictionary
    #
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'config')))
    sys.path.append('.')

    import config.definitions

    #
    # Init logger plus
    #
    main_logger = LoggerPlus(glbs=main_env.getGlobals(), logdir=main_env.getGlobal('LOG_DIR'))
    logging.debug('Logging subsystem initialized')
    logging.debug(f'env globals [{main_env.getGlobals()}]')
    #loggerpp.setLogger(logdir='logs1', loglevel=logging.DEBUG)

    logging.info(f'(MAIN) {Fore.GREEN}[{main_env.getGlobal("pgmname")}] started {Style.RESET_ALL}')
    #
    # Record environment and local overrides, loaded prior to logging framework init, a bit of chicken/egg issue
    #
    logging.info('Loading env property files env.properties and local.properties from {CONFIG_DIR}')
    logging.debug('CONFIG_DIR [{}]'.format(main_env.getGlobal('CONFIG_DIR')))
    main_logger.setLogger(loglevel=main_properties.getProp('LOG_LEVEL'))


    main()

    