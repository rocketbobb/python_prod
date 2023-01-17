#
# Collection of utility functions
#
__all__ = [
    'get_function_name',
    'get_function_parameters_and_values',
    'dump',
    'dumpclean',
    'toFloat',
    'toInt',
    'getQuarterEnd',
    'strToDate',
    'strToDatetime',
    'dateToStr',
    'listToString',
    'isNumeric',
    'isBlank',
    'isWritable',
    'isAccessible',
    'isNotBlank',
    'is_empty',
    'whitespace_replace',
    'printArgsKwargs',
    'load_json',
    'keysExist',
    'myelin_payload',
    'get_file_size',
    'get_env_value'
]

# Import core libraries
import inspect
import logging
import sys
import os
import json
import datetime
import enum

def get_function_name():
    """
    :return: name of caller
    """
    return sys._getframe(1).f_code.co_name

def get_function_parameters_and_values():
    frame = inspect.currentframe().f_back
    args, _, _, values = inspect.getargvalues(frame)
    return ([(i, values[i]) for i in args])

def my_func(a, b, c=None):
    logging.info('Running ' + get_function_name() + '(' + str(get_function_parameters_and_values()) +')')
    pass

def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))

def dumpclean(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print(k)
                dumpclean(v)
            else:
                print('%s : %s'.format(k, v))
    elif isinstance(obj, list):
        for v in obj:
            if hasattr(v, '__iter__'):
                dumpclean(v)
            else:
                print(v)
    else:
        print(obj)

def isBlank (myString):
    return not (myString and myString.strip())

def isNotBlank (myString):
    return bool(myString and myString.strip())
    
# Function to convert   
def listToString(s):  
    # function to string using list comprehension
    # returning string   
    return (' '.join([str(elem) for elem in s])) 

def isNumeric(val):
    if isinstance(val, (int, float)):
        return True
    try:
        float(val)
    except ValueError:
        return False
    else:
        return True

def is_empty(any_structure):
    # any_structure returns false, is not empty
    if any_structure:
        return False
    return True

def isWritable(directory):
    try:
        tmp_prefix = "write_tester"
        count = 0
        filename = os.path.join(directory, tmp_prefix)
        while(os.path.exists(filename)):
            filename = "{}.{}".format(os.path.join(directory, tmp_prefix),count)
            count = count + 1
        f = open(filename,"w")
        f.close()
        os.remove(filename)
        return True
    except Exception as e:
        #print "{}".format(e)
        return False

#def keyExists(dict, key):
##    if key in dict.keys():
#        return True
#    return False

def keysExist(element, *keys):
    '''
    Check if *keys (nested) exists in `element` (dict).
    '''
    if not isinstance(element, dict):
        raise AttributeError('keysExist() expects dict as first argument.')
    if len(keys) == 0:
        raise AttributeError('keysExist() expects at least two arguments, one given.')

    _element = element
    for key in keys:
        try:
            _element = _element[key]
        except KeyError:
            return False
    return True

def isAccessible(path, mode='r'):
    """
    Check if the file or directory at `path` can
    be accessed by the program using `mode` open flags.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True

# Helper Functions
def toFloat(x):
    try:
        float(x)
    except:
        return x
    return float(x)

def toInt(x):
    try:
        int(float(x))
    except:
        return x
    return float(x)

def getQuarterEnd(dt):
     '''
         given a datetime object, find the end of the quarter
     '''
     quarter_of_month = int((dt.month-1)/3 + 1)
     #======================================================
     # find the first day of the next quarter
     #======================================================
     # if in last quarter then go to the next year
     year = dt.year + 1 if quarter_of_month==4 else dt.year
     # if in last quarter then month is january (or 1)
     month = 1 if quarter_of_month==4 else (quarter_of_month*3) + 1

     first_of_next_quarter = datetime.datetime(year  = year, 
                                               month = month,
                                               day   = 1
                                              )
     # last day of quarter for dt will be minus 1 day of first of next quarter
     quarter_end_dt = first_of_next_quarter - datetime.timedelta(days=1)
     return quarter_end_dt

def strToDatetime(s):
    if '/' in s:
        if float(s.split("/")[0]) > 1000.0:
            fmt = "%Y/%m/%d"
        else:    
            fmt = "%m/%d/%Y"
    elif '-' in s:
        if float(s.split("-")[0]) > 1000.0:
            fmt = "%Y-%m-%d"
        else:    
            fmt = "%m-%d-%Y"
    else:
        fmt = "%m/%d/%Y"
    try:    
        return datetime.datetime.strptime(s, fmt)
    except:
        return s

def strToDate(s):
    if '/' in s:
        if float(s.split("/")[0]) > 1000.0:
            fmt = "%Y/%m/%d"
        else:    
            fmt = "%m/%d/%Y"
    elif '-' in s:
        if float(s.split("-")[0]) > 1000.0:
            fmt = "%Y-%m-%d"
        else:    
            fmt = "%m-%d-%Y"
    else:
        fmt = "%m/%d/%Y"
    try:    
        return datetime.datetime.strptime(s, fmt).date()
    except:
        return s

def dateToStr(d, fmt="%m-%d-%Y"):
    #if d is None or pd.isnull(d) or (d[0] not in numStr) or isinstance(d, datetime.date):
    #    return ''
    #if d.year < 1900:
    #    return d
    if isinstance(d, datetime.date):
        return d.strftime(fmt)
    else:
        return d

def whitespace_replace(string):
    while '  ' in string:
        string = string.replace('  ', ' ')
    return string.replace('\n', '')

def printArgsKwargs(*args, **kwargs):
    print(f' Args: [{args}]')
    print(f' Kwargs: [{kwargs}]')

def load_json(file=None):
    rc = 0
    dict = {}

    # load config values
    if file is None:
        print('Error: missing json filename')
        return 1, None

    logging.debug(f'file =[{file}]')

    try:
        with open(file) as jsonfile_contents:
            try:
                dict = json.load(jsonfile_contents)
            except json.JSONDecodeError as e:
                print(f'json error [{e}]')
                rc = 1
    except:
        print(f'Unknown exception {sys.exc_info()}')
        rc = 1
    return rc, dict

# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4

def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes

def get_file_size(file_name, size_type = SIZE_UNIT.BYTES ):
   """ Get file in size in given unit like KB, MB or GB"""
   size = os.path.getsize(file_name)
   return convert_unit(size, size_type)

def myelin_payload(payloadType=None, 
    payloadVersion="0.1.0",
    requestTimestamp=None,
    source="myelin_api"):

    payload = {
        "payloadHeaders": {
        "apiVersion": "1.0.0",
        "correlator": "user:1",
        "payloadType": payloadType,
        "payloadVersion": payloadVersion,
        "requestor": "self",
        "requestTimestamp": requestTimestamp,
        "responseTimestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%z"),
        "source": source
        },
    "payloadBody": {
        }
    }
    return payload

def myelin_header():
    return header

def get_env_value(env_var=None):
    if env_var in os.environ:
        return os.getenv(env_var)
    else:
        msg = 'Missing environment variable [SM_CRED]'
        logging.error(f'{msg}')
        raise Exception(msg)
        return 

def main():
    my_func(a=1, b=2)

    foo = None
    print(f' None test {isBlank(foo)}')
    foo = ''
    print(f' \'\' string empty {isBlank(foo)}')
    foo = ' '
    print(f' \'   \' string with spaces test {isBlank(foo)}')
    print(f' \'   \' isNotBlank test {isNotBlank(foo)}')

    data = {
        "spam": {
            "egg": {
                "bacon": "Well..",
                "sausages": "Spam egg sausages and spam",
                "spam": "does not have much spam in it"
            }
        }
    }
    print('spam (exists): {}'.format(keysExist(data, "spam")))
    print('spam > bacon (do not exists): {}'.format(keysExist(data, "spam", "bacon")))
    print('spam > egg (exists): {}'.format(keysExist(data, "spam", "egg")))
    print('spam > egg > bacon (exists): {}'.format(keysExist(data, "spam", "egg", "bacon")))

if __name__ == '__main__':
    pgmname = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    print(f'\n**** Running main Program [{pgmname}]\n')

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] -> %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    #print(f'This is {Fore.GREEN}color{Style.RESET_ALL}!')
    #logging.info(f'key {Fore.GREEN}[{key}] value [{value}]{Style.RESET_ALL}')

    main()
    
    print(f'\n**** Main clean exit [{pgmname}]\n')
    sys.exit(0)
    
    # end of main