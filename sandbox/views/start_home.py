def get_start_home():

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
				"type": "section",
				"text": {
					"type": "mrkdwn",
					"text": "Here, you can connect to an Outbound Dialler campaign, and generate a pre-tagged dataset. But first.."
				}
			},
			{
				"type": "actions",
				"elements": [
					{
						"type": "button",
						"text": {
							"type": "plain_text",
							"text": "Create Session!"
						},
						"action_id": "new_session_info"
					}
				]
			}
		]
	}
	return view