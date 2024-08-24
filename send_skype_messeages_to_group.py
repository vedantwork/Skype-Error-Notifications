from skpy import Skype, SkypeChats
sk = Skype('your_skype_email_id', 'your_skype_password') # connect to Skype
skc = SkypeChats(sk)
print("sk ====>>>> ",skc.recent()) # This will get you the skype channel id
sk.user # you
sk.contacts # your contacts
sk.chats # your conversations
# Paste the channel id you get from above
ch = sk.chats.chat('skype_channel_id')
msg_to_send = "testing"
ch.sendMsg(msg_to_send)
ch.getMsgs()
