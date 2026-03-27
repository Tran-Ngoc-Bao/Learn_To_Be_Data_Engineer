from dagster import job, op

@op
def cleanup():
    print("cleanup done")

@job
def cleanup_job():
    cleanup()