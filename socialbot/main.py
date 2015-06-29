#!/usr/bin/python
# -*- coding: utf-8 -*-
import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from socialbot.utils import get_config

config = get_config()
MAGIC_KEYWORD = config.get('main', 'magic_keyword')


class SlackBotHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)

        try:
            postvars = cgi.parse_qs(post_body, keep_blank_values=1)
            user_name = postvars.get('user_name')[0]
            content = postvars.get('text')[0]
            raw_link = content.strip("{} <".format(MAGIC_KEYWORD)).rstrip(">")
            link = raw_link.split("|")[0]
            text = content.split(">")[1]
            # TODO: Change this, so it can return an status for each of
            # the actions
            map(lambda x:x.do(text, link), self.plugin_list)

            actions = [k.ACTION_NAME for k in self.plugin_list]
            action_string = " and ".join(actions)

            payload = '{"text" : "Thanks for the link, %s. It has been %s "}' % (user_name, action_string)
        except Exception as err:
            payload = '{"text" : "Sorry %s! Could not process link"}' % user_name
        finally:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Send the html message
            self.wfile.write(payload)

        return

try:
    #Create a web server and define the handler to manage the
    #incoming request
    config = get_config()
    PORT_NUMBER = int(config.get('main', 'port'))
    # TODO: Read this from config file and import them accordingly
    from socialbot.plugins.twitterer import Twitterer
    from socialbot.plugins.relayer import Relayer
    #plugin_list = [Twitterer()]
    plugin_list = [Relayer(), Twitterer()]

    SlackBotHandler.plugin_list = plugin_list
    server = HTTPServer(('', PORT_NUMBER), SlackBotHandler)
    print 'Started httpserver on port ', PORT_NUMBER
    server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
