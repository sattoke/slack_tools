# slack_tools
This is a variety of tools for slack.

## Prerequisite
Set your Slack API token to the enviroment variable `SLACK_API_TOKEN` before running this tool by executing the following :  

```shell
$ read -sp 'Input your Slack API token: ' SLACK_API_TOKEN; echo && export SLACK_API_TOKEN
```

## save_conversations_history
Tool for saving the slack channel(conversations) log to local files.

### Usage
```sh
$ ./save_conversations_history.py -h
usage: save_conversations_history.py [-h] [-n CHANNEL_NAME] [-i CHANNEL_ID]
                                     [-p PREFIX] [-u]

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

### Example
```sh
$ ./save_conversations_history.py -n general
```

## list_files
Tool for listing the uploaded files

### Usage
```sh
$ ./list_files.py -h
usage: list_files.py [-h] [-r] [-u USER_ID]

optional arguments:
  -h, --help            show this help message and exit
  -r, --raw-output      Output a raw slack API response.
  -u USER_ID, --user-id USER_ID
                        Filter files created by a single user.
```

### Example
```sh
$ ./list_files.py
```

## delete_files
Tool for deliting the uploaded files

### Usage
```sh
$ ./delete_files.py -h
usage: delete_files.py [-h] [-l LIST_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -l LIST_FILE, --list-file LIST_FILE
                        list of file IDs to be deleted. The default value is
                        '-'. If it is '-', the list is read from the standard
                        input.This list assumes a space-separated format with
                        the ID of the file uploaded to slack in the first
                        column. This format follows the output of `list-
                        files.py`. The tool assumes that the user edits the
                        output of `list-files.py` with an editor, etc., and
                        then inputs it into `delete-files.py`.
```

### Example
```sh
$ cat file_list.tsv | ./delete_files.py
```
