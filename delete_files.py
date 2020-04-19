#!/usr/bin/env python3
"""Tool for deliting the uploaded files

This tool uses `python-slackclient`.
https://github.com/slackapi/python-slackclient
"""

import argparse
import json
import os
import sys

import slack


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list-file",
                        default="-",
                        help="list of file IDs to be deleted. "
                        "The default value is '-'. "
                        "If it is '-', the list is read from the standard input."
                        "This list assumes a space-separated format "
                        "with the ID of the file uploaded to slack in the first column. "
                        "This format follows the output of `list-files.py`. "
                        "The tool assumes that the user edits the output "
                        "of `list-files.py` with an editor, etc., "
                        "and then inputs it into `delete-files.py`.")

    args = parser.parse_args()

    try:
        token = os.environ["SLACK_API_TOKEN"]
    except KeyError:
        print("The environment variable `SLACK_API_TOKEN` was not found. "
              "Set your Slack API token to the enviroment variable `SLACK_API_TOKEN` "
              "before running this tool by executing the following :\n"
              "    $ read -sp 'Input your Slack API token: ' SLACK_API_TOKEN; echo && export SLACK_API_TOKEN")
        exit(1)

    client = slack.WebClient(token=os.environ["SLACK_API_TOKEN"])

    def delete_from(list_file):
        for line in list_file:
            file_id = line.split()[0]

            resp = client.files_delete(file=file_id)
            print(json.dumps(resp.data, ensure_ascii=False))

    if args.list_file == "-":
        delete_from(sys.stdin)
    else:
        with open(args.list_file, mode='r') as f:
            delete_from(f)
