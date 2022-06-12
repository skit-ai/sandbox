# this houses the User class. has methods to support various user interactions
from typing import Dict
from slack_bolt import App

from sandbox.session import Session
from sandbox.utils import LogExceptions
from sandbox.views import View


## view names
START_HOME = "start_home"
SESSION_INFO_MODAL = "session_info_modal"
SESSION_STATS_MODAL = "session_stats_modal"
TASK_INFO_HOME = "task_info_home"
DISPLAY_TASK_HOME = "display_task_home"
DISPLAY_CALL_HOME = "display_call_home"
DISPLAY_CALL_STATUS_HOME = "display_call_status_home"
HELP_MESSAGE = "help_message"
ALL_TASK_SHEETS_MODAL = "all_task_sheets_modal"
TASK_SHEET_INFO_MODAL = "task_sheet_info_modal"
ALL_TASK_SESSIONS_MESSAGE = "all_task_sessions_message"


class User(metaclass=LogExceptions):
	""" Instantiates a User object to handle Slack interactions for a specific user."""

	def __init__(self, user_id: str, channel_id: str):

		self._user_id = user_id
		self._channel_id = channel_id

		self.view: View = View(user_id)
		self.session: Session = Session(user_id)


	####
	## Methods for user interactions in the Home tab

	def show_app_home(self, client: App.client, event: Dict, view_name: str = START_HOME):

		if self.view._current_view is None:
			self.post_help_message(client)
			self.view.set_current(view_name)

		self.view.publish_home(client)


	def open_session_info(self, client: App.client, body: Dict, view_name: str = SESSION_INFO_MODAL):
		self.view.set_current(view_name)
		self.view.open_modal(client, trigger_id=body["trigger_id"])


	def parse_and_show_session_info(self, client: App.client, view: Dict, view_name: str = TASK_INFO_HOME):

		## read values from modal submission
		values = view["state"]["values"]

		## session info
		session_info = {
			"session_name": values["session"]["name"]["value"],
			"campaign_uuid": values["campaign"]["uuid"]["value"],
			"caller_number": values["caller"]["number"]["value"],
		}
		self.session.parse_info(**session_info)

		## publish view
		self.view.set_current(view_name, **self.session._info)
		self.view.publish_home(client)

		## tasks name
		task_name = values["task"]["sheet"]["value"]
		self.session.load_data(task_name)


	def delete_session(self, client: App.client, body: Dict, view_name: str = START_HOME):

		self.session.delete()

		self.view.set_current(view_name)
		self.view.publish_home(client)


	def open_session_stats(self, client: App.client, body: Dict, view_name: str = SESSION_STATS_MODAL):

		session_stats = self.session.get_stats()

		if len(session_stats) > 0:
			self.view.set_current(view_name, session_stats=session_stats)
			self.view.open_modal(client, trigger_id=body["trigger_id"])


	def show_new_task(self, client: App.client, body: Dict, view_name: str = DISPLAY_TASK_HOME):

		self.session.get_new_task()

		self.view.set_current(view_name, task_data=self.session._current_task["data"], **self.session._info)
		self.view.publish_home(client)


	def show_start_call(self, client: App.client, body: Dict, view_name: str = DISPLAY_CALL_HOME):

		call_placed = self.session.start_call()

		self.view.set_current(view_name, task_data=self.session._current_task["data"], call_placed=call_placed,
		                      **self.session._info)
		self.view.publish_home(client)


	def show_call_status(self, client: App.client, body: Dict, view_name: str = DISPLAY_CALL_STATUS_HOME):

		self.session.get_call_status()

		self.view.set_current(view_name, task_data=self.session._current_task["data"],
		                      call_status=self.session._current_task["call_status"], **self.session._info)
		self.view.publish_home(client)


	def delete_current_call(self, client: App.client, body: Dict, view_name: str = DISPLAY_TASK_HOME):

		self.session.delete_current_call()

		self.view.set_current(view_name, task_data=self.session._current_task["data"], **self.session._info)
		self.view.publish_home(client)


	####
	## Methods for user interactions in the Messages tab

	def post_help_message(self, client: App.client, view_name: str = HELP_MESSAGE):
		view = View.get_view(view_name, user_id=self._user_id)
		self.view.post_message(client, channel_id=self._channel_id, text="Something went wrong", view=view)


	def show_all_tasks(self, client: App.client, body: Dict, view_name: str = ALL_TASK_SHEETS_MODAL):

		task_names_list = self.session.get_all_task_names()

		self.view.set_current(view_name, task_sheet_list=task_names_list)
		self.view.open_modal(client, trigger_id=body["trigger_id"])


	def show_task_info(self, client: App.client, body: Dict, view_name: str = TASK_SHEET_INFO_MODAL):

		task_name = body["actions"][0]["value"]
		task_fields = self.session.get_task_info(task_name)

		view_values = body["view"]
		view = View.get_view(view_name, previous_view=self.view.get_previous(), task_fields=task_fields)
		self.view.update_modal(client, view_id=view_values["id"], hash=view_values["hash"], view=view)


	def show_all_session_names(self, client: App.client, body: Dict, view_name: str = ALL_TASK_SESSIONS_MESSAGE):

		session_names_list = self.session.get_all_session_names()

		view = View.get_view(view_name, task_session_list=session_names_list)
		self.view.post_message(client, channel_id=self._channel_id, text="Something went wrong", view=view)


	def download_session_data(self, client: App.client, body: Dict):

		session_name = body["actions"][0]["value"]
		data_file = self.session.get_session_data(session_name)

		if data_file == -1:
			self.view.post_message(client, channel_id=self._channel_id,  text="No data present", view=-1)
		else:
			self.view.upload_file(client, channel_id=self._channel_id,
			                      initial_comment="Here's your download of created calls :smile:", file=data_file,
			                      title=f"{session_name}.created_calls.csv")


	####
	## Class methods

	@classmethod
	def get_user(cls, users_dict: Dict, user_id: str, channel_id: str = None):
		if user_id not in users_dict:
			users_dict[user_id] = cls(user_id, channel_id)
		return users_dict.get(user_id)
