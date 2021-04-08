from dotenv import load_dotenv
load_dotenv("./.env")

from os import environ as env
from sanic import Sanic, response
from jinja2 import Environment, PackageLoader, select_autoescape

from blueprints.landing import LandingBP


# -*- Sanic Config -*-
app = Sanic(__name__)
app.static('/static', './static')
app.config.update({
    # Uncomment when you deploy with nginx
    # "PROXIES_COUNT": 1,
    # "FORWARDED_SECRET": env.get('FORWARDING_SECRET')
})


# -*- Jinja2 Setup -*-
J2Env = Environment(loader=PackageLoader('server', './templates'),
                    autoescape=select_autoescape(['html', 'xml']),
                    enable_async=True)
J2Env.globals["url_for"] = app.url_for
app.ctx.J2Env = J2Env


@app.listener('before_server_start')
async def preflight(app, loop):
    print("executed before server start")


@app.listener('after_server_stop')
async def aftermath(app, loop):
    print("executed after server halted")


# -*- Blueprint Registration -*-
app.blueprint(LandingBP)


# -*- DEBUG HEADERS, REMOVE IF YOU DO NOT NEED HOT-RELOADING -*-
@app.middleware('response')
async def debug_headers(req, res):
    res.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    res.headers['Pragma'] = "no-cache"
    res.headers['Expires'] = "0"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, workers=2, access_log=True, debug=True)
