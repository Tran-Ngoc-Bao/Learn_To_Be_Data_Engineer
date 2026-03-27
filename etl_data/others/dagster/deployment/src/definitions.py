from dagster import Definitions

from .jobs.etl_job import etl_job
from .jobs.cleanup_job import cleanup_job
from .schedules.schedules import etl_schedule, cleanup_schedule

defs = Definitions(
    jobs=[etl_job, cleanup_job],
    schedules=[etl_schedule, cleanup_schedule],
)