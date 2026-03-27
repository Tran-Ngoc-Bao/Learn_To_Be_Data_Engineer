from prefect import flow, task
from datetime import datetime

@task
def hello(name: str = "Bao"):
    print(f"[{datetime.now().isoformat()}] Hello {name} from Prefect!")

@flow(name="hello-flow")
def hello_flow(name: str = "Bao"):
    hello(name)

if __name__ == "__main__":
    hello_flow()