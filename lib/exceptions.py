import logging
import json
from lib import utils as utils

# Simple exception wrappers
class ProdException(Exception):
    def __init__(self, exception):
        self.exception = exception

    def __str__(self):
        return str(self.exception)
    #pass

class LambdaException(Exception):
    pass

def raise_exception_with_payload(response, status_code, error_code, message, event_req=None):
    logging.error(message)
    loglevel = logging.getLogger().level

    if event_req is None:
        response['payloadBody'] = {
            'statusCode': status_code,
            'error': {
                'code': error_code,
                'message': message
                },        
            'data': {
                }
            }
    else:
        response['payloadBody'] = {
            'statusCode': status_code,
            'error': {
                'code': error_code,
                'message': message
                },        
            'data': {
                },
            'params': event_req
            }
    #response = json.dumps(response)
    raise ProdException(response)

def raise_invalid_event_type(response, unknown_event_type, event_req=None):
    raise_exception_with_payload(response, 400, 40003001, f'Unknown event type:[{unknown_event_type}]', event_req=event_req)
    return

def raise_invalid_input(response, input_name, inputs, expected_type):
    raise_exception_with_payload(response, 400, 40003002, f'Invalid input for {input_name}. Must be {expected_type}: [{inputs}]')
    return

def raise_missing_input(response, input_name, expected_type):
    raise_exception_with_payload(response, 400, 40003003, f'Missing input {input_name} of type {expected_type}.')
    return

def raise_missing_header_key(response, input_name):
    raise_exception_with_payload(response, 400, 40003004, f'Missing header key {input_name}')
    return

def raise_query_returned_zero_records(response, input_name, event_req=None):
    message = f'Query returned zero records [{input_name}]'
    logging.error(message)
    loglevel = logging.getLogger().level

    response['payloadBody'] = {
        'statusCode': 204,
        'error': {
            'code': 40003005,
            'message': message
            },        
        'data': {
            },
        'params': event_req
        }
    #response = json.dumps(response)
    raise ProdException(response)   

def raise_unknown_id(response, unknown_id, message='None', event_req=None):
    raise_exception_with_payload(response, 404, 40003006, f'{message} {unknown_id}', event_req=event_req)
    return

def raise_unknown_program_error(response, message='None'):
    logging.error(message)
    loglevel = logging.getLogger().level

    response['payloadBody'] = {
        'statusCode': 400,
        'error': {
            'code': 40003007,
            'message': message
            },        
        'data': {
            }
        }
    raise ProdException(response)

def raise_missing_env_variable(response, env_var, message='None'):
    raise_exception_with_payload(response, 404, 40003008, f'Missing environment variable [{env_var}]')
    return

def raise_database_connection_error(response, database, message='Unknown database error'):
    raise_exception_with_payload(response, 404, 40003009, f'Database {database} error {message}]')
    return

def raise_boto_error(response, session, message='Boto3 session failure'):
    raise_exception_with_payload(response, 404, 400030010, f'Boto3 error {session} {message}]')

def raise_S3_error(response, file, message='S3 error'):
    raise_exception_with_payload(response, 404, 400030011, f'S3 error {file} {message}]')

def raise_pandas_error(response, function, message='error'):
    raise_exception_with_payload(response, 404, 400030012, f'Pandas {function} {message}]')

