import ipaddress
from typing import Any

import httpx
import pendulum

from airflow.decorators import dag, task
from airflow.models import BaseOperator
from airflow.operators.bash import BashOperator


class GetRequestOperator(BaseOperator):
    template_fields = ("url",)

    def __init__(self, *, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def execute(self, context):
        return httpx.get(self.url).json()


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def example_dag_decorator(url: str = "https://httpbingo.org/get"):
    get_ip = GetRequestOperator(task_id="get_ip", url=url)

    @task(multiple_outputs=True)
    def prepare_command(raw_json: dict[str, Any]) -> dict[str, str]:
        external_ip = raw_json.get("origin", "")
        # lấy IP đầu tiên nếu có dạng "a, b"
        external_ip = external_ip.split(",")[0].strip()

        ipaddress.ip_address(external_ip)  # sẽ raise nếu không hợp lệ
        return {
            "command": f"echo 'Seems like today your server executing Airflow is connected from IP {external_ip}'",
        }

    command_info = prepare_command(get_ip.output)

    BashOperator(task_id="echo_ip_info", bash_command=command_info["command"])


example_dag = example_dag_decorator()