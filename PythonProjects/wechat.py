import itchat

itchat.auto_login(hotReload=True)
itchat.send('Hello, coder. \n  --send from Python.', toUserName='filehelper')
author = itchat.search_friends(nickName='温暖的弦')[0]
author.send('Goodnight, Honey. \n  --send from Python program.')
itchat.logout()
