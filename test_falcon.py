import falcon
from project_atom_app.logs import LOGGING
from gunicorn.glogging import Logger

#api_logger = Logger()


class Resource(object):
    def on_post(self, req, resp):
        if req.content_length in (None, 0):
            #api_logger.info('Request failed <400>:\t' + 'no content')
            return
        body = req.stream.read()
        print(body.decode('utf-8').split('"')[-2])
        Logger.info('Request <200>')

    '''
    def load_config(self):
        """Load configuration into Gunicorn."""
        self.cfg.set('logger_class', ApiLogger)
    '''

app = falcon.API()
resource = Resource()
app.add_route('/', resource)


'''
from gunicorn.app.base import BaseApplication


class Application(BaseApplication):
    def load(self):
        return app()
if __name__ == '__main__':
    options = {
       'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': 2,
    }
    #Application(options=settings.get('gunicorn', {})).run()
    #Application(options=options).run()
'''