class WSGISaveData(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        from cStringIO import StringIO
        body = environ['wsgi.input'].read(length)
        environ['req_data'] = body
        environ['wsgi.input'] = StringIO(body)

        app_iter = self.app(environ, self._sr_callback(start_response))

        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):
            start_response(status, headers, exc_info)
        return callback
