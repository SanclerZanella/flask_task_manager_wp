import os
from flask import Flask
if os.path.exists('env.py'):
    import env

# Instance of Flask
app = Flask(__name__)


# Route decorator for the main route
@app.route("/")
def hello():
    return "Hello World... again!"


# Define host and port for the app
# Tell the app how and where to run
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
