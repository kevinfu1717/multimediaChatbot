

import time
import asyncio

import logging
from typing import Optional, Union

from wechaty_puppet import PuppetOptions, FileBox  # type: ignore

from wechaty import Wechaty, Contact
from wechaty.user import Message, Room

# from .tencentaiplat import TencentAI
import botProcess

from talkProcess import talkManger
import os
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(filename)s <%(funcName)s> %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger('DingDongBot')

chat_friend: list = []
splitNum = 5
bm = botProcess.botManger(3)
path = '/root/paddlejob/workspace/output'
print('path', path, os.path.exists(path))
tm = talkManger(path, path)
async def message(msg: Message):
    """back on message"""
    from_contact = msg.talker()
    username = from_contact.name
    text = msg.text()
    room = msg.room()
    conversation: Union[
        Room, Contact] = from_contact if room is None else room

    global chat_friend
    global splitNum
    global bm
    global tm

    if "吐槽" in text or "图槽" in text or "树洞" in text :
        chat_friend.append(conversation)
        inputdata = "#str#" + msg.text()
        print('————text')

        bot = bm.run(username, inputdata)
        if bot is not None:
            # print('bot', bot)
            # print('bot replys',bot.replys[-1])
            # print('bot.replys_index',bot.replys_index)
            for i in range(bot.replys_index):
                bot, rdict = tm.run(bot)
                print('rdict', rdict)
                if len(list(rdict.keys())) == 0: continue
                if list(rdict.keys())[0] == "str":
                    print('reply str')
                    conversation: Union[
                        Room, Contact] = from_contact if room is None else room

                    await conversation.ready()
                    print('rdict[splitNum:]', list(rdict.values())[0])
                    await conversation.say(list(rdict.values())[0])
                elif list(rdict.keys())[0] == "pic" or 'mov':
                    print('reply pic/mov')
                    conversation: Union[
                        Room, Contact] = from_contact if room is None else room

                    await conversation.ready()
                    try:
                        file_box = FileBox.from_file(list(rdict.values())[0])
                    except Exception as e:
                        print('file box error', e)
                        file_box = '嗯嗯'
                    await conversation.say(file_box)
        # await conversation.ready()
        # await conversation.say('闲聊功能开启成功！现在你可以和我聊天啦！')
        return

    if conversation in chat_friend:
        if username=='KFu':
            print('KFu')
            return
        if msg.type() == Message.Type.MESSAGE_TYPE_IMAGE:

            print('__image')
            image_file_box = await msg.to_file_box()
            filename='p'+str(time.time())+'.jpg'
            await image_file_box.to_file(file_path=filename,overwrite=True)
            inputdata="#pic#"+filename
        elif   msg.type() == Message.Type.MESSAGE_TYPE_TEXT:
            print('--text')
            inputdata = "#str#" + msg.text()
            bot = bm.run(username, inputdata)
            if bot is not None:
                # print('bot', bot)
                # print('bot replys',bot.replys[-1])
                # print('bot.replys_index',bot.replys_index)
                for i in range(bot.replys_index):
                    bot, rdict = tm.run(bot)
                    print('rdict', rdict)
                    if len(list(rdict.keys())) == 0: continue
                    if list(rdict.keys())[0] == "str":
                        print('reply str')
                        conversation: Union[
                            Room, Contact] = from_contact if room is None else room

                        await conversation.ready()
                        print('rdict[splitNum:]', list(rdict.values())[0])
                        await conversation.say(list(rdict.values())[0])
                    elif list(rdict.keys())[0] == "pic" or 'mov':
                        print('reply pic/mov')
                        conversation: Union[
                            Room, Contact] = from_contact if room is None else room

                        await conversation.ready()
                        try:
                            file_box = FileBox.from_file(list(rdict.values())[0])
                        except Exception as e:
                            print('file box error', e)
                            file_box = '嗯嗯'
                        await conversation.say(file_box)
        # data = TencentAI(text)
        # await conversation.ready()
        # await conversation.say(data)
        return
    else:
        print('not in friend')
        return




bot: Optional[Wechaty] = None


async def main():
    """doc"""
    # pylint: disable=W0603
    global bot
    bot = Wechaty().on('message', message)
    await bot.start()


asyncio.run(main())