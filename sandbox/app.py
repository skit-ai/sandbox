import os
from typing import Dict
from slack_bolt import App

from sandbox.user import UserSession

# Manages different UserSession objects for different users
user_sessions: Dict[str, UserSession] = {}

# Initializes your app with your bot token and signing secret
app = App(
	token=os.environ.get("SLACK_BOT_TOKEN"),
	signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

####
## Home tab

# User opens App Home tab
@app.event("app_home_opened")
def app_home_opened(client, event, logger):
	try:
		session = UserSession.get_user(user_sessions, event["user"], event["channel"])
		session.show_app_home(client, event)

	except Exception as e:
		logger.error(f"Error publishing home tab: {e}")

# User wants to start a new task session
@app.action("new_session_info")
def new_session_info(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.view_session_info(app.client, body)
	logger.info(body)

# User submits modal with session info
@app.view("session_info_modal")
def handle_submission(ack, body, client, view, logger):
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.parse_and_show_session_info(client, view)
	ack()
	session.load_task_session_data()
	logger.info(body)

# User wants to delete task session
@app.action("delete_session_info")
def delete_session_info(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.delete_session_info(app.client, body)
	logger.info(body)

# User wants to check stats for the session
@app.action("session_stats")
def check_session_stats(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.view_session_stats(app.client, body)
	logger.info(body)

# User wants to see a random task
@app.action("display_task")
def display_task(ack, body, logger):
	try:
		ack()
		session = UserSession.get_user(user_sessions, body["user"]["id"])
		session.show_random_task(app.client, body)
		logger.info(body)

	except Exception as e:
		logger.error(f"Error displaying task: {e}")

# User wants to start a call with for the currently displayed task
@app.action("start_call")
def start_call(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.start_call(app.client, body)
	logger.info(body)

# User wants to check the status of last successful call
@app.action("check_call_status")
def check_call_status(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.update_call_status(app.client, body)
	logger.info(body)

# User wants to cancel the current call
@app.action("cancel_call")
def cancel_call(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.delete_current_call(app.client, body)
	logger.info(body)

####
## Messages tab

@app.message("help")
def post_help_info(message, say):
	session = UserSession.get_user(user_sessions, message["user"])
	session.post_help_message(app.client)

@app.action("list_task_sheets")
def list_all_task_sheets(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.view_all_task_sheets(app.client, body)
	logger.info(body)

@app.action("task_sheet_info")
def list_task_sheet_info(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.view_task_sheet_info(app.client, body)
	logger.info(body)

@app.action("list_task_sessions")
def list_all_task_sessions(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.post_all_task_sessions(app.client, body)
	logger.info(body)

@app.action("download_session_data")
def download_session_data(ack, body, logger):
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.upload_session_data(app.client, body)
	logger.info(body)


# Start your app
def main():
	app.start(port=int(os.environ.get("PORT", 3000)))
