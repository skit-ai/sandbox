from sandbox.views.start_home import *
from sandbox.views.session_modal import *
from sandbox.views.session_home import *
from sandbox.views.call_home import *
from sandbox.views.messages_tab import *


WITH_TASKS_VIEWS = {
	"start_home": get_start_home,
	"resume_session_modal": get_resume_session_modal,
	"rename_session_modal": get_rename_session_modal,
	"session_stats_modal": get_session_stats_modal,
	"session_info_modal": get_session_info_modal,
	"session_home": get_session_home,
	"display_task_home": get_display_task_home,
	"display_call_home": get_display_call_home,
	"display_call_status_home": get_display_call_status_home,
}

WO_TASKS_VIEWS = {
	"start_home": get_start_home,
	"session_info_wo_tasks_modal": get_session_info_wo_tasks_modal,
	"session_wo_tasks_home": get_session_wo_tasks_home,
	"wip_modal": get_wip_modal,
	# "display_task_home": get_display_task_home,
	# "display_call_home": get_display_call_home,
	# "display_call_status_home": get_display_call_status_home,
}

MESSAGES_VIEWS = {
	"help_message": get_help_message,
	"all_task_sheets_modal": get_all_task_sheets_modal,
	"task_sheet_info_modal": get_task_sheet_info_modal,
	"all_sessions_message": get_all_sessions_message,
	"admin_message": get_admin_message,
	"download_options_modal": get_download_options_modal,
}

ALL_VIEWS = {}

def return_all_views() -> Dict:
	for x in [WITH_TASKS_VIEWS, WO_TASKS_VIEWS, MESSAGES_VIEWS]:
		ALL_VIEWS.update(x)
	return ALL_VIEWS
