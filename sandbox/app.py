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

# User opens App Home tab
@app.event("app_home_opened")
def app_home_opened(client, event, logger):
	try:
		session = UserSession.get_user(user_sessions, event["user"])
		session.load_app_home(client, event)

	except Exception as e:
		logger.error(f"Error publishing home tab: {e}")

# User wants to start a new task session
@app.action("new_session_info")
def task_session_info(ack, body, logger):
	# Acknowledge the shortcut request
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.load_session_info_modal(app.client, body)
	logger.info(body)

# User submits modal with session info
@app.view("session_info_modal")
def handle_submission(ack, body, client, view, logger):
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.parse_session_info_modal(client, view)
	ack()
	session.load_task_session_data()

# User wants to delete task session
@app.action("delete_session_info")
def task_session_info(ack, body, logger):
	# Acknowledge the shortcut request
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.delete_session_info(app.client, body)
	logger.info(body)

# User wants to check stats for the session
@app.action("session_stats")
def check_stats(ack, body, logger):
	# Acknowledge the shortcut request
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.load_session_stats_modal(app.client, body)
	logger.info(body)

# User wants to see a random task
@app.action("display_task")
def display_task(ack, body, logger):
	# Acknowledge the shortcut request
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.display_random_task(app.client)
	logger.info(body)

# User wants to start a call with for the currently displayed task
@app.action("start_call")
def start_call(ack, body, logger):
	# Acknowledge the shortcut request
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.start_call(app.client)
	logger.info(body)

# User wants to check the status of last successful call
@app.action("check_call_status")
def check_call_status(ack, body, logger):
	# Acknowledge the shortcut request
	ack()
	session = UserSession.get_user(user_sessions, body["user"]["id"])
	session.update_call_status(app.client)
	logger.info(body)


# Start your app
def main():
	app.start(port=int(os.environ.get("PORT", 3000)))
