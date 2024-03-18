#EscapeChar, \
#MaxHotkeysPerInterval 200

controlMode := False

numlock:: controlMode := False, runClient("Mode", "Off")
NumpadDiv:: controlMode := True, runClient("Mode","Youtube")
NumpadMult:: controlMode := True, runClient("Mode","Twitch")
NumpadSub:: controlMode := True, runClient("Mode","Mako")
;PgUp:: controlMode := True, runClient("Mode","Netflix")
PgUp:: controlMode := True, runClient("Mode","Kan")


#If controlMode
Media_Play_Pause::runClient("Command","Pause")
Media_Next::runClient("Command","Forward")
Media_Prev::runClient("Command","Backward")
Volume_Up:: runClient("Command","Volume up")
Volume_Down:: runClient("Command","Volume down")
Volume_Mute:: runClient("Command","Mute")
NumpadAdd:: runClient("Command", "Tab cycle")


runClient(field,value)
{
    str = pythonw -B client.pyw "{\\"%field%\\" : \\"%value%\\"}"
    Run %str%
    return
}

