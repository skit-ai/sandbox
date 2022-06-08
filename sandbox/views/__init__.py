from sandbox.views.start_home import *
from sandbox.views.session_info import *
from sandbox.views.task_home import *
from sandbox.views.call_home import *


VIEWS = {
	"start_home": get_start_home,
	"session_info_modal": get_session_info_modal,
	"session_stats_modal": get_session_stats_modal,
	"task_info_home": get_task_info_home,
	"display_task_home": get_display_task_home,
	"display_call_home": get_display_call_home,
	"display_call_status_home": get_display_call_status_home,
}


def get_view(view_name: str, **kwargs):
	return VIEWS.get(view_name)(**kwargs)