from typing import Dict

def get_display_call_home(campaign_uuid, session_name, caller_number, task_data: Dict, call_placed: bool):

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
			}
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

	view["blocks"].append(
		{
			"type": "divider"
		}
	)

	if call_placed:
		call_blocks = [
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": "Call in progress..",
					"emoji": True
				}
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Check call status!"
						},
						"action_id": "check_call_status"
					}
				]
			},
		]

	else:
		call_blocks = [
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": "Call failed",
					"emoji": True
				}
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Call again!"
						},
						"action_id": "start_call"
					}
				]
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Choose a different task!"
						},
						"action_id": "display_task"
					}
				]
			},
		]

	view["blocks"] += call_blocks

	return view


def get_display_call_status_home(campaign_uuid, session_name, caller_number, task_data: Dict, call_status):

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
			}
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

	view["blocks"].append(
		{
			"type": "divider"
		}
	)

	view["blocks"] += [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Call in progress..",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Check call status!"
					},
					"action_id": "check_call_status"
				}
			]
		},
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": f"{call_status}",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Cancel this call"
					},
					"action_id": "cancel_call"
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
						"text": "Choose next task!"
					},
					"action_id": "display_task"
				}
			]
		},
	]

	return view