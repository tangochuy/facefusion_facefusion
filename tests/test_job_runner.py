import subprocess
import shutil
import pytest
import facefusion.core

from facefusion.download import conditional_download
from facefusion.job_manager import init_jobs, clear_jobs, get_job_status
from facefusion.job_runner import run_job


@pytest.fixture(scope = 'module', autouse = True)
def before_all() -> None:
	clear_jobs('.jobs')
	init_jobs('.jobs')
	prepare_run_args()
	conditional_download('.assets/examples',
	[
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/source.jpg',
		'https://github.com/facefusion/facefusion-assets/releases/download/examples/target-240p.mp4'
	])
	subprocess.run([ 'ffmpeg', '-i', '.assets/examples/target-240p.mp4', '-vframes', '1', '.assets/examples/target-240p.jpg' ])


def prepare_run_args() -> None:
	import facefusion.globals
	facefusion.globals.execution_thread_count = 4
	facefusion.globals.execution_queue_count = 1


def copy_json(source_path : str, destination_path : str) -> None:
	shutil.copyfile(source_path, destination_path)


def test_run_job() -> None:
	copy_json('tests/providers/test_run_job.json', './.jobs/queued/test_run_job.json')
	assert run_job('test_run_job', facefusion.core.handle_step)
	assert get_job_status('test_run_job') == 'completed'


@pytest.mark.skip()
def test_run_job_merge_action() -> None:
	copy_json('tests/providers/test_run_job_merge_action.json', './.jobs/queued/test_run_job_merge_action.json')
	assert run_job('test_run_job_merge_action', facefusion.core.handle_step)
	assert get_job_status('test_run_job_merge_action') == 'completed'


def test_run_job_remix_action() -> None:
	copy_json('tests/providers/test_run_job_remix_action.json', './.jobs/queued/test_run_job_remix_action.json')
	assert run_job('test_run_job_remix_action', facefusion.core.handle_step)
	assert get_job_status('test_run_job_remix_action') == 'completed'
