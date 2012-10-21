import dimmer
import flask
import json
import scroller

def flask_app(dim, scroll):
  app = flask.Flask(__name__)

  def color_definitions():
    try:
      with open('color-defs.json', 'r') as f:
        return json.load(f)
    except (IOError, ValueError):
      return {}

  def write_color_definitions(defs):
    with open('color-defs.json', 'w') as f:
      json.dump(defs, f)

  def add_color_definition(name):
    defs = color_definitions()
    defs[name] = dim.level
    write_color_definitions(defs)

  def del_color_definition(name):
    defs = color_definitions()
    if name in defs:
      del defs[name]
      write_color_definitions(defs)

  def color_names():
    return sorted(name for name in color_definitions().iterkeys())

  @app.route('/scroll')
  def scroll_message():
    scroll.write(flask.request.args['message'])
    return flask.redirect('/')

  @app.route('/')
  def main():
    if 'red' in flask.request.args:
      level = lambda x: float(flask.request.args[x])
      dim.set_level(level('red'), level('green'), level('blue'))
      return flask.redirect('/')

    elif 'name' in flask.request.args:
      if 'name' in flask.request.args:
        add_color_definition(flask.request.args['name'])
      return flask.redirect('/')

    elif 'load' in flask.request.args:
      defs = color_definitions()
      preset = flask.request.args['load']
      if preset in defs:
        r, g, b = defs[flask.request.args['load']]
        dim.set_level(r, g, b)
      return flask.redirect('/')

    elif 'del' in flask.request.args:
      del_color_definition(flask.request.args['del'])
      return flask.redirect('/')
      
    r, g, b = dim.level
    return flask.render_template('main.html',
        red=r, green=g, blue=b,
        red_byte=int(256*r), green_byte=int(256*g), blue_byte=int(256*b),
        color_defs=color_names()
        )

  return app

if __name__ == '__main__':
  from gevent.wsgi import WSGIServer
  import sys

  if len(sys.argv) < 2:
    d = dimmer.dimmer(None)
  else:
    d = dimmer.dimmer(sys.argv[1])

  if len(sys.argv) < 3:
    s = scroller.scroller(None)
  else:
    s = scroller.scroller(sys.argv[2])

  app = flask_app(d, s)
  if len(sys.argv) > 3 and sys.argv[3] == 'debug':
    app.run(debug=True)
  else:
    server = WSGIServer(('', 80), app)
    server.serve_forever()
