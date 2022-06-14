def get_divider():
	return {
		"type": "divider"
	}

def get_text(type: str, text: str):
	return {
		"type": "section",
		"text": {
			"type": type,
			"text": text
		}
	}

def get_button(text: str, action_id: str):
	return {
		"type": "actions",
		"elements": [
			{
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": text
				},
				"action_id": action_id
			}
		]
	}

def get_button_with_text(text: str, button_text: str, action_id: str, value: str = " "):
	return {
		"type": "section",
		"text": {
			"type": "mrkdwn",
			"text": text
		},
		"accessory": {
			"type": "button",
			"text": {
				"type": "plain_text",
				"text": button_text,
				"emoji": True
			},
			"value": value,
			"action_id": action_id
		}
	}

def get_input_block(block_id: str, action_id: str, placeholder: str, label: str):
	return {
		"type": "input",
		"block_id": block_id,
		"element": {
			"type": "plain_text_input",
			"action_id": action_id,
			"placeholder": {
				"type": "plain_text",
				"text": placeholder
			}
		},
		"label": {
			"type": "plain_text",
			"text": label
		}
	}