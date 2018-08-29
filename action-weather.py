#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import io
import requests


import ConfigParser
from hermes_python.hermes import Hermes


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"


class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


def subscribe_intent_callback(hermes, intent_message):
    conf = read_configuration_file(CONFIG_INI)

    action_wrapper(hermes, intent_message, conf)


def action_wrapper(hermes, intent_message, conf):
    """

    :param hermes:
    :param intent_message:
    :param conf:
    :return:
    """
    print(intent_message.intent.intent_name)
    url = 'https://icanhazdadjoke.com/'
    header = {'Accept': 'application/json', 'User-Agent': 'dad-jokes (https://github.com/dmegbert/dad-jokes)'}
    try:
        joke = requests.get(url, headers=header).json()['joke']
    except Exception as ex:
        print('An error occurred: {}'.format(ex))
        joke = 'An error occurred'
    hermes.publish_end_session(intent_message.session_id, joke)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("ElleDadSean:getJoke", subscribe_intent_callback).start()
