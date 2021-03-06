# this houses the User class. has methods to support various user interactions
import os.path
from typing import Dict
from slack_bolt import App

from sandbox.views import View
from sandbox.session import Session
from sandbox.utils import LogExceptions, load_yaml
from sandbox.constants import *


class User(metaclass=LogExceptions):
	""" Instantiates a User object to handle Slack interactions for a specific user."""

	def __init__(self, user_id: str):

		self._user_id = user_id

		self.view: View = View(user_id)
		self.session: Session = Session(user_id)


	####
	# Methods for user interactions in the Home tab

	def show_app_home(self, client: App.client, event: Dict):

		if self.view.get_home() is None:
			self.post_help_message(client, event["channel"])
			self.show_start_home(client, event)
		else:
			self.view.publish_home(client)


	def open_resume_session(self, client: App.client, body: Dict, view_name: str = "resume_session_modal"):
		self.__open_simple_modal(client, body, view_name)


	def open_session_info(self, client: App.client, body: Dict, view_name: str = "session_info_modal"):
		self.__open_simple_modal(client, body, view_name)


	def show_session_info(self, client: App.client, view: Dict, view_name: str = "session_home"):

		## read values from modal submission
		values = view["state"]["values"]
		self.__parse_session_info(values)

		## publish view
		self.view.set_home(view_name, **self.session._info)
		self.view.publish_home(client)

		## tasks name
		task_name = values["task"]["name"]["value"]
		self.session.load_data(task_name)


	def parse_and_resume_session(self, client: App.client, view: Dict, view_name: str = "session_home"):

		## read values from modal submission
		values = view["state"]["values"]

		## session info
		session_name = values["session"]["name"]["value"]
		self.session.load_session(session_name)

		## publish view
		self.view.set_home(view_name, **self.session._info)
		self.view.publish_home(client)


	def open_rename_session(self, client: App.client, body: Dict, view_name: str = "rename_session_modal"):
		self.__open_simple_modal(client, body, view_name)


	def parse_new_session_name(self, client: App.client, view: Dict, view_name: str = "session_home"):

		## read values from modal submission
		values = view["state"]["values"]

		## session info
		session_name = values["session"]["name"]["value"]
		self.session.update_info(session_name)

		## publish view
		self.view.set_home(view_name, **self.session._info)
		self.view.publish_home(client)


	def delete_session(self, client: App.client, body: Dict):
		self.session.delete()
		self.show_start_home(client, body)


	def open_session_stats(self, client: App.client, body: Dict, view_name: str = "session_stats_modal"):

		self.session.check_stats()

		if len(self.session._stats) > 0:
			view = View.get_view(view_name, session_stats=self.session._stats, created_calls_count=self.session._created_calls_count)
			self.view.open_modal(client, trigger_id=body["trigger_id"], view=view)

		self.session.get_all_calls_status()


	def show_updated_session_stats(self, client: App.client, body: Dict, view_name: str = "session_stats_modal"):

		self.session.check_stats()

		if len(self.session._stats) > 0:
			view_values = body["view"]
			view = View.get_view(view_name, session_stats=self.session._stats, created_calls_count=self.session._created_calls_count)
			self.view.update_modal(client, view_id=view_values["id"], hash=view_values["hash"], view=view)

		self.session.get_all_calls_status()


	def show_new_task(self, client: App.client, body: Dict, view_name: str = "display_task_home"):

		self.session.get_new_task()

		if len(self.session._current_task)>0:
			task_data = self.session._current_task["data"]
		else:
			task_data = {}

		self.view.set_home(view_name, task_data=task_data, **self.session._info)
		self.view.publish_home(client)


	def show_start_call(self, client: App.client, body: Dict, view_name: str = "display_call_home"):

		call_placed = self.session.start_call()

		self.view.set_home(view_name, task_data=self.session._current_task["data"], call_placed=call_placed,
		                   **self.session._info)
		self.view.publish_home(client)


	def show_call_status(self, client: App.client, body: Dict, view_name: str = "display_call_status_home"):

		self.session.get_call_status()

		self.view.set_home(view_name, task_data=self.session._current_task["data"],
		                   call_status=self.session._current_task["call_status"], **self.session._info)
		self.view.publish_home(client)


	def delete_current_call(self, client: App.client, body: Dict, view_name: str = "display_task_home"):

		self.session.delete_current_call()

		self.view.set_home(view_name, task_data=self.session._current_task["data"], **self.session._info)
		self.view.publish_home(client)


	##
	# Under development

	def open_session_info_wo_tasks(self, client: App.client, body: Dict, view_name: str = "wip_modal"):
		self.__open_simple_modal(client, body, view_name)


	def show_session_info_wo_tasks(self, client: App.client, view: Dict, view_name: str = "session_wo_tasks_home"):

		## read values from modal submission
		values = view["state"]["values"]
		self.__parse_session_info(values)

		## publish view
		self.view.set_home(view_name, **self.session._info)
		self.view.publish_home(client)


	####
	# Methods for user interactions in the Messages tab

	def post_help_message(self, client: App.client, channel_id: str, view_name: str = "help_message"):
		blocks = View.get_view(view_name, user_id=self._user_id)
		self.view.post_message(client, channel_id=channel_id, text="Something went wrong", blocks=blocks)


	def show_all_tasks(self, client: App.client, body: Dict, view_name: str = "all_task_sheets_modal"):

		task_names_list = self.session.get_all_task_names()

		view = View.get_view(view_name, task_sheet_list=task_names_list)
		self.view.open_modal(client, trigger_id=body["trigger_id"], view=view)
		self.view.set_previous(view)


	def show_task_info(self, client: App.client, body: Dict, view_name: str = "task_sheet_info_modal"):

		task_name = body["actions"][0]["value"]
		task_fields = self.session.get_task_info(task_name)

		view_values = body["view"]
		view = View.get_view(view_name, previous_view=self.view.get_previous(), task_fields=task_fields)
		self.view.update_modal(client, view_id=view_values["id"], hash=view_values["hash"], view=view)


	def show_all_session_names(self, client: App.client, body: Dict, view_name: str = "all_sessions_message"):

		session_names_list = self.session.get_all_session_names()

		blocks = View.get_view(view_name, task_session_list=session_names_list)
		self.view.post_message(client, channel_id=body["channel"]["id"], text="Something went wrong", blocks=blocks)


	def download_session_data(self, client: App.client, body: Dict):

		session_name = body["actions"][0]["value"]
		data_file = self.session.get_session_data(session_name)

		if data_file == -1:
			self.view.post_message(client, channel_id=body["channel"]["id"],  text="No data present", blocks=-1)
		else:
			self.view.upload_file(client, channel_id=body["channel"]["id"],
			                      initial_comment="Here's your download of created calls :smile:", file=data_file,
			                      title=f"{session_name}.created_calls.csv")


	def show_start_home(self, client: App.client, event: Dict):
		view_name = "start_home"
		self.view.set_home(view_name=view_name, session_exists=(len(self.session.get_all_session_names()) > 0))
		self.view.publish_home(client)

	##
	# Admin interactions

	def post_admin_message(self, client: App.client, channel_id: str, view_name: str = "admin_message"):

		admin_users = load_yaml(ADMIN_YAML)

		if self._user_id in admin_users:
			blocks = View.get_view(view_name)
			self.view.post_message(client, channel_id=channel_id, text="Something went wrong", blocks=blocks)
		else:
			self.view.post_message(client, channel_id=channel_id,
			                       text="Sorry, this option is only available to admins.", blocks=-1)


	def show_download_options(self, client: App.client, body: Dict, view_name: str = "download_options_modal"):
		self._channel_id = body["channel"]["id"]
		self.__open_simple_modal(client, body, view_name)


	def download_all_session_data(self, client: App.client, view: Dict):

		## read values from modal submission
		values = view["state"]["values"]
		session_name = values["session"]["name"]["value"]

		## get all sessions with given name. across all users
		data_files = []
		for user in os.listdir(USERS_DIR):
			user_dir = os.path.join(USERS_DIR, user)
			if os.path.isdir(user_dir):
				if session_name in self.session.get_all_session_names(user_dir):
					file = self.session.get_session_data(session_name, user_dir)
					if file != -1:
						data_files.append(file)

		## upload to messages tab and delete temp data file
		all_data_file = self.session.merge_session_data(data_files)
		self.view.upload_file(client, channel_id=self._channel_id,
		                      initial_comment="Here's your download :smile:", file=all_data_file,
		                      title=f"{session_name}.created_calls.csv")
		os.remove(all_data_file)


	def __open_simple_modal(self, client: App.client, body: Dict, view_name: str):
		view = View.get_view(view_name)
		self.view.open_modal(client, trigger_id=body["trigger_id"], view=view)


	def __parse_session_info(self, values: Dict):
		## session info
		session_info = {
			"session_name": values["session"]["name"]["value"],
			"campaign_uuid": values["campaign"]["uuid"]["value"],
			"caller_number": values["caller"]["number"]["value"],
		}
		self.session.parse_info(**session_info)


	####
	# Class methods

	@classmethod
	def get_user(cls, users_dict: Dict, user_id: str):
		if user_id not in users_dict:
			users_dict[user_id] = cls(user_id)
		return users_dict.get(user_id)
