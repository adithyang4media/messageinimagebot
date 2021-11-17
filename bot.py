#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import telegram
import os
import sys
import requests

import cv2
import numpy as np




import bot
from telegram.ext import ConversationHandler


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

H2, H3, H4, R2 = range(4)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')
    update.message.reply_text('I Am Online')
    update.message.reply_text('This Bot Was Made By @g4_media')
    update.message.reply_text('Please Consider Subscribing our Youtube Channel https://www.youtube.com/channel/UCad4U0t57KqjvHxqqdmZW_w')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')
    update.message.reply_text("This is a Multi Function Bot\nThis Bot was Made By @g4_media\n\nThis Bot Can Rename Files Upto 100MB\n	For This you Have to send the document to this bot\n	And provide new name whwn asked\n\nThis Bot Can Convert Voice Messege to audio file and audio document\n	For this you Have to send the voice message to this bot\n	And provide filename with disired filetype extention\n	eg : music.mp3\n	You will get the voice message as audio file and audio document\n\nThis Bot Can Convert Audio file to voice message\n	For this you have to send the audio file to ths bot\n	And you will get the audio file as voice message\n\nThis Bot Can Clear Captions of image\n	Just Send the image \n	You will get the Image as caption cleared")

def fuck(update, context):
    """Send a message when the command /fuck is issued."""
    update.message.reply_text('come lets do sex!')

def hai(update, context):
    """Send a message when the command /hai is issued."""
    update.message.reply_text('hello how are you')

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data):
    # read the image
    image = cv2.imread(image_name)
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    secret_data += "====="
    data_index = 0
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # convert RGB values to binary format
            r, g, b = to_bin(pixel)
            # modify the least significant bit only if there is still data to store
            if data_index < data_len:
                # least significant red pixel bit
                pixel[0] = int(r[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant green pixel bit
                pixel[1] = int(g[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            if data_index < data_len:
                # least significant blue pixel bit
                pixel[2] = int(b[:-1] + binary_secret_data[data_index], 2)
                data_index += 1
            # if data is encoded, just break out of the loop
            if data_index >= data_len:
                break
    return image

def decode(image_name):
    update.message.reply_text("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for row in image:
        for pixel in row:
            r, g, b = to_bin(pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    # split by 8-bits
    all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
    # convert from bits to characters
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "=====":
            break
    return decoded_data[:-5]

def hide1(update, context):
    update.message.reply_text("Send me the image which you want to hide your message")
    return H2

def hide2(update, context):
    global photo
    global fileid
    photo = update.message.photo[-1]
    fileid = update.message.photo[-1].file_id
    update.message.reply_text("Now send me the text which you want to hide ")
    return H3

def hide3(update, context):
    global mes
    mes=update.message.text
    update.message.reply_text("Now Send Me a Filename for the text hidden image ")
    return H4

def hide4(update, context):
    gname=update.message.text
    filename=gname + ".png"
    inputimg=gname + ".jpg"
    file = context.bot.getFile(fileid)
    file.download(inputimg)
    # encode the data into the image
    encoded_image = encode(image_name=filename, secret_data=mes)
    # save the output image (encoded image)
    cv2.imwrite(filename, encoded_image)
    context.bot.sendDocument(chat_id=update.effective_chat.id, document=open(filename, 'rb'), filename=filename)
    return ConversationHandler.END



def unhide1(update, context):
    update.message.reply_text("Send me the image file which you want extract the message")
    return R2

def unhide2(update, context):
    fileid=update.message.document.file_id
    filename=update.message.document.file_name
    file = context.bot.getFile(fileid)
    file.download(filename)
    # decode the secret data from the image
    decoded_data = decode(filename)
    decodeddata="[+] Decoded data: " + decoded_data
    update.message.reply_text(decodeddata)
    return ConversationHandler.END






def main():
   """Start the bot."""
   # Create the Updater and pass it your bot's token.
   # Make sure to set use_context=True to use the new context based callbacks
   # Post version 12 this will no longer be necessary
   updater = Updater(os.environ['bottoken'], use_context=True)

   # Get the dispatcher to register handlers
   dp = updater.dispatcher

   # on different commands - answer in Telegram
   dp.add_handler(CommandHandler("start", start))
   dp.add_handler(CommandHandler("help", help))
   dp.add_handler(CommandHandler("fuck", fuck))
   dp.add_handler(CommandHandler("hai", hai))

   hide_handler = ConversationHandler(
        entry_points=[CommandHandler("hide", hide1)],
        states={

            H2: [MessageHandler(Filters.photo, hide2)]
            H3: [MessageHandler(Filters.text, hide3)]
            H4: [MessageHandler(Filters.text, hide4)]

        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
    )

   dp.add_handler(hide_handler)

   unhide_handler = ConversationHandler(
        entry_points=[CommandHandler("unhide", unhide1)],
        states={

            R2: [MessageHandler(Filters.document, unhide2)]


        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
    )

   dp.add_handler(unhide_handler)
