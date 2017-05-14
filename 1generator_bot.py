#!/usr/bin/env python3
from _1generator import translate_with, get_replacements
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent
import bcolors
import logging
import telepot

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

def handle_inline(repls, msg):
    try:
        query_id, _, query_string = telepot.glance(msg, flavor="inline_query")
        reply = translate_with(repls, query_string)

        logging.info("Message is query #{}, namely \"{}\"".format(query_id, query_string))

        articles = [InlineQueryResultArticle(
            id="1generator",
            title=reply,
            input_message_content=InputTextMessageContent(message_text=reply)
            )]

        bot.answerInlineQuery(query_id, articles)
        logging.info("Proposing {}".format(reply))
    except telepot.exception.TelegramError:
        pass


if __name__ == "__main__":
    logging.basicConfig(
        format="{}[%(levelname)s %(asctime)s]{} %(message)s".format(
            bcolors.BOLD,
            bcolors.ENDC
        ), level=logging.INFO
    )
    TOKEN = open("meerschweinchen.token").read().strip()

    repls = get_replacements("vong.csv")

    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, {
        "inline_query": lambda msg: handle_inline(repls, msg),
        "chat": lambda msg: handle(repls, msg)
        }).run_forever()
