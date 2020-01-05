#!/usr/bin/env python3
"""Tool for saving the slack channel log

This tool uses `python-slackclient`.
https://github.com/slackapi/python-slackclient
"""

import argparse
import json
import os

import slack


def get_channel_id(client, channel_name):
    """Get the channel ID from the channel name.

    Parameters
    ----------
    client : slack.web.client.WebClient
        slack client object.
    channel_name : str
        channel name of public channel or private channel.

    Returns
    -------
    channel_id : str
        channel ID.

    Raises
    ------
    ValueError
        occur if the specified channel is not found.

    """
    resp = client.conversations_list(types="public_channel,private_channel")

    for _ in resp:
        channel_ids = [x["id"] for x in resp["channels"] if x["name"] == channel_name]

        if len(channel_ids) >= 1:
            channel_id = channel_ids[0]
            break
    else:
        raise ValueError("the specified channel_name was not found.")

    return channel_id


def save_conversations_history(client, channel_id, file_name_prefix=""):
    """Save the conversations specified by the channel ID to files.

    Parameters
    ----------
    client: slack.web.client.WebClient
        slack client object.
    channel_id : str
        channel ID of channel-like conversations.
    file_name_prefix : str
        Prefix given to the output file name.

    """
    resp = client.conversations_history(channel=channel_id)

    for i, _ in enumerate(resp):
        file_name = f"{file_name_prefix}{i:08}.json"

        with open(file_name, mode="w") as f:
            print(json.dumps(resp.data, ensure_ascii=False), file=f)


def save_users_list(client, file_name_prefix=""):
    """Save the users list of the workspace to files.

    Parameters
    ----------
    client: slack.web.client.WebClient
        slack client object.
    file_name_prefix : str
        Prefix given to the output file name.

    """
    resp = client.users_list()

    for i, _ in enumerate(resp):
        file_name = f"{file_name_prefix}userslist_{i:08}.json"

        with open(file_name, mode="w") as f:
            print(json.dumps(resp.data, ensure_ascii=False), file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--channel-name",
                        help="channel name of public channel or private channel. "
                        "`--channel-name` or `--channel-id` is required.")
    parser.add_argument("-i", "--channel-id",
                        help="channel ID of channel-like conversations. "
                        "`--channel-name` or `--channel-id` is required. "
                        "The channel ID can be viewed from the URL displayed in the web browser. "
                        "(e.g. https://app.slack.com/client/<team-id>/<channel-id>/details/)")
    parser.add_argument("-p", "--prefix", default="", help="output file name prefix.")
    parser.add_argument("-u", "--with-users-list", action='store_true', help="enable to output users list as well.")

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

    if args.channel_name:
        channel_id = get_channel_id(client, args.channel_name)
    elif args.channel_id:
        channel_id = args.channel_id
    else:
        raise ValueError("`--channel-name` or `--channel-id` is required. ")

    save_conversations_history(client, channel_id, args.prefix)

    if args.with_users_list:
        save_users_list(client, args.prefix)
