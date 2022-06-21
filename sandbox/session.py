# this houses the Session class. has methods to support various session functionalities
import os
import json
import shutil
import random

import pandas as pd
from typing import List

from sandbox.outbound_dialler import OutboundDiallerClient, END_STATUS, COMPLETED_STATUS
from sandbox.utils import LogExceptions, load_yaml, save_yaml


## cols
CALLS_FIELDS = ["index", "data", "call_task_uuid", "call_status", "call_data"]

## data storage
TASKS_DIR = os.path.join("data", "tasks")
USERS_DIR = os.path.join("data", "users")


skit_client = OutboundDiallerClient()

class Session(metaclass=LogExceptions):
	""" Instantiates a Session object to handle data flow within Home and Messages interactions."""

	def __init__(self, user_id: str):

		self._info = None
		self._tasks_df = None
		self._calls_df = None
		self._current_task = None

		self._tasks_dir = TASKS_DIR
		self._user_dir = os.path.join(USERS_DIR, user_id)

		if not os.path.exists(self._user_dir):
			os.makedirs(self._user_dir)

	####
	## Methods for Home tab

	def load_session(self, session_name):
		file_path = os.path.join(self._user_dir, session_name, "session_info.yaml")
		self._info = load_yaml(file_path)
		self.__load_old_data(session_name)

	def parse_info(self, **kwargs):

		self.__clear_session_info()

		self._info = {
			"session_name": kwargs["session_name"],
			"campaign_uuid": kwargs["campaign_uuid"],
			"caller_number": kwargs["caller_number"],
		}

		self.__log_session_info()

	def load_data(self, task_name):
		self.__clear_data()

		self.__load_old_data(self._info["session_name"])
		if self._tasks_df is None:
			self.__load_new_data(task_name)
			self.__save_session_data()

	def delete(self):
		self.__delete_session_dir()
		self.__clear_session_info()
		self.__clear_data()


	def get_stats(self, tasks_df=None, calls_df=None):

		if tasks_df is None:
			tasks_df = self._tasks_df
		if calls_df is None:
			calls_df = self._calls_df

		if (tasks_df is not None) and (calls_df is not None):
			calls_df = self.__check_all_status(calls_df)
			return {
				"Completed": len(calls_df[calls_df["call_status"] == END_STATUS]),
				"In Progress": len(calls_df[calls_df["call_status"] != END_STATUS]),
				"Remaining": len(tasks_df),
			}
		else:
			return {}


	def get_new_task(self):
		if self._current_task is not None:
			self.__log_task(self._current_task)
			self.__save_session_data()

		self._current_task = self.__get_random_task()

	def start_call(self):

		call_task_uuid, call_placed = skit_client.create_call(campaign_uuid=self._info["campaign_uuid"],
		                                                      caller_number=self._info["caller_number"],
		                                                      metadata=self._current_task["data"])
		if call_placed:
			self._current_task["call_task_uuid"] = call_task_uuid

		return call_placed


	def get_call_status(self):
		call_data, call_status = skit_client.retrieve_call(self._current_task["call_task_uuid"])
		self._current_task["call_data"] = json.dumps(call_data)
		self._current_task["call_status"] = call_status

	def delete_current_call(self):
		self._current_task = {key: self._current_task[key] for key in ["index", "data"]}

	####
	## Internal methods. Mostly handles data flows

	def __log_session_info(self):
		# go to directory
		dir_path = os.path.join(self._user_dir, self._info["session_name"])
		if not os.path.isdir(dir_path):
			os.makedirs(dir_path)

		# load or save session_info
		file_path = os.path.join(dir_path, "session_info.yaml")
		if os.path.exists(file_path):
			self._info = load_yaml(file_path)
		else:
			save_yaml(self._info, file_path)


	def __save_session_data(self):
		# go to directory
		dir_path = os.path.join(self._user_dir, self._info["session_name"])

		# save session_data
		self._tasks_df.to_csv(os.path.join(dir_path, "tasks.csv"), index=False)
		self._calls_df.to_csv(os.path.join(dir_path, "calls.csv"), index=False)

	def __load_new_data(self, tasks_name):
		file_path = os.path.join(self._tasks_dir, f"{tasks_name}.csv")
		if os.path.exists(file_path):
			self._tasks_df = pd.read_csv(file_path)
			self._calls_df = pd.DataFrame(columns=CALLS_FIELDS)

	def __load_old_data(self, session_name: str):
		dir_path = os.path.join(self._user_dir, session_name)
		if os.path.exists(os.path.join(dir_path, "tasks.csv")):
			self._tasks_df = pd.read_csv(os.path.join(dir_path, "tasks.csv"))
			self._calls_df = pd.read_csv(os.path.join(dir_path, "calls.csv"))


	def __log_task(self, task_data):
		if "call_task_uuid" in task_data:
			task_data["call_data"], task_data["call_status"] = skit_client.retrieve_call(task_data["call_task_uuid"])

			if task_data["call_status"] in COMPLETED_STATUS:
				self._tasks_df.drop(index=task_data["index"], inplace=True)
				self._calls_df = self._calls_df.append(task_data, ignore_index=True)


	def __get_random_task(self):
		if len(self._tasks_df) > 0:
			index = random.choice(self._tasks_df.index.to_list())
			data = self._tasks_df.loc[index].to_dict()
			return {
				"index": index,
				"data": data
			}
		else:
			return {}

	def __check_all_status(self, calls_df: pd.DataFrame):
		for index in calls_df[calls_df["call_status"] != END_STATUS].index:
			call_data, call_status = skit_client.retrieve_call(calls_df.loc[index]["call_task_uuid"])
			calls_df.loc[index, "call_data"] = json.dumps(call_data)
			calls_df.loc[index, "call_status"] = call_status
		return calls_df

	def __clear_session_info(self):
		self._info = None

	def __clear_data(self):
		self._tasks_df = None
		self._calls_df = None

	def __delete_session_dir(self):
		shutil.rmtree(os.path.join(self._user_dir, self._info["session_name"]))

	####
	## Methods for Messages tab

	def get_all_task_names(self) -> List:
		return [t.rsplit(".csv", 1)[0] for t in os.listdir(self._tasks_dir)]

	def get_task_info(self, task_name) -> List:
		return pd.read_csv(os.path.join(self._tasks_dir, f"{task_name}.csv")).columns.to_list()

	def get_all_session_names(self) -> List:
		return [name for name in os.listdir(self._user_dir) if os.path.isdir(os.path.join(self._user_dir, name))]

	def get_session_data(self, session_name):
		data_file = os.path.join(self._user_dir, f"{session_name}", "calls.csv")
		if os.path.exists(data_file):
			data = self.__check_all_status(pd.read_csv(data_file))
			data.to_csv(data_file, index=False)
			return data_file
		else:
			return -1
