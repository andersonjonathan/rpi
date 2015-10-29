import lirc
sockid = lirc.init("python_remote")

while True:
    code = lirc.nextcode()
    if code:
        print(code[0])
        if code[0] == "KEY_POWER":
            break


