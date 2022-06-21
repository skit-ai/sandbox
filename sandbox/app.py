import os
from typing import Dict
from slack_bolt import App

from sandbox.user import User

# Manages different User objects for different users
users_dict: Dict[str, User] = {}

# Initializes your app with your bot token and signing secret
app = App(
	token=os.environ.get("SLACK_BOT_TOKEN"),
	signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

####
# Home tab

# User opens App Home tab
@app.event("app_home_opened")
def app_home_opened(client, event, logger):
	try:
		user = User.get_user(users_dict, event["user"], event["channel"])
		user.show_app_home(client, event)

	except Exception as e:
		logger.error(f"Error publishing home tab: {e}")

# User wants to start a new session - with a task sheet
@app.action("new_session")
def new_session_action(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.open_session_info(app.client, body)
	logger.info(body)

# User submits modal with session info -
@app.view("session_info_modal")
def session_info_submission(ack, body, client, view, logger):
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_session_info(client, view)
	ack()
	logger.info(body)

# User wants to resume an existing session
@app.action("resume_session")
def resume_session_action(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.open_resume_session(app.client, body)
	logger.info(body)

# User submits resume session modal
@app.view("resume_session_modal")
def handle_submission(ack, body, client, view, logger):
	user = User.get_user(users_dict, body["user"]["id"])
	user.parse_and_resume_session(client, view)
	ack()
	logger.info(body)

# User wants to pause a current session
@app.action("pause_session")
def new_session_info(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_start_home(app.client, body)
	logger.info(body)

# User wants to delete current session
@app.action("delete_session")
def delete_session(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.delete_session(app.client, body)
	logger.info(body)

# User wants to check stats for the session
@app.action("session_stats")
def check_session_stats(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.open_session_stats(app.client, body)
	logger.info(body)

# User wants to see a random task in the current session
@app.action("display_task")
def display_task(ack, body, logger):
	try:
		ack()
		user = User.get_user(users_dict, body["user"]["id"])
		user.show_new_task(app.client, body)
		logger.info(body)

	except Exception as e:
		logger.error(f"Error displaying task: {e}")

# User wants to start a call for the currently displayed task
@app.action("start_call")
def start_call(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_start_call(app.client, body)
	logger.info(body)

# User wants to check the status of the ongoing call
@app.action("check_call_status")
def check_call_status(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_call_status(app.client, body)
	logger.info(body)

# User wants to cancel the ongoing call
@app.action("cancel_call")
def cancel_call(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.delete_current_call(app.client, body)
	logger.info(body)

##
# Under development

# User wants to start a new session - without a task sheet
@app.action("new_session_wo_tasks")
def new_session_action(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.open_session_info_wo_tasks(app.client, body)
	logger.info(body)

# User submits modal with session info
@app.view("session_info_wo_tasks_modal")
def session_info_submission(ack, body, client, view, logger):
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_session_info_wo_tasks(client, view)
	ack()
	logger.info(body)

####
# Messages tab

@app.message("help")
def post_help_info(message, say):
	user = User.get_user(users_dict, message["user"])
	user.post_help_message(app.client)

@app.action("list_task_sheets")
def list_all_task_sheets(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_all_tasks(app.client, body)
	logger.info(body)

@app.action("task_sheet_info")
def list_task_sheet_info(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_task_info(app.client, body)
	logger.info(body)

@app.action("list_task_sessions")
def list_all_task_sessions(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.show_all_session_names(app.client, body)
	logger.info(body)

@app.action("download_session_data")
def download_session_data(ack, body, logger):
	ack()
	user = User.get_user(users_dict, body["user"]["id"])
	user.download_session_data(app.client, body)
	logger.info(body)


# Start your app
def main():
	app.start(port=int(os.environ.get("PORT", 3000)))
