# this houses the BotSession class. has methods to support various session functionalities
import os
import shutil
import random

import pandas as pd
from typing import Dict
from slack_bolt import App

from sandbox.outbound_dialler import OutboundDiallerClient
from sandbox.utils import LogExceptions, load_yaml, save_yaml
from sandbox.views import get_view

## views
START_HOME = "start_home"
SESSION_INFO_MODAL = "session_info_modal"
SESSION_STATS_MODAL = "session_stats_modal"
TASK_INFO_HOME = "task_info_home"
DISPLAY_TASK_HOME = "display_task_home"
DISPLAY_CALL_HOME = "display_call_home"
DISPLAY_CALL_STATUS_HOME = "display_call_status_home"

## cols
CREATED_CALLS_COLUMNS = ["index", "data", "call_task_uuid", "call_status", "call_data"]

skit_client = OutboundDiallerClient()

class UserSession(metaclass=LogExceptions):
	""" Instantiates a UserSession object to handle Slack interactions for a particular user."""

	def __init__(self, user_id):
		self._user_id = str(user_id)
		self._view = None
		self._session_info = None
		self._task_sheet_df = None
		self._created_calls_df = None
		self._current_task = None

	####
	## Main methods. Used directly by app

	def load_app_home(self, client: App.client, event: Dict, view_name: str = START_HOME):
		if not self._view:
			self._view = get_view(view_name)
		# views.publish is the method that your app uses to push a view to the Home tab
		client.views_publish(
			# the user that opened your app's app home
			user_id=self._user_id,
			# the view object that appears in the app home
			view=self._view
		)

	def load_session_info_modal(self, client: App.client, body: Dict, view_name: str = SESSION_INFO_MODAL):
		# Call views_open with the built-in client
		client.views_open(
			# Pass a valid trigger_id within 3 seconds of receiving it
			trigger_id=body["trigger_id"],
			# View payload
			view=get_view(view_name)
		)

	def parse_session_info_modal(self, client: App.client, view: Dict, view_name: str = TASK_INFO_HOME):

		self.__reset_session_info()

		# Parse values from the modal inputs
		values = view["state"]["values"]
		self._session_info = {
			"session_name": values["session"]["name"]["value"],
			"campaign_uuid": values["campaign"]["uuid"]["value"],
			"task_sheet": values["task"]["sheet"]["value"],
			"caller_number": values["caller"]["number"]["value"],
		}

		self.__log_session_info()

		self._view = get_view(view_name, session_name=self._session_info["session_name"],
		                      campaign_uuid=self._session_info["campaign_uuid"],
		                      caller_number=self._session_info["caller_number"])
		# views.publish is the method that your app uses to push a view to the Home tab
		client.views_publish(
			# the user that opened your app's app home
			user_id=self._user_id,
			# the view object that appears in the app home
			view=self._view
		)

	def load_task_session_data(self):

		self.__reset_session_data()

		self.__load_old_task_sheets()
		if self._task_sheet_df is None:
			self.__load_new_task_sheets()

	def delete_session_info(self, client: App.client, body: Dict, view_name: str = START_HOME):

		self.__delete_session()

		self.__reset_session_info()
		self.__reset_session_data()

		# Call views_open with the built-in client
		self._view = get_view(view_name)
		# views.publish is the method that your app uses to push a view to the Home tab
		client.views_publish(
			# the user that opened your app's app home
			user_id=self._user_id,
			# the view object that appears in the app home
			view=self._view
		)

	def load_session_stats_modal(self, client: App.client, body: Dict, view_name: str = SESSION_STATS_MODAL):
		if self._task_sheet_df is not None:

			for index in self._created_calls_df[self._created_calls_df["call_status"] != "SUCCESS"].index:
				self._created_calls_df.loc[index]["call_data"], self._created_calls_df.loc[index][
					"call_status"] = skit_client.retrieve_call(self._created_calls_df.loc[index]["call_task_uuid"])

			session_stats = self.__check_stats()

			# Call views_open with the built-in client
			client.views_open(
				# Pass a valid trigger_id within 3 seconds of receiving it
				trigger_id=body["trigger_id"],
				# View payload
				view=get_view(view_name, session_stats=session_stats)
			)

	def display_random_task(self, client: App.client, view_name: str = DISPLAY_TASK_HOME):

		if self._current_task is not None:
			self.__save_task(self._current_task)
		self.__load_random_task()

		self.__save_task_session_data()

		self._view = get_view(view_name, session_name=self._session_info["session_name"],
		                      campaign_uuid=self._session_info["campaign_uuid"],
		                      caller_number=self._session_info["caller_number"],
		                      task_data=self._current_task["data"])
		# views.publish is the method that your app uses to push a view to the Home tab
		client.views_publish(
			# the user that opened your app's app home
			user_id=self._user_id,
			# the view object that appears in the app home
			view=self._view
		)

	def start_call(self, client: App.client, view_name: str = DISPLAY_CALL_HOME):

		call_task_uuid, call_placed = skit_client.create_call(campaign_uuid=self._session_info["campaign_uuid"],
		                                                      caller_number=self._session_info["caller_number"],
		                                                      metadata=self._current_task["data"])
		if call_placed:
			self._current_task["call_task_uuid"] = call_task_uuid

		self._view = get_view(view_name, session_name=self._session_info["session_name"],
		                      campaign_uuid=self._session_info["campaign_uuid"],
		                      caller_number=self._session_info["caller_number"],
		                      task_data=self._current_task["data"],
		                      call_placed=call_placed)
		# views.publish is the method that your app uses to push a view to the Home tab
		client.views_publish(
			# the user that opened your app's app home
			user_id=self._user_id,
			# the view object that appears in the app home
			view=self._view
		)

	def update_call_status(self, client: App.client, view_name: str = DISPLAY_CALL_STATUS_HOME):

		self._current_task["call_data"], self._current_task["call_status"] = skit_client.retrieve_call(
			self._current_task["call_task_uuid"])

		self._view = get_view(view_name, session_name=self._session_info["session_name"],
		                      campaign_uuid=self._session_info["campaign_uuid"],
		                      caller_number=self._session_info["caller_number"],
		                      task_data=self._current_task["data"],
		                      call_status=self._current_task["call_status"])
		# views.publish is the method that your app uses to push a view to the Home tab
		client.views_publish(
			# the user that opened your app's app home
			user_id=self._user_id,
			# the view object that appears in the app home
			view=self._view
		)

	def cancel_call(self, client: App.client, view_name: str = DISPLAY_TASK_HOME):

		self._current_task = {key: val for key, val in self._current_task.items() if key in ["index", "data"]}

		self._view = get_view(view_name, session_name=self._session_info["session_name"],
		                      campaign_uuid=self._session_info["campaign_uuid"],
		                      caller_number=self._session_info["caller_number"],
		                      task_data=self._current_task["data"])
		# views.publish is the method that your app uses to push a view to the Home tab
		client.views_publish(
			# the user that opened your app's app home
			user_id=self._user_id,
			# the view object that appears in the app home
			view=self._view
		)

	####
	## Class methods

	@classmethod
	def get_user(cls, sessions: Dict, user_id: str):
		if user_id not in sessions:
			sessions[user_id] = cls(user_id)
		return sessions.get(user_id)

	####
	## Internal methods. Mostly handles data flows

	def __log_session_info(self):
		# go to directory
		dir_path = os.path.join("data", "users", self._user_id, self._session_info["session_name"])
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)

		# load or save session_info
		file_path = os.path.join(dir_path, "session_info.yaml")
		if os.path.exists(file_path):
			self._session_info = load_yaml(file_path)
		else:
			save_yaml(self._session_info, file_path)

	def __save_task_session_data(self):
		# go to directory
		dir_path = os.path.join("data", "users", self._user_id, self._session_info["session_name"])

		# save session_data
		self._task_sheet_df.to_csv(os.path.join(dir_path, "task_sheet.csv"), index=False)
		self._created_calls_df.to_csv(os.path.join(dir_path, "created_calls.csv"), index=False)

	def __load_new_task_sheets(self):
		file_path = os.path.join("data", "tasks", "{}.csv".format(self._session_info["task_sheet"]))
		if os.path.exists(file_path):
			self._task_sheet_df = pd.read_csv(file_path)
			self._created_calls_df = pd.DataFrame(columns=CREATED_CALLS_COLUMNS)

	def __load_old_task_sheets(self):
		dir_path = os.path.join("data", "users", self._user_id, self._session_info["session_name"])
		if os.path.exists(os.path.join(dir_path, "task_sheet.csv")):
			self._task_sheet_df = pd.read_csv(os.path.join(dir_path, "task_sheet.csv"))
			self._created_calls_df = pd.read_csv(os.path.join(dir_path, "created_calls.csv"))


	def __save_task(self, task_data):
		if "call_task_uuid" in task_data:
			task_data["call_data"], task_data["call_status"] = skit_client.retrieve_call(task_data["call_task_uuid"])

			if task_data["call_status"] in ["SUCCESS", "NOT ENDED"]:
				self._task_sheet_df.drop(index=task_data["index"], inplace=True)
				self._created_calls_df = self._created_calls_df.append(task_data, ignore_index=True)

	def __load_random_task(self):
		self._current_task = {}
		self._current_task["index"] = idx = random.choice(self._task_sheet_df.index.to_list())
		self._current_task["data"] = self._task_sheet_df.loc[idx].to_dict()

	def __check_call_status(self):
		call_data, call_status = skit_client.retrieve_call(self._current_task["call_task_uuid"])
		self._current_task["call_data"] = call_data
		self._current_task["call_status"] = call_status

	def __check_stats(self):
		return {
			"Completed": len(self._created_calls_df[self._created_calls_df["call_status"] == "SUCCESS"]),
			"In Progress":len(self._created_calls_df[self._created_calls_df["call_status"] != "SUCCESS"]),
			"Remaining": len(self._task_sheet_df),
		}

	def __reset_session_info(self):
		self._session_info = None

	def __reset_session_data(self):
		self._task_sheet_df = None
		self._created_calls_df = None

	def __delete_session(self):
		shutil.rmtree(os.path.join("data", "users", self._user_id, self._session_info["session_name"]))
