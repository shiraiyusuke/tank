import os
import tornado.wsgi
import tornado.ioloop
import tornado.httpserver

def start_from_terminal(app, port=5000, proc=1, debug=False):
    if os.path.dirname(__file__) == '':
        os.chdir('./')
    else:
        os.chdir(os.path.dirname(__file__))    
    if debug:
        app.run(debug=debug, host='0.0.0.0', port=port)
    else:
        start_tornado(app, port, proc)

def start_tornado(app, port, proc):
    http_server = tornado.httpserver.HTTPServer(tornado.wsgi.WSGIContainer(app))
    http_server.bind(port)
    http_server.start(proc)
    print('Tornado server starting on port {}'.format(port))
    tornado.ioloop.IOLoop.instance().start()
