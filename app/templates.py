import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from starlette.templating import _TemplateResponse
from starlette.requests import Request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    autoescape=select_autoescape(),
    enable_async=False,
)


def render(name: str, request: Request, **context):
    template = _env.get_template(name)
    ctx = {"request": request, **context}
    return _TemplateResponse(template, ctx, media_type="text/html")
