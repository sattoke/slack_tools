#!/usr/bin/env python3
"""Tool for listing the uploaded files

This tool uses Python Slack SDK.
https://github.com/slackapi/python-slack-sdk
"""

import argparse
import json
import os

import slack_sdk


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--raw-output", action='store_true', help="Output a raw slack API response.")
    parser.add_argument("-u", "--user-id", help="Filter files created by a single user.")

    args = parser.parse_args()

    try:
        token = os.environ["SLACK_API_TOKEN"]
    except KeyError:
        print("The environment variable `SLACK_API_TOKEN` was not found. "
              "Set your Slack API token to the enviroment variable `SLACK_API_TOKEN` "
              "before running this tool by executing the following :\n"
              "    $ read -sp 'Input your Slack API token: ' SLACK_API_TOKEN; echo && export SLACK_API_TOKEN")
        exit(1)

    client = slack_sdk.WebClient(token=os.environ["SLACK_API_TOKEN"])

    api_args = {}

    if args.user_id:
        api_args["user"] = args.user_id

    # In my environment, the pagination function of SlackResponse didn't work properly,
    # so I implemented it as follows in this program
    page = 0  # page is one-based indexing.
    while True:
        page += 1
        api_args["page"] = page

        resp = client.files_list(**api_args)

        if args.raw_output:
            print(json.dumps(resp.data, ensure_ascii=False))
        else:
            for f in resp["files"]:
                print(f'{f["id"]}\t{f["user"]}\t{f["is_public"]}\t{f["name"]}"')

        if resp.data["paging"]["pages"] == resp.data["paging"]["page"]:
            break
