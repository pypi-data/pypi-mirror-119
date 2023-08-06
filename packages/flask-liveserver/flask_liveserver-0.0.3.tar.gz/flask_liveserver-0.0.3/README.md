flask_liveserver


Quick Start
-------
```python
from flask import Flask
from liveserver import LiveServer

app = Flask(__name__)

ls = LiveServer(app)


@app.route("/")
def index():
    return ls.render_template("index.html")
    

ls.run("0.0.0.0", 8080)
```

License
-------
MIT Licence
