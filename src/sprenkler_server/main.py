from flask import Flask, render_template, request, abort

from config import ControllerConfig

app = Flask(__name__)
app.config["config_file"] = "config.json"

def load_config() -> ControllerConfig:
    with open(app.config["config_file"], "r") as f:
        data = f.read().replace('\n', '')
        return ControllerConfig.from_json(data)

def save_config(config: ControllerConfig) -> None:
    json = config.to_json()
    with open(app.config["config_file"], "w") as f:
        f.write(json)

@app.route("/")
def index():
    config = load_config()
    return render_template("main.jinja2")


@app.route("/valve/<valve_id>", methods=["GET", "PUT"])
def hello(valve_id):
    config = load_config()
    valve_config = None
    for valve_config in config.valves:
        if valve_config.id == valve_id:
            break

    if valve_config is None:
        abort(400, 'Record not found')
    if request.method == "GET":
        config = valve_config
        return render_template("detail.jinja2", config=config)
    if request.method == "PUT":
        changes = request.get_json()




