import diskcache
from dash import Dash
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager

from src.layout import layout
from src.callbacks import register_callbacks


cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(external_stylesheets=[dbc.themes.DARKLY, dbc_css], long_callback_manager=long_callback_manager)

app.layout = layout
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)
