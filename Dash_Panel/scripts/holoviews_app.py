from dash import Dashboard, pn

STYLE = '''
.bk.app-body {
    background: #f2f2f2;
    color: #000000;
    font-family: roboto, sans-serif, Verdana;
}
.bk.app-bar {
    background: #d52e3f;
    border-color: white;
    box-shadow: 5px 5px 20px #9E9E9E;
    color: #ffffff;
    z-index: 50;
}
.bk.app-container {
    background: #ffffff;
    border-radius: 5px;
    box-shadow: 2px 2px 2px lightgrey;
    color: #000000;
}
.bk.app-settings {
    background: #e0e0e0;
    color: #000000;
}
'''

pn.config.raw_css.append(STYLE)

pn.extension(raw_css=[STYLE])



if __name__ == '__main__':
    dash = Dashboard()
    pn.serve(dash.panel().servable(), port=5006, allow_websocket_origin=["localhost:5000","127.0.0.1:5000"], show=False)