# methods that are used by multiple modules

import types
import yaml
import json
import ast
from sandbox.logger import logger

def save_yaml(data, path):
    with open(path, "w") as f:
        yaml.dump(data, f)

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def read_json(data):
    try:
        output = json.loads(data)
    except:
        output = ast.literal_eval(data)
    return output

def log_exceptions(func):
    """
    Decorator for logging and catching exceptions

    :param func:
    :return:
    """

    def func_wrapper(*args, **kwargs):

        try:
            logger.debug(
                f"Entering method: {func.__name__} with arguments: {args} {kwargs}"
            )
            response = func(*args, **kwargs)
            logger.debug(f"Exiting method: {func.__name__} with response: {response}")
            return response

        except Exception as e:
            logger.exception(e)
            return None

    return func_wrapper


class LogExceptions(type):
    """
    Metaclass that adds decorator to each class method
    """

    def __new__(cls, name, bases, attr):

        for name, value in attr.items():

            if type(value) is types.FunctionType or type(value) is types.MethodType:
                attr[name] = log_exceptions(value)

        return super(LogExceptions, cls).__new__(cls, name, bases, attr)
