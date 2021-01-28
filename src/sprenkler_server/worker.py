import calendar
from datetime import time, timedelta, datetime

import requests
from config import ControllerConfig, ValveConfig, ValveStatus, TimeSlice


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_valve_status(self, valve: ValveConfig) -> ValveStatus:
        r = requests.get(f"{self.base_url}/valve/{valve.id}")
        r.raise_for_status()
        return r.text

    def set_valve_status(self, valve: ValveConfig, status: ValveStatus) -> None:
        r = requests.put(f"{self.base_url}/valve/{valve.id}", data=status)
        r.raise_for_status()

    def get_current_uptime(self) -> int:
        r = requests.get(f"{self.base_url}/")
        r.raise_for_status()
        data = r.json()
        return data["uptime"]


class Worker:
    def __init__(self, base_url: str):
        self.client = Client(base_url)

    def update_client(self, config: ControllerConfig) -> None:
        for valve in config.valves:
            if valve.get_valve_status(datetime.now()) == "open":
                self.client.set_valve_status(valve, "open")
            else:
                self.client.set_valve_status(valve, "closed")


def main():
    # w = Worker("http://0.0.0.0:8081")
    v = ValveConfig(
        index=0,
        schedule={
            calendar.MONDAY: [TimeSlice(time(hour=17), timedelta(hours=1, minutes=30))]
        },
    )
    config = ControllerConfig(valves=[v])
    # w.update_client(config)
    json = config.to_json()
    with open("config.json", "w") as f:
        f.write(json)
    with open("config.json", "r") as f:
        data = f.read().replace('\n', '')
        config2 = ControllerConfig.from_json(data)

    print(repr(config2))


if __name__ == "__main__":
    main()
