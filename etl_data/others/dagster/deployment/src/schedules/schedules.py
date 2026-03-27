from dagster import ScheduleDefinition
from ..jobs.etl_job import etl_job
from ..jobs.cleanup_job import cleanup_job

etl_schedule = ScheduleDefinition(job=etl_job, cron_schedule="*/2 * * * *")      # mỗi 2 phút
cleanup_schedule = ScheduleDefinition(job=cleanup_job, cron_schedule="*/5 * * * *")  # mỗi 5 phút