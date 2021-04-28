# Notice messages constants
WELCOME = ["안녕하세요! 카톡 통역봇 TransBot이에요!\nHello! I'm your KakaoTalk translator, TransBot!",
           "도움말을 보시려면 '/도움말'을 입력해주세요.\nType '/help' for help."]

HELP_KOR = "/자동, /ㅈ\n" \
           "TransBot을 자동 번역 모드로 설정합니다.\n" \
           "자동 번역 모드가 활성화되어 있을 때에는 TransBot이 톡방의 모든 메시지를 자동으로 번역합니다.\n\n" \
           "/수동, /ㅅ\n" \
           "답장하기 기능으로 메시지를 수동으로 번역할 수 있는 수동 모드로 설정합니다.\n" \
           "수동 번역 모드에서는 번역하고 싶은 메시지에 카카오톡의 '답장하기' 기능으로 '/번역' 또는 '/ㅂ'이라 입력하면 번역됩니다."
HELP_ENG = "/auto, /a\n" \
           "Sets the mode to 'Auto mode'.\n" \
           "In Auto mode, all messages sent to the chat room will be automatically translated.\n\n" \
           "/manual, /m\n" \
           "Sets the mode to 'Manual mode'.\n" \
           "In Manual mode, you can translate messages manually " \
           "by replying '/translate' or '/tr' to the message that you want to will_be_deleted."

SET_AUTO = "이제부터 모든 메시지가 자동으로 변역됩니다.\n" \
           "All messages will be translated automatically from now on."
SET_MANUAL = "이제 메시지가 자동으로 번역되지 않습니다.\n" \
             "All messages will not be translated automatically from now on."

SYNC_START = "동기화 시작\n" \
             "Sync start"

SYNC_COMPLETE = "동기화 완료\n" \
                "Sync complete"


# Error message constants
ERROR_ALREADY_AUTO = "자동 모드는 이미 활성화되어 있습니다.\n" \
                     "Auto mode is already active."

ERROR_ALREADY_MANUAL = "수동 모드는 이미 활성화되어 있습니다.\n" \
                       "Manual mode is already active."

ERROR_MSG_UNSELECTED = "번역할 메시지를 선택해 주세요.\n" \
                       "Select the message to translate."

ERROR_API_LIMIT_EXCEEDED = "PAPAGO API 일일 사용량이 초과되었습니다.\n" \
                           "PAPAGO API daily limit exceeded"

ERROR_UNDEFINED = "알 수 없는 오류가 발생했습니다. 개발자에게 문의해 주세요.\n" \
                  "An undefined error has occurred. Please contact the developers."
