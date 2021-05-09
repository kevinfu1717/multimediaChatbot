# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:27:33 2021

@author: D&E Tech
"""
"""
set WECHATY_PUPPET_SERVICE_TOKEN="puppet_padlocal_2d7902aeb6ec4160a22bf146c8a532f7"
set WECHATY_PUPPET_SERVICE_TOKEN=kevinsun17
"""
import time
import asyncio
import logging
from typing import Optional, Union
import os
from wechaty_puppet import FileBox, ScanStatus  # type: ignore

# from wechaty import Wechaty, Contact
from wechaty.user import Message, Room
import botProcess

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

from talkProcess import talkManger

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def create_gif():
    """
    refer to : https://note.nkmk.me/en/python-pillow-gif/
    you can create gif file with your own code.
    """
    from PIL import Image, ImageDraw

    images = []

    width = 200
    center = width // 2
    color_1 = (0, 0, 0)
    color_2 = (255, 255, 255)
    max_radius = int(center * 1.5)
    step = 8

    for i in range(0, max_radius, step):
        im = Image.new('RGB', (width, width), color_1)
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - i, center - i, center + i, center + i), fill=color_2)
        images.append(im)

    for i in range(0, max_radius, step):
        im = Image.new('RGB', (width, width), color_2)
        draw = ImageDraw.Draw(im)
        draw.ellipse((center - i, center - i, center + i, center + i), fill=color_1)
        images.append(im)

    images[0].save('./bot.gif',
                   save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)





class MyBot(Wechaty):
    """
    listen wechaty event with inherited functions, which is more friendly for
    oop developer
    """
    def __init__(self):
        super().__init__()
        self.splitNum=5
        self.bm = botProcess.botManger(3)
        path='/root/paddlejob/workspace/output/'
        print('path',path,os.path.exists(path))
        self.tm = talkManger(path, path)
        # if os.path.exists(path):
        #
        #     self.tm = talkManger(path, path)
        # else:
        #     self.tm = talkManger()

    async def on_message(self, msg: Message):
        """
        listen for message event
        """
        from_contact = msg.talker()
        text = msg.text()
        type = msg.type()
        room = msg.room()
        #
        username = from_contact.name
        if username=='KFu':
            print('message from myself')
            return
        # 不处理群消息
        # if room is None:
        if msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:

            print('__image')
            image_file_box = await msg.to_file_box()
            filename='p'+str(time.time())+'.jpg'

            await image_file_box.to_file(file_path=filename,overwrite=True)
            inputdata="#pic#"+filename
            bot = self.bm.run(username, inputdata)
            if bot is not None:
                # print('bot',bot)
                # print('bot replys',bot.replys[-1])
                # print('bot.replys_index',bot.replys_index)
                for i in range(bot.replys_index):
                    bot, rdict = self.tm.run(bot)
                    print('rdict',rdict)

                    if len(list(rdict.keys()))==0:continue
                    if list(rdict.keys())[0] == "str":
                        print('reply str')
                        conversation: Union[
                        Room, Contact] = from_contact if room is None else room
                        print('ready')
                        await conversation.ready()
                        print(list(rdict.values())[0])
                        await conversation.say(list(rdict.values())[0])
                    elif list(rdict.keys())[0] == "pic" or 'mov':
                        print('reply pic/mov')

                        conversation: Union[
                            Room, Contact] = from_contact if room is None else room

                        await conversation.ready()
                        try:
                            file_box = FileBox.from_file(list(rdict.values())[0])
                        except Exception as e:
                            print('file box error',e)
                            file_box='嗯嗯'
                        await conversation.say(file_box)

        elif   msg.type() == Message.Type.MESSAGE_TYPE_TEXT:
            inputdata = "#str#" + msg.text()
            print('————text')

            bot = self.bm.run(username, inputdata)
            if bot is not None:
                # print('bot', bot)
                # print('bot replys',bot.replys[-1])
                # print('bot.replys_index',bot.replys_index)
                for i in range(bot.replys_index):
                    bot, rdict = self.tm.run(bot)
                    print('rdict',rdict)
                    if len(list(rdict.keys()))==0:continue
                    if list(rdict.keys())[0] == "str":
                        print('reply str')
                        conversation: Union[
                            Room, Contact] = from_contact if room is None else room

                        await conversation.ready()
                        print('rdict[splitNum:]',list(rdict.values())[0])
                        await conversation.say(list(rdict.values())[0])
                    elif list(rdict.keys())[0] == "pic" or 'mov':
                        print('reply pic/mov')
                        conversation: Union[
                            Room, Contact] = from_contact if room is None else room

                        await conversation.ready()
                        try:
                            file_box = FileBox.from_file(list(rdict.values())[0])
                        except Exception as e:
                            print('file box error',e)
                            file_box='嗯嗯'
                        await conversation.say(file_box)
        else:
                print('__new for dict')
                conversation: Union[
                    Room, Contact] = from_contact if room is None else room
                await conversation.ready()
                await conversation.say('暂时不支持这种类型的消息哦')

    async def on_login(self, contact: Contact):
        print(f'user: {contact} has login')

    async def on_scan(self, status: ScanStatus, qr_code: Optional[str] = None,
                      data: Optional[str] = None):
        contact = self.Contact.load(self.contact_id)
        print(f'user <{contact}> scan status: {status.name} , '
              f'qr_code: {qr_code}')


async def main():
    """doc"""
#    create_gif()
    bot = MyBot()
    await bot.start()


asyncio.run(main())