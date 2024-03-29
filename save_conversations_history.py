#!/usr/bin/env python3
"""Tool for saving the slack channel log

This tool uses Python Slack SDK.
https://github.com/slackapi/python-slack-sdk
"""

import argparse
import copy
import json
import os

from slack_sdk.http_retry.builtin_handlers import RateLimitErrorRetryHandler
from slack_sdk.web import WebClient


def get_team_info(client):
    """Get team information

    Parameters
    ----------
    client : slack_sdk.web.client.WebClient
        slack client object.

    Returns
    -------
    team_info : dict
        team information

    """
    if "_info" not in dir(get_team_info):
        resp = client.team_info()

        get_team_info._info = resp.data["team"]

    return get_team_info._info


def save_team_info(client, file_name_prefix=""):
    """Save the team information to files.

    Parameters
    ----------
    client: slack_sdk.web.client.WebClient
        slack client object.
    file_name_prefix : str
        Prefix given to the output file name.

    """
    team_info = get_team_info(client)
    team_domain = team_info["domain"]
    os.makedirs(team_domain, exist_ok=True)
    file_name = "team_info.json"
    file_path = os.path.join(team_domain, file_name)
    with open(file_path, mode="w") as f:
        print(json.dumps(team_info, ensure_ascii=False), file=f)


def get_conversations_list(client):
    """Get conversations_list.

    Parameters
    ----------
    client : slack_sdk.web.client.WebClient
        slack client object.

    Returns
    -------
    conversations_list : dict
        conversations_list

    """
    if "_list" not in dir(get_conversations_list):
        resp = client.conversations_list(types="public_channel,private_channel,mpim,im")

        _list = []
        for _ in resp:
            _list.extend(copy.copy(resp.data["channels"]))

        get_conversations_list._list = _list

    return get_conversations_list._list


def save_conversations_list(client, file_name_prefix=""):
    """Save the users list of the workspace to files.

    Parameters
    ----------
    client: slack_sdk.web.client.WebClient
        slack client object.
    file_name_prefix : str
        Prefix given to the output file name.

    """
    team_domain = get_team_info(client)["domain"]
    os.makedirs(team_domain, exist_ok=True)

    file_name = "conversations_list.json"
    file_path = os.path.join(team_domain, file_name)
    with open(file_path, mode="w") as f:
        print(json.dumps(get_conversations_list(client), ensure_ascii=False), file=f)


def get_channel_id(client, channel_name):
    """Get the channel ID from the channel name.

    Parameters
    ----------
    client : slack_sdk.web.client.WebClient
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
    # [NOTE] Conversations other than public_channel and private_channel do not have a "name" key.
    for c in get_conversations_list(client):
        if c.get("name") == channel_name:
            channel_id = c["id"]
            break
    else:
        raise ValueError("the specified channel_name was not found.")

    return channel_id


def get_conversation_name(client, conversation_id):
    """Get the name of the conversation.

    This function returns the name of the conversation partner
    if the specified conversation type is im,
    otherwise the name of the conversation.

    Parameters
    ----------
    client : slack_sdk.web.client.WebClient
        slack client object.
    conversation_id : str
        conversation ID.

    Returns
    -------
    conversation_name : str
        the name of the conversation.

    Raises
    ------
    ValueError
        occur if the specified channel is not found.

    """
    for c in get_conversations_list(client):
        if c.get("id") == conversation_id:
            if c.get("is_im"):
                for u in get_users_list(client):
                    if u["id"] == c["user"]:
                        conversation_name = u["name"]
                        break
                else:
                    raise ValueError("The user corresponding to the specified im-type conversation ID could not be found.")
            else:
                conversation_name = c["name"]

            break
    else:
        raise ValueError("The specified conversation was not found.")

    return conversation_name


def save_conversations_history(client, channel_id, file_name_prefix=""):
    """Save the conversations specified by the channel ID to files.

    Parameters
    ----------
    client: slack_sdk.web.client.WebClient
        slack client object.
    channel_id : str
        channel ID of channel-like conversations.
    file_name_prefix : str
        Prefix given to the output file name.

    """
    team_domain = get_team_info(client)["domain"]
    conversation_name = get_conversation_name(client, channel_id)
    dir_path = os.path.join(team_domain, conversation_name)
    os.makedirs(dir_path, exist_ok=True)

    resp = client.conversations_history(channel=channel_id)

    for i, _ in enumerate(resp):
        file_name = f"{file_name_prefix}{i:08}.json"
        file_path = os.path.join(dir_path, file_name)

        with open(file_path, mode="w") as f:
            print(json.dumps(resp.data, ensure_ascii=False), file=f)


def get_users_list(client):
    """Get users list.

    Parameters
    ----------
    client : slack_sdk.web.client.WebClient
        slack client object.

    Returns
    -------
    conversations_list : dict
        users list

    """
    if "_list" not in dir(get_users_list):
        resp = client.users_list()

        _list = []
        for _ in resp:
            _list.extend(copy.copy(resp.data["members"]))

        get_users_list._list = _list

    return get_users_list._list


def save_users_list(client, file_name_prefix=""):
    """Save the users list of the workspace to files.

    Parameters
    ----------
    client: slack_sdk.web.client.WebClient
        slack client object.
    file_name_prefix : str
        Prefix given to the output file name.

    """
    team_info = get_team_info(client)
    team_domain = team_info["domain"]
    os.makedirs(team_domain, exist_ok=True)
    file_name = "users_list.json"
    file_path = os.path.join(team_domain, file_name)
    with open(file_path, mode="w") as f:
        print(json.dumps(get_users_list(client), ensure_ascii=False), file=f)


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
    parser.add_argument("-c", "--with-conversations-list", action='store_true', help="enable to output conversations list as well.")
    parser.add_argument("-t", "--with-team-info", action='store_true', help="enable to output team info as well.")

    args = parser.parse_args()

    try:
        token = os.environ["SLACK_API_TOKEN"]
    except KeyError:
        print("The environment variable `SLACK_API_TOKEN` was not found. "
              "Set your Slack API token to the enviroment variable `SLACK_API_TOKEN` "
              "before running this tool by executing the following :\n"
              "    $ read -sp 'Input your Slack API token: ' SLACK_API_TOKEN; echo && export SLACK_API_TOKEN")
        exit(1)

    client = WebClient(token=os.environ["SLACK_API_TOKEN"])
    rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=1)
    client.retry_handlers.append(rate_limit_handler)

    if args.channel_name:
        channel_id = get_channel_id(client, args.channel_name)
    elif args.channel_id:
        channel_id = args.channel_id
    else:
        raise ValueError("`--channel-name` or `--channel-id` is required. ")

    save_conversations_history(client, channel_id, args.prefix)

    if args.with_users_list:
        save_users_list(client, args.prefix)

    if args.with_conversations_list:
        save_conversations_list(client, args.prefix)

    if args.with_team_info:
        save_team_info(client, args.prefix)
