# !/usr/bin/env python3
"""
    xpan userinfo
    include:
        user_info
        user_quota
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
import openapi_client
from openapi_client.api import userinfo_api
from pprint import pprint


def user_quota():
    """
    user_quota demo
    """
    # Enter a context with an instance of the API client
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = userinfo_api.UserinfoApi(api_client)
        access_token = "126.4932acbfe7bfad408c53ca046269160e.Yayu1Mr-z6nltVEpDq9rbCfLX9jDe90NrfFpn1p.Z6cljw"  # str |
        checkexpire = 1  # int |  (optional)
        checkfree = 1  # int |  (optional)

        # example passing only required values which don't have defaults set
        # and optional values
        try:
            api_response = api_instance.apiquota(access_token, checkexpire=checkexpire, checkfree=checkfree)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling UserinfoApi->apiquota: %s\n" % e)


def user_info():
    """
    user_info demo
    """
    # Enter a context with an instance of the API client
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = userinfo_api.UserinfoApi(api_client)
        access_token = "126.4932acbfe7bfad408c53ca046269160e.Yayu1Mr-z6nltVEpDq9rbCfLX9jDe90NrfFpn1p.Z6cljw"  # str |

        # example passing only required values which don't have defaults set
        try:
            api_response = api_instance.xpannasuinfo(access_token)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling UserinfoApi->xpannasuinfo: %s\n" % e)


if __name__ == '__main__':
    """
    main
    """
    user_quota()
    user_info()
