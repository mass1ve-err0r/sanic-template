# -*- Blueprint setup -*-
from sanic import Blueprint, response

LandingBP = Blueprint('LandingBP')


# -*- Routes -*-
@LandingBP.route('/', methods=['GET'])
async def index(request):
    template = request.app.ctx.J2Env.get_template('/pages/Index.jinja2')
    page = await template.render_async(title="Homepage")
    return response.html(page)
