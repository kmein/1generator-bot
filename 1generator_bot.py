#!/usr/bin/env python3
import bcolors

import logging
import telepot

from _1generator import translate_with, get_replacements

def handle(repls, msg):
    content_type, _, chat_id, _, message_id = telepot.glance(msg, long=True)
    logging.info("Received a {} in chat {} with ID {}".format(content_type, chat_id, message_id))
    if content_type == "text":
        text = msg["text"]
        reply = translate_with(repls, text)
        logging.info("Message is a {}, namely \"{}\"".format(content_type, text))
        logging.info("Sending response \"{}\" in chat {} to ID {}".format(reply, chat_id, message_id))
        bot.sendMessage(chat_id, reply, reply_to_message_id=message_id)
    else:
        logging.info("Done")

if __name__ == "__main__":
    logging.basicConfig(
        format="{}[%(levelname)s %(asctime)s]{} %(message)s".format(
            bcolors.BOLD,
            bcolors.ENDC
        ), level=logging.INFO
    )
    TOKEN = open("1generator.token").read().strip()

    repls = get_replacements("vong.csv")

    bot = telepot.Bot(TOKEN)
    bot.message_loop(lambda msg: handle(repls, msg), run_forever=True)
