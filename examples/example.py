#!/usr/bin/env python

import asyncio
import os
import sys

FILE_DIR = os.path.dirname(__file__)
# aionap dir
sys.path.append(f"{FILE_DIR}/..")
# tox venv
sys.path.append(f"{FILE_DIR}/../.tox/py36/lib/python3.6/site-packages/")
assert sys.version_info >= (3, 6), "python >= 3.6 is required"

import aionap  # noqa


async def main():
    # Create a resource for the API
    async with aionap.API('https://jsonplaceholder.typicode.com') as demo:
        # Send a GET request to https://jsonplaceholder.typicode.com/users
        users = await demo.users.get()

    print(f"In total {len(users)} users:")
    for user in users:
        print(f"Name: {user['name']} Company: {user['company']['name']}")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
