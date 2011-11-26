from pyramid.config import Configurator

from cornice import Service
from cornice.schemas import *


class Checker(GetChecker):
    fields = [Integer('foo')]


service = Service(name="service", path="/service")


@service.get(validator=Checker())
def get1(request):
    res = {"test": "succeeded"}
    try:
        res['foo'] = get_converted(request, 'foo')
    except KeyError:
        pass

    return res


@service.post(validator=JsonBody())
def post1(request):
    return {"body": request.body}


def includeme(config):
    config.include("cornice")
    config.scan("cornice.tests.validationapp")


def main(global_config, **settings):
    config = Configurator(settings={})
    config.include(includeme)
    return config.make_wsgi_app()
