import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PLOTS:
    def brent_ok_candle(brent, station_ok, adjust):
        """candlestick graph for the brent prices

        Input:
            brent: pd.DataFrame
                contains the ytd data for brent crude oil
            ok_station: pd.DataFrame
                contains ok tank station prices ytd
            adjust: str
                set if we want to adjust the brent numbers to DKK and per liter

        Raise
            None

        Output
            fig: plotlu.graph_objects
                plot showing brent candle and line for ok station prices

        """

        fig = make_subplots(specs = [[{'secondary_y': True}]])

        if not adjust:

            fig.add_trace(
                    go.Candlestick(
                        x = brent['Datetime'],
                        open = brent['Open'],
                        high = brent['High'],
                        low = brent['Low'],
                        close = brent['Close']
                        )
                    )
        else:
            fig.add_trace(
                    go.Candlestick(
                        x = brent['Datetime'],
                        open = brent['Open_adj'],
                        high = brent['High_adj'],
                        low = brent['Low_adj'],
                        close = brent['Close_adj']
                        )
                    )
        
        fig.add_trace(
            go.Scatter(
                x = station_ok['Dato'],
                y = station_ok['Pris'],
                mode = 'lines',
                name = 'Station Prices'
            ),
                secondary_y = True
        )

        fig.update_layout(template = 'plotly_dark')

        return fig

    def brent_ok_fig(brent, station_ok, adjust):
        """brent crude and ok station prices

        Input:
            brent_d: pd.Dataframe
                brent crude oil prices (See data.brent_adj.py)
            station_ok: pd.Dataframe
                ok oil station prices (see data.ok_data.py)
            adjust: str
                set if we want to adjust the brent numbers to DKK and per liter

        Raise
            None

        Output:
            fig: plotly.graph_objects go figure

        --------------------------------------

        TODO
            [] show Close or Close_dkk_l
        """
        fig = make_subplots(specs = [[{'secondary_y': True}]])

        if not adjust:

            fig.add_trace(
                go.Scatter(
                    x = brent['Datetime'],
                    y = brent['Close'],
                    mode = 'lines',
                    name = 'Brent Index'
                ),
                    secondary_y = False
            )

        else:

            fig.add_trace(
                go.Scatter(
                    x = brent['Datetime'],
                    y = brent['Close_adj'],
                    mode = 'lines',
                    name = 'Brent Index'
                ),
                    secondary_y = False
            )

        fig.add_trace(
            go.Scatter(
                x = station_ok['Dato'],
                y = station_ok['Pris'],
                mode = 'lines',
                name = 'Station Prices'
            ),
                secondary_y = True
        )

        fig.update_layout(template = 'plotly_dark')

        return fig
