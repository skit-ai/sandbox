from typing import Dict
from sandbox.views.blocks import *
from sandbox.views.session_home import get_session_with_tasks_home

def get_task_data_blocks(task_data: Dict):
	blocks = [get_divider()]
	blocks.extend(
		[
			get_text(type="mrkdwn", text="{}: *{}*".format(col, value)) for col, value in task_data.items()
		]
	)
	return blocks

def get_check_status_blocks():
	return [
		get_divider(),
		get_text(type="plain_text", text="Call in progress.."),
		get_button(text="Check call status!", action_id="check_call_status"),
	]


def get_display_call_home(campaign_uuid, session_name, caller_number, task_data: Dict, call_placed: bool):

	view = get_session_with_tasks_home(session_name, campaign_uuid, caller_number)
	view["blocks"].extend(get_task_data_blocks(task_data))

	if call_placed:
		call_blocks = get_check_status_blocks()

	else:
		call_blocks = [
			get_divider(),
			get_text(type="plain_text", text="Call failed"),
			get_button(text="Call again!", action_id="start_call_with_tasks"),
			get_button(text="Choose a different task!", action_id="display_task"),
		]
	view["blocks"].extend(call_blocks)

	return view


def get_display_call_status_home(campaign_uuid, session_name, caller_number, task_data: Dict, call_status):

	view = get_session_with_tasks_home(session_name, campaign_uuid, caller_number)
	view["blocks"].extend(get_task_data_blocks(task_data))

	view["blocks"].extend(get_check_status_blocks())
	view["blocks"].extend(
		[
			get_text(type="plain_text", text="{}".format(call_status)),
			get_button(text="Cancel this call", action_id="cancel_call"),
			get_divider(),
			get_button(text="Choose next task!", action_id="display_task"),
		]
	)
	return view