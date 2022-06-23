from typing import List, Dict
from sandbox.views.blocks import *

def get_options_blocks():
	return [
		get_divider(),
		get_button_with_text(text="List all available Task Sheets.", button_text="Click Me", action_id="list_task_sheets"),
		get_divider(),
		get_button_with_text(text="List my existing Sessions.", button_text="Click Me", action_id="list_sessions"),
	]

def get_admin_message():

	blocks = [
		get_button_with_text(text="Options for download", button_text="Click Me", action_id="download_options"),
	]
	return blocks

def get_download_options_modal():
	view = {
		"type": "modal",
		"callback_id": "download_options_modal",
		"title": {
			"type": "plain_text",
			"text": "Download Options"
		},
		"submit": {
			"type": "plain_text",
			"text": "Submit"
		},
		"blocks": [
			get_input_block(block_id="session", action_id="name", placeholder="Download all data from sessions of this name",
			                label="Session Name"),
		]
	}
	return view

def get_help_message(user_id):

	blocks = [
		get_text(type="mrkdwn", text="Hi there, <@{}>!\n\nTry one of the following:".format(user_id)),
	]
	blocks.extend(get_options_blocks())
	return blocks


def get_all_task_sheets_modal(task_sheet_list: List):

	view = {
		"type": "modal",
		"callback_id": "session_stats_modal",
		"title": {
			"type": "plain_text",
			"text": "Task Sheet names"
		},
		"blocks": []
	}
	for task_sheet_name in task_sheet_list:
		view["blocks"].extend(
			[
				get_divider(),
				get_button_with_text(text="{}".format(task_sheet_name), button_text="Show info",
				                     value="{}".format(task_sheet_name), action_id="task_sheet_info"),
			]
		)
	return view


def get_task_sheet_info_modal(previous_view: Dict, task_fields: List):

	view = previous_view.copy()
	view["blocks"] = [get_text(type="mrkdwn", text="*[ {} ]*".format(", ".join(task_fields)))]
	view["blocks"].extend(previous_view["blocks"])
	return view


def get_all_sessions_message(task_session_list: List):

	blocks = []
	for session_name in task_session_list:
		blocks.extend(
			[
				get_divider(),
				get_button_with_text(text="{}".format(session_name), button_text="Download data",
				                     value="{}".format(session_name), action_id="download_session_data"),
			]
		)
	return blocks
