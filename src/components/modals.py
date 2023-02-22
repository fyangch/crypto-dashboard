from dash import dcc
import dash_bootstrap_components as dbc


modal_args = {
    "is_open": False,
    "centered": True,
    "size": "lg"
}

trend_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Uptrend Screener")),
        dbc.ModalBody(dcc.Markdown("""
            - hmm
            - ok
            - cool
        """)),
    ],
    id="trend_modal",
    **modal_args,
)

pump_modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Pump Screener")),
        dbc.ModalBody(dcc.Markdown("""
            - pumpedy pump
        """)),
    ],
    id="pump_modal",
    **modal_args,
)
