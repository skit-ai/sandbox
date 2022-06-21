from typing import Dict, List
from sandbox.views.blocks import *

def get_session_info_blocks(session_name, campaign_uuid, caller_number) -> List:
	return [
		get_text(type="mrkdwn", text="*Welcome to your SandBox!*"),
		get_divider(),
		get_button(text="Pause Session", action_id="pause_session"),
		# get_button(text="Delete Session", action_id="delete_session"),
		get_divider(),
		get_text(type="plain_text", text="Session Name: {}".format(session_name)),
		get_text(type="plain_text", text="Campaign UUID: {}".format(campaign_uuid)),
		get_text(type="plain_text", text="Caller Number: {}".format(caller_number)),
	]


def get_session_home(session_name, campaign_uuid, caller_number):

	view = {
		"type": "home",
		"blocks": get_session_info_blocks(session_name, campaign_uuid, caller_number)
	}
	view["blocks"].extend(
		[
			get_divider(),
			get_button(text="Check stats for Session", action_id="session_stats"),
			get_divider(),
			get_button(text="Display (random) task!", action_id="display_task"),
		]
	)
	return view


def get_display_task_home(campaign_uuid, session_name, caller_number, task_data: Dict):

	view = get_session_home(session_name, campaign_uuid, caller_number)

	if len(task_data) > 0:
		view["blocks"].extend(
			[
				get_text(type="mrkdwn", text="{}: *{}*".format(col, value)) for col, value in task_data.items()
			]
		)
		view["blocks"].extend(
			[
				get_divider(),
				get_button(text="Start call!", action_id="start_call"),
			]
		)
	else:
		view["blocks"].extend(
			[
				get_text(type="mrkdwn", text="No more tasks!\n\nWait for a while and then download the session data.")
			]
		)

	return view


def get_session_wo_tasks_home(session_name, campaign_uuid, caller_number):

	view = {
		"type": "home",
		"blocks": get_session_info_blocks(session_name, campaign_uuid, caller_number)
	}
	view["blocks"].extend(
		[
			get_divider(),
			get_button(text="Check stats for Session", action_id="session_stats_wo_tasks"),
			get_divider(),
			get_button(text="Start call!", action_id="start_call_wo_tasks"),
		]
	)
	return view
