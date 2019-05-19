import falcon
import json
import logging
from project_atom_app.database1 import *
from project_atom_app.logs import Logger
from project_atom_app.model.ml import Model

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
model = Model()


def form_response(result_list):
    result_dict = {}
    result = []
    for item in result_list:
        result_dict['title'] = item.get('title', None)
        # result_dict['description'] = item.get('description', None)
        result.append(result_dict)
        result_dict = {'title': None, 'description': None}
    return result


class Resource(object):
    def on_post(self, req, resp):
        if req.content_length in (None, 0):
            logger.info('Request failed <400>:\t' + 'no content')
            return

        content = json.loads(req.stream.read().decode('utf-8'))
        if 'text' not in content:
            resp.status = falcon.HTTP_400
            return
        elif type(content['text']) is not str:
            resp.status = falcon.HTTP_400
            return

        category, suggests = model.wish_handler(content['text'])
        print(suggests)
        suggests = [str(i) for i in suggests]
        if category is 'hh':
            category_id, category_name = model.predict_text(content['text'])
            resp.body = str(category_name) + str(form_response(get_list_vacancy(suggests)))
        elif category is 'youla':
            resp.body = str(form_response(get_list_youla(suggests)))
        else:
            resp.body = str('dummy query: no result')

        print(resp.body)
        logger.info('Request <200>')


app = falcon.API()
resource = Resource()
app.add_route('/', resource)
