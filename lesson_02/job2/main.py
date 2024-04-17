import os
from flask import Flask, request
from flask import typing as flask_typing
from lesson_02.job2.job_two import save_sales_to_stg_dir


AUTH_TOKEN = os.environ.get("AUTH_TOKEN")


if not AUTH_TOKEN:
    print("AUTH_TOKEN environment variable must be set")


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    """
    Controller that accepts command via HTTP and
    trigger business logic layer

    Proposed POST body in JSON:
    {
      "raw_dir": "/path/to/my_dir/raw/sales/2022-08-09",
      "stg_dir": "/path/to/my_dir/stg/sales/2022-08-09"
    }
    """
    input_data: dict = request.json
    raw_dir = input_data.get('raw_dir')
    stg_dir = input_data.get('stg_dir')

    if not stg_dir:
        return {
            "message": "stg_dir parameter missed",
        }, 400

    save_sales_to_stg_dir(raw_dir=raw_dir, stg_dir=stg_dir)

    return {
               "message": "Data retrieved successfully from API",
           }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)