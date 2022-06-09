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


def get_view(view_name: str, **kwargs):
	return VIEWS.get(view_name)(**kwargs)