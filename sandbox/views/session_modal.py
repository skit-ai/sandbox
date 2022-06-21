from typing import Dict
from sandbox.views.blocks import *

def get_wip_modal():
	view = {
		"type": "modal",
		"callback_id": "session_info_wo_tasks_modal",
		"title": {
			"type": "plain_text",
			"text": "WIP"
		},
		"blocks": [
			get_text(type="plain_text", text="This feature is under development")
		]
	}
	return view

def get_session_info_wo_tasks_modal():

	view = {
		"type": "modal",
		"callback_id": "session_info_wo_tasks_modal",
		"title": {
			"type": "plain_text",
			"text": "New Session info"
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit"
		},
		"blocks": [
			get_input_block(block_id="session", action_id="name", placeholder="Unique identifier", label="Session Name"),
			get_input_block(block_id="campaign", action_id="uuid", placeholder="Find this in the Campaign Manager", label="Campaign UUID"),
			get_input_block(block_id="caller", action_id="number", placeholder="Number to call at", label="Caller Number"),
		]
	}
	return view

def get_session_info_with_tasks_modal():

	view = get_session_info_wo_tasks_modal()
	view["callback_id"] = "session_info_with_tasks_modal"
	view["blocks"].extend(
		[
			get_input_block(block_id="task", action_id="name", placeholder="Name of the Task Sheet csv", label="Task Sheet"),
		]
	)
	return view

def get_resume_session_modal():

	view = {
		"type": "modal",
		"callback_id": "resume_session_modal",
		"title": {
			"type": "plain_text",
			"text": "Resume Session info"
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit"
		},
		"blocks": [
			get_input_block(block_id="session", action_id="name", placeholder="Use the same Name as before", label="Session Name"),
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
		"blocks": [
			get_text(type="mrkdwn", text="{}: *{}*".format(col, value)) for col, value in session_stats.items()
		]
	}
	return view
