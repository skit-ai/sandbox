from typing import Dict

def get_task_info_home(session_name, campaign_uuid, caller_number):

	view = {
		"type": "home",
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*Welcome to your SandBox!*"
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "New Session ?"
						},
						"action_id": "new_session_info"
					}
				]
			},
			{
				"type": "divider"
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Delete this Session!"
						},
						"action_id": "delete_session_info"
					}
				]
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"Session Name: {session_name}",
					"emoji": True
				}
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"Campaign UUID: {campaign_uuid}",
					"emoji": True
				}
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"Caller Number: {caller_number}",
					"emoji": True
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Display (random) task!"
						},
						"action_id": "display_task"
					}
				]
			},
		]
	}

	return view

def get_display_task_home(campaign_uuid, session_name, caller_number, task_data: Dict):

	view = {
		"type": "home",
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "*Welcome to your SandBox!*"
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "New Session ?"
						},
						"action_id": "new_session_info"
					}
				]
			},
			{
				"type": "divider"
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Delete this Session!"
						},
						"action_id": "delete_session_info"
					}
				]
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"Session Name: {session_name}",
					"emoji": True
				}
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"Campaign UUID: {campaign_uuid}",
					"emoji": True
				}
			},
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": f"Caller Number: {caller_number}",
					"emoji": True
				}
			},
			{
				"type": "divider"
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Check stats for Session"
						},
						"action_id": "session_stats"
					}
				]
			},
			{
				"type": "divider"
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Display (random) task!"
						},
						"action_id": "display_task"
					}
				]
			},
		]
	}

	for col, value in task_data.items():
		view["blocks"].append(
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"{col}: *{value}*"
				}
			}
		)

	view["blocks"] += [
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Start call!"
					},
					"action_id": "start_call"
				}
			]
		},
	]

	return view