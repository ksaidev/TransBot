import httpApi

user_id = str(input("ID: "))
user_pw = str(input("PW: "))

device_name = "TransBot"
user_uuid = "TEVWSUNFMQ=="

httpApi.RequestPasscode(user_id, user_pw,
                        device_name, user_uuid)

passcode = str(input("Input Passcode : "))

httpApi.RegisterDevice(user_id, user_pw,
                       device_name, user_uuid, passcode)
