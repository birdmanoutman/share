# !/usr/bin/env python3
# fileinfo.py
"""
    xpan fileinfo
    include:
        search
        doclist
        imagelist
        filelist
"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from pprint import pprint
from openapi_client.api import fileinfo_api
import openapi_client


def search():
    """
    search
    """
    # Enter a context with an instance of the API client
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = fileinfo_api.FileinfoApi(api_client)
        access_token = ''  # str |
        key = "老友记"  # str |
        web = "1"  # str |  (optional)
        num = "2"  # str |  (optional)
        page = "1"  # str |  (optional)
        dir = "/"  # str |  (optional)
        recursion = "1"  # str |  (optional)

        # example passing only required values which don't have defaults set
        # and optional values
        try:
            api_response = api_instance.xpanfilesearch(
                access_token, key, web=web, num=num, page=page, dir=dir, recursion=recursion)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling FileinfoApi->xpanfilesearch: %s\n" % e)


def doclist():
    """
    doclist
    """
    # Enter a context with an instance of the API client
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = fileinfo_api.FileinfoApi(api_client)
        access_token = '126.4932acbfe7bfad408c53ca046269160e.Yayu1Mr-z6nltVEpDq9rbCfLX9jDe90NrfFpn1p.Z6cljw'  # str |
        parent_path = "/"  # str |  (optional)
        recursion = "1"  # str |  (optional)
        page = 1  # int |  (optional)
        num = 2  # int |  (optional)
        order = "time"  # str |  (optional)
        desc = "1"  # str |  (optional)
        web = "1"  # str |  (optional)

        # example passing only required values which don't have defaults set
        # and optional values
        try:
            api_response = api_instance.xpanfiledoclist(
                access_token, parent_path=parent_path, recursion=recursion, page=page, num=num, order=order, desc=desc,
                web=web)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling FileinfoApi->xpanfiledoclist: %s\n" % e)


def imagelist():
    """
    imagelist
    """
    # Enter a context with an instance of the API client
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = fileinfo_api.FileinfoApi(api_client)
        access_token = '126.4932acbfe7bfad408c53ca046269160e.Yayu1Mr-z6nltVEpDq9rbCfLX9jDe90NrfFpn1p.Z6cljw'  # str |
        parent_path = "/"  # str |  (optional)
        recursion = "1"  # str |  (optional)
        page = 1  # int |  (optional)
        num = 2  # int |  (optional)
        order = "time"  # str |  (optional)
        desc = "1"  # str |  (optional)
        web = "1"  # str |  (optional)

        # example passing only required values which don't have defaults set
        # and optional values
        try:
            api_response = api_instance.xpanfileimagelist(
                access_token, parent_path=parent_path, recursion=recursion, page=page, num=num, order=order, desc=desc,
                web=web)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling FileinfoApi->xpanfileimagelist: %s\n" % e)


def filelist():
    """
    filelist
    """
    # Enter a context with an instance of the API client
    with openapi_client.ApiClient() as api_client:
        # Create an instance of the API class
        api_instance = fileinfo_api.FileinfoApi(api_client)
        access_token = '126.4932acbfe7bfad408c53ca046269160e.Yayu1Mr-z6nltVEpDq9rbCfLX9jDe90NrfFpn1p.Z6cljw'  # str |
        dir = "/"  # str |  (optional)
        folder = "0"  # str |  (optional)
        start = "0"  # str |  (optional)
        limit = 2  # int |  (optional)
        order = "time"  # str |  (optional)
        desc = 1  # int |  (optional)
        web = "web"  # str |  (optional)
        showempty = 1  # int |  (optional)

        # example passing only required values which don't have defaults set
        # and optional values
        try:
            api_response = api_instance.xpanfilelist(
                access_token, dir=dir, folder=folder, start=start, limit=limit, order=order, desc=desc, web=web,
                showempty=showempty)
            pprint(api_response)
        except openapi_client.ApiException as e:
            print("Exception when calling FileinfoApi->xpanfilelist: %s\n" % e)


if __name__ == '__main__':
    search()
    doclist()
    imagelist()
    filelist()
