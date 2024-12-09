# hl7Adapter
## Installation

Set up python virtual environment:

```
python -m venv env
```

Activate virtual environment env:

```
# Windows
.\env\Scripts\Activate.ps1
```

To install it by the following command:

```
# If you don't want to make changes to current code later
pip install .

# if you want to make changes and test results quickly
pip install -e .
```

To run it:

```
# Windows
python .\flask\app.py
```

The above command will open up a browser window at `127.0.0.1:5000` (You can configure this in "flask/app.py"). Press CTRL+C to quit the app.

You can also choose to use development server (werkzeug) or production server (waitress). Just comment out either one of the lines in "flask/app.py".

```python
# app.run(host=host, port=port) # use dev server
serve(app, host=host, port=port) # use prod server
```



## Package
To package all files to one executable, [pyinstaller](https://github.com/pyinstaller/pyinstaller) is used in this project. Be sure to read [this](https://pyinstaller.org/en/stable/operating-mode.html) to understand the limitation of pyinstaller.
To package it:


```
# dev server
pyinstaller --onefile --hidden-import werkzeug --add-data ".\flask\templates:templates" --add-data "hl7:hl7" flask\app.py

# prod server
pyinstaller --onefile --hidden-import waitress --add-data ".\flask\templates:templates" --add-data "hl7:hl7" .\flask\app.py
```