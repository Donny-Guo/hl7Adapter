from flask import Flask, render_template, request
from hl7.parser import parse_message
from waitress import serve
import time, webbrowser
import multiprocessing
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex()

def open_browser(url):
    time.sleep(2)
    webbrowser.open(url)

def validate_message(message):
    errors, warnings = parse_message(message)
    # print(f"errors: {errors}")
    # print(f"warnings: {warnings}")
    errors = [f"Error: {e}" for e in errors]
    warnings = [f"Warning: {warning}" for warning in warnings]
    output = errors + warnings
    if not output:
        output = ['Passed']
    return '\n'.join(output)

@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    user_input = ""
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        if user_input:
            try:
                output = validate_message(user_input)
            except Exception as e: # caught any exception when parsing the message
                output = f"Exception: {e}"
        else:
            output = ""
    return render_template("index.html", output=output, user_input=user_input)

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 5000
    url = f"http://{host}:{port}"
    multiprocessing.freeze_support()
    multiprocessing.Process(target=open_browser, args=(url,)).start()
    print(f"Running on {url}")
    print(f"Press CTRL+C to quit")
    # app.run(host=host, port=port) # use dev server
    serve(app, host=host, port=port) # use prod server
