from DB import mode
from language.interpret import interpreter

import text

def respond(chat):
    chatId = chat.channel.chatId
    message = chat.message

    # Always works (regardless of mode)
    if message == '/도움말':
        return [text.korHelpMsg]
    if message == '/help':
        return [text.engHelpMsg]
    if message in ['/등록', '/reg']:
        return [text.alreadyRegistered]


    # Mode change
    if message in ['/수동', '/ㅅ', '/manual', '/m']:
        if mode.isActivated(chat):
            mode.deactivate(chatId)
            return [text.changeToManual]

        else:
            return [text.alreadyManual]

    if message in ['/자동', '/ㅈ', '/auto', '/a']:
        if mode.isActivated(chat):
            return [text.alreadyAuto]

        else:
            mode.activate(chatId)
            return [text.changeToAuto]


    # Manual Translation
    if message in ['/번역', '/ㅂ', '/translate', '/tr']:
        if chat.type == 26:
            extra = chat.attachment

            msg = extra['src_message']
            res = interpreter(msg)

            # TODO
            '''
            if extra['attach_type'] in [1, 26]:


            else:
            '''

            return ['[Manual Translate] ' + res]

        else:
            return [text.ManualSelectionError]

    # Auto Translation
    if mode.isActivated(chat):
        res = interpreter(chat.message)
        return ['[Auto Translate] ' + res]

    return []


def register(chat):
    message = chat.message
    chatId = chat.chatId

    if message in ['/등록', '/reg', '/register']:
        mode.activate(chatId)

        return text.welcomeMsg

    else:
        # TODO : 이 메시지 한번만 출력되게 하기 - Database
        return [text.registrationReq]


def translatable(chat):
    if chat.type in [1, 26]:
        return True
    
    message = chat.message
    # TODO



