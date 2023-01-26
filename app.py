from subprocess import Popen, CREATE_NEW_CONSOLE

from dash import Dash
import dash_bootstrap_components as dbc

from src.pages import pump_screener_page


app = Dash(external_stylesheets=[dbc.themes.DARKLY])
app.layout = pump_screener_page.layout


if __name__ == "__main__":
    # start background worker process
    Popen(["python", "background_task.py"], creationflags=CREATE_NEW_CONSOLE)
    app.run()
