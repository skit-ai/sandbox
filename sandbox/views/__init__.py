from typing import Dict, Union
from slack_bolt import App

from sandbox.utils import LogExceptions

from sandbox.views.start_home import *
from sandbox.views.session_modal import *
from sandbox.views.task_home import *
from sandbox.views.call_home import *
from sandbox.views.messages_tab import *


VIEWS = {
	"start_home": get_start_home,
	"session_info_modal": get_session_info_modal,
	"session_stats_modal": get_session_stats_modal,
	"task_info_home": get_task_info_home,
	"display_task_home": get_display_task_home,
	"display_call_home": get_display_call_home,
	"display_call_status_home": get_display_call_status_home,
	"help_message": get_help_message,
	"all_task_sheets_modal": get_all_task_sheets_modal,
	"task_sheet_info_modal": get_task_sheet_info_modal,
	"all_task_sessions_message": get_all_task_sessions_message,
}


class View(metaclass=LogExceptions):
	""" Instantiates a View object to handle interactive views shown to the user."""

	def __init__(self, user_id: str):

		self._user_id = user_id

		self._previous_view: Dict = None
		self._current_view: Dict = None


	def publish_home(self, client: App.client, view: Dict = None):
		client.views_publish(
			user_id=self._user_id,
			view=self.__check(view)
		)
		self.__rollover()

	def open_modal(self, client: App.client, trigger_id: str, view: Dict = None):
		client.views_open(
			trigger_id=trigger_id,
			view=self.__check(view)
		)
		self.__rollover()

	def update_modal(self, client: App.client, view_id: str, hash: str, view: Dict = None):
		client.views_update(
			view_id=view_id,
			hash=hash,
			view=self.__check(view)
		)
		self.__rollover()

	def post_message(self, client: App.client, channel_id: str, text: str, view: Union[Dict, int]):
		if view == -1:
			client.chat_postMessage(
				channel=channel_id,
				text=text
			)
		else:
			client.chat_postMessage(
				channel=channel_id,
				blocks=self.__check(view),
				text=text
			)

	def upload_file(self, client: App.client, channel_id: str, initial_comment: str, file: str, title: str):
		client.files_upload(
			channels=channel_id,
			initial_comment=initial_comment,
			file=file,
			title=title
		)


	def set_current(self, view_name: str, **kwargs):
		self._current_view = self.get_view(view_name, **kwargs)

	def get_previous(self):
		return self._previous_view

	def __rollover(self):
		self._previous_view = self._current_view.copy()

	def __check(self, view: Dict = None):
		if view is None:
			view = self._current_view
		return view


	@staticmethod
	def get_view(view_name: str, view_dict=None, **kwargs):
		if view_dict is None:
			view_dict = VIEWS
		return view_dict.get(view_name)(**kwargs)