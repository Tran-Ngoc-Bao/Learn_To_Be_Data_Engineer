from dagster import job, op

@op
def extract():
    return [1, 2, 3]

@op
def transform(numbers):
    return [n * 10 for n in numbers]

@op
def load(result):
    print("Loaded:", result)

@job
def etl_job():
    load(transform(extract()))