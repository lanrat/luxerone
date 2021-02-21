#!/usr/bin/env python3

import luxerone
import os
import pprint
import getpass
import sys

token_env_name = 'LUXERONE_TOKEN'
token = os.getenv(token_env_name)

# if there is no token set, ask the user for credentials to authenticate
if not token:
    print("Enter Luxer Credentials")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    try:
        token = luxerone.login(username, password)
    except Exception as err:
        print("Error: {0}".format(err))
        sys.exit(2)
    os.environ[token_env_name] = token
    print("token: \"%s\"" % token)

# display user information
user_info = luxerone.user_info(token)
print("user info:")
pprint.pprint(user_info)

# print all pending packages
pending = luxerone.pending(token)
print("pending (%d):" % len(pending))
luxerone.print_packages(pending)

# print last 10 packages
history = luxerone.history(token)
print("history:")
luxerone.print_packages(history, 30)
