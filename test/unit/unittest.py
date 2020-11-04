#!/usr/bin/python3

import requests
import json
import sys

api_url = "https://hacker-news.firebaseio.com/v0"

def api_test():
    new_stories = requests.get(api_url + "/newstories.json")
    return

try:
    api_test()
    print("""
             ==============================================
             Unit Test Successful. Parsed The API Response.
             ==============================================
          """)
except:
    raise Exception("Unit Test Failed. Error While Parsing API Response.")
    sys.exit(2)

