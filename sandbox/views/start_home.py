from sandbox.views.blocks import *

def get_start_home(session_exists: bool):

	view = {
		"type": "home",
		"blocks": [
			get_text(
				type="mrkdwn", text="*Welcome to your Sandbox!* \n\nHere, you can connect to an existing Outbound Dialler campaign, and generate a pre-tagged dataset."),
			get_divider(),
			get_text(type="mrkdwn", text="You can begin, one of two ways:"),
			get_button(text="I have a Task Sheet!", action_id="new_session_with_tasks"),
			get_button(text="I dont have a Task Sheet!", action_id="new_session_wo_tasks"),
		]
	}

	if session_exists:
		view["blocks"].extend(
			[
				get_divider(),
				get_button_with_text(text="Looks like you have an existing session..", button_text="Resume Session", action_id="resume_session"),
			]
		)

	return view