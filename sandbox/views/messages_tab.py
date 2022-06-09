from typing import List, Dict

option_blocks = [
	{
		"type": "divider"
	},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "List all uploaded Task Sheets."
		},
		"accessory": {
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": "Click Me",
				"emoji": True
			},
			"action_id": "list_task_sheets"
		}
	},
	{
			"type": "divider"
	},
	{
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": "List all existing Task Sessions."
		},
		"accessory": {
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": "Click Me",
				"emoji": True
			},
			"action_id": "list_task_sessions"
		}
	},
]

def get_help_message(user_id):

	blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"Hi there, <@{user_id}>!\n\nTry one of the following:"
			}
		},
	]
	blocks += option_blocks
	return blocks

def get_all_task_sheets_modal(task_sheet_list: List):

	blocks = []
	for task_sheet_name in task_sheet_list:
		blocks += [
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"{task_sheet_name}"
				},
				"accessory": {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Show info",
						"emoji": True
					},
					"value": f"{task_sheet_name}",
					"action_id": "task_sheet_info"
				}
			},
		]

	view = {
		"type": "modal",
		"callback_id": "session_stats_modal",
		"title": {
			"type": "plain_text",
			"text": "Task Sheet names"
		},
		"blocks": blocks
	}

	return view

def get_task_sheet_info_modal(previous_view: Dict, task_fields: List):

	view = previous_view.copy()

	view["blocks"] = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f'*[ {", ".join(task_fields)} ]*'
			}
		},
	] + previous_view["blocks"]

	return view

def get_all_task_sessions_message(task_session_list: List):

	blocks = []
	for session_name in task_session_list:
		blocks += [
			{
				"type": "divider"
			},
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"{session_name}"
				},
				"accessory": {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Download data",
						"emoji": True
					},
					"value": f"{session_name}",
					"action_id": "download_session_data"
				}
			},
		]

	return blocks
