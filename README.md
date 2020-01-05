# save_slack_conversations_history
Tool for saving the slack channel(conversations) log to local files.

## Prerequisite
Set your Slack API token to the enviroment variable `SLACK_API_TOKEN` before running this tool by executing the following :  

```shell
$ read -sp 'Input your Slack API token: ' SLACK_API_TOKEN; echo && export SLACK_API_TOKEN
```

## Usage
```sh
$ ./save_slack_conversations_history.py -h
usage: save_slack_conversations_history.py [-h] [-n CHANNEL_NAME]
                                           [-i CHANNEL_ID] [-p PREFIX] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -n CHANNEL_NAME, --channel-name CHANNEL_NAME
                        channel name of public channel or private channel.
                        `--channel-name` or `--channel-id` is required.
  -i CHANNEL_ID, --channel-id CHANNEL_ID
                        channel ID of channel-like conversations. `--channel-
                        name` or `--channel-id` is required. The channel ID
                        can be viewed from the URL displayed in the web
                        browser. (e.g. https://app.slack.com/client/<team-
                        id>/<channel-id>/details/)
  -p PREFIX, --prefix PREFIX
                        output file name prefix.
  -u, --with-users-list
                        enable to output users list as well.
```

## Example
```sh
$ read -sp 'Input your Slack API token: ' SLACK_API_TOKEN; echo && export SLACK_API_TOKEN
Input your Slack API token:
$ ./save_slack_conversations_history.py -n general
```
