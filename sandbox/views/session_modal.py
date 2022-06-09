from typing import Dict

def get_session_info_modal():

	view = {
		"type": "modal",
		"callback_id": "session_info_modal",
		"title": {
			"type": "plain_text",
			"text": "Task Session info"
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit"
		},
		"blocks": [
			{
				"type": "input",
				"block_id": "session",
				"element": {
					"type": "plain_text_input",
					"action_id": "name",
					"placeholder": {
						"type": "plain_text",
						"text": "Unique identifier"
					}
				},
				"label": {
					"type": "plain_text",
					"text": "Session Name"
				}
			},
			{
				"type": "input",
				"block_id": "campaign",
				"element": {
					"type": "plain_text_input",
					"action_id": "uuid",
					"placeholder": {
						"type": "plain_text",
						"text": "Find this in the Outbound Dialler"
					}
				},
				"label": {
					"type": "plain_text",
					"text": "Campaign UUID"
				}
			},
			{
				"type": "input",
				"block_id": "task",
				"element": {
					"type": "plain_text_input",
					"action_id": "sheet",
					"placeholder": {
						"type": "plain_text",
						"text": "Name of the Task Sheet csv"
					}
				},
				"label": {
					"type": "plain_text",
					"text": "Task Sheet"
				}
			},
			{
				"type": "input",
				"block_id": "caller",
				"element": {
					"type": "plain_text_input",
					"action_id": "number",
					"placeholder": {
						"type": "plain_text",
						"text": "Number to call at"
					}
				},
				"label": {
					"type": "plain_text",
					"text": "Caller number"
				}
			}
		]
	}
	return view

def get_session_stats_modal(session_stats: Dict):

	view = {
		"type": "modal",
		"callback_id": "session_stats_modal",
		"title": {
			"type": "plain_text",
			"text": "Task Session stats"
		},
		"blocks": []
	}

	for col, value in session_stats.items():
		view["blocks"].append(
			{
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": f"{col}: *{value}*"
				}
			}
		)

	return view
