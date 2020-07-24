#!/usr/bin/env python
import re
import os
import datetime
import tempfile

title = input("What did you learn today?")
today = datetime.date.today()


tmp_path = tempfile.mktemp(suffix=".md")
os.system(f"gedit {tmp_path}")

filepath = (
    f"app/markdown/"
    f"{str(today.year).zfill(4)}-{str(today.month).zfill(2)}-{str(today.day).zfill(2)}/"
    f"til-{re.sub(r'[^a-zA-Z0-9]+', '-', title).lower()}.md"
)
os.makedirs(os.path.dirname(filepath), exist_ok=True)
with open(
    filepath,
    mode="w"
) as f:
    with open(tmp_path, "r") as f2:
        data = f2.read()
        if not data:
            exit(0)
        f.write(data)

os.system("git diff")
print("If this looks good run git add app/markdown/ and ./deploy.sh")

"""
# TIL: How to get the HTTP status code from a Flask errorhandler exception

When you're using Flasks [`errorhandler`](https://flask.palletsprojects.com/en/1.1.x/api/#flask.Flask.errorhandler) decorator for a specific HTTP status code it's clear what HTTP
status code the response will be:

```python
from flask import Flask

app = Flask(__name__)

@app.errorhandler(404)
def on_not_found(error):
    return "This is a 404 for sure!", 404
```

However I didn't know how to write an error handler that handles
all HTTP status calls, `abort(XYZ)` calls, and just general
exceptions being raised from the stack. This is what I ended up with:

```python
from flask import Flask

app = Flask(__name__)

@app.errorhandler(Exception)
def on_error(error):
    return "This is an error!", ...?
```

but I wasn't sure how to get the status code from the `HTTPException` that
Flask was going to raise (another thing to note is that `HTTPException` is
from `werkzeug`, not from Flask). I tried `status_code` and `status`, to no avail
and then ran `dir()` on the error which revealed `code` as the property to use.
This was my final function without a ton of guards since it's for a quick project:

```python
from flask import Flask

app = Flask(__name__)

@app.errorhandler(Exception)
def on_error(error):
    # Errors raised from places besides abort() or routing failures
    # will have a status code of 500 for internal error.
    status_code = getattr(error, "code", 500)
    return f"HTTP Error {status_code}", status_code
```
"""