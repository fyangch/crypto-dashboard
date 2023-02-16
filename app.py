import diskcache
from dash import Dash
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager

from src.components import pump_screener
from src.layout import layout
from src.callbacks import register_callbacks


cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

app = Dash(external_stylesheets=[dbc.themes.DARKLY], long_callback_manager=long_callback_manager)
app.layout = layout
register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)
