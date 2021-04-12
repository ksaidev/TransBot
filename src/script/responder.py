from src.script.command import Command
from src.script.channel import BotChannel




class Bot:

    def __init__(self):
        pass




    def respond(self, chat):
        channel = BotChannel(chat.channel)
        command = Command(chat.message)

        if channel.isUnregistered():



        """
        main script goes here
        :param chat:
        :return:
        """
        pass

