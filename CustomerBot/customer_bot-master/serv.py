from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.channels import HttpInputChannel
from rasa_core import utils
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.channels.channel import UserMessage
from rasa_core.channels.direct import CollectingOutputChannel
from rasa_core.channels.rest import HttpInputComponent
from flask import Blueprint, request, jsonify

logger = logging.getLogger(__name__)
class SimpleWebBot(HttpInputComponent):
    """A simple web bot that listens on a url and responds."""

    def blueprint(self, on_new_message):
        print('in blueprint');
        custom_webhook = Blueprint('custom_webhook', __name__)

        @custom_webhook.route("/status", methods=['GET'])
        def health():
            return jsonify({"status": "ok"})

        @custom_webhook.route("/chat", methods=['POST'])
        def receive():
            payload = request.json
            print('in receive bot')
            print(payload)
            sender_id = payload.get("sender", None)
            text = payload.get("message", None)
            print(text)
            out = CollectingOutputChannel()
            on_new_message(UserMessage(text, out, sender_id))
            responses = [m for _, m in out.messages]
            return jsonify(responses)
    
        return custom_webhook

def run(serve_forever=True):
    #path to your NLU model
    interpreter = RasaNLUInterpreter("C:/Srikanth/2018-Hackathon/git/myHR/CustomerBot/customer_bot-master/models/nlu/current/")
    # path to your dialogues models
    agent = Agent.load("C:/Srikanth/2018-Hackathon/git/myHR/CustomerBot/customer_bot-master/models/dialogue/", interpreter=interpreter)
    #http api endpoint for responses
    input_channel = SimpleWebBot()
    if serve_forever:
        agent.handle_channel(HttpInputChannel(5000, "/parse", input_channel))
    return agent

if __name__ == '__main__':
    run()
