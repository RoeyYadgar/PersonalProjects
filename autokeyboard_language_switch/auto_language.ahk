#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#Persistent
#SingleInstance, force
#include Acc.ahk
#MaxThreadsBuffer Off
#MaxThreadsPerHotkey 1

CryptBinaryToString(VarIn, Format)
{
    SizeIn := (Strlen(VarIn) + 1) * 2
    if !(DllCall("crypt32.dll\CryptBinaryToString", "Ptr", &VarIn, "UInt", SizeIn, "UInt", Format, "Ptr", 0, "UInt*", SizeOut))
        return "*" A_LastError
    VarSetCapacity(VarOut, SizeOut << 1, 0)
    if !(DllCall("crypt32.dll\CryptBinaryToString", "Ptr", &VarIn, "UInt", SizeIn, "UInt", Format, "Ptr", &VarOut, "UInt*", SizeOut))
        return "*" A_LastError

    string := StrGet(&VarOut)
    StringReplace,string,string,`r`n,,
    return string
}

CryptStringToBinary(VarIn,Format)
{
    if !(DllCall("crypt32\CryptStringToBinary", "ptr", &VarIn, "uint", 0, "uint", Format, "ptr", 0, "uint*", size, "ptr", 0, "ptr", 0))
        throw Exception("CryptStringToBinary failed", -1)
    VarSetCapacity(buf, size, 0)
    if !(DllCall("crypt32\CryptStringToBinary", "ptr", &VarIn, "uint", 0, "uint", Format, "ptr", &buf, "uint*", size, "ptr", 0, "ptr", 0))
        throw Exception("CryptStringToBinary failed", -1)

    return StrGet(&buf, size, "UTF-16")
}


Shell := ComObjCreate("WScript.Shell")
language_detector := Shell.Exec("C:\Users\User\anaconda3\pythonw.exe predictor.py")
/*
language_detector.Stdin.WriteLine(CryptBinaryToString("vhh nv bang?", 0x0000000c))
x := language_detector.Stdout.ReadLine()

language_detector.Stdin.WriteLine(CryptBinaryToString("hey how is it going?", 0x0000000c))
y := language_detector.Stdout.ReadLine()

MsgBox, %x% , %y%
*/






N := 40



endOfString(string)
{
    global N

    str_len := StrLen(string)
    ind := str_len - N + 1
    len := N
    if(ind < 1)
    {
        ind := 1
        len := str_len
    }
    x := SubStr(string,ind,len)
    return SubStr(string,ind,len)
}

translateString(string,prog)
{
    end_of_string := endOfString(string)
    encoded_string := CryptBinaryToString(end_of_string, 0x0000000c)
    prog.Stdin.WriteLine(encoded_string)
    output := prog.Stdout.ReadLine()
    decoded_output := CryptStringToBinary(output,0x0000000c)
    return decoded_output
}

convertValue(acc_input,child_id_input,prog)
{
    global N
    vRoleText := Acc_Role(acc_input, child_id_input)
    
    if(vRoleText == "editable text" || vRoleText == "combo box")
    {
        vValue := "", try vValue := acc_input.accValue(child_id_input)
        if(StrLen(vValue) >= 5 && StrLen(vValue) <= N)
        {       
            convertedValue := translateString(vValue,prog)
            end_of_string := endOfString(vValue)
            if(end_of_string != convertedValue)
            {
                vValue := acc_input.accValue(child_id_input)
                vValue := StrReplace(vValue, end_of_string,convertedValue)
                acc_input.accValue(child_id_input) := vValue

                

                Send, {Alt Down}{Shift Down}{Shift Up}{Alt Up}
                Send, {End}
            }
        }        
    }
}

oAcc := ""
oAcc_childID := ""
WinEventProc(hHook, event, hWnd, idObject, idChild, eventThread, eventTime)
{
    global N,language_detector,oAcc,oAcc_childID
    Critical
    oAcc := Acc_ObjectFromEvent(_idChild_, hWnd, idObject, idChild)
    oAcc_childID := _idChild_
    ; Code Here:
    convertValue(oAcc,oAcc_childID,language_detector)
    
}
pCallback := RegisterCallback("WinEventProc")
hHook1 := Acc_SetWinEventHook(0x8005,0x8005,pCallback)
hHook2 := Acc_SetWinEventHook(0x800E,0x800E,pCallback)


CapsLock & l::
{
    global oAcc,oAcc_childID
    switchLanguageShell := ComObjCreate("WScript.Shell")
    switchLanguage := switchLanguageShell.Exec("C:\Users\User\anaconda3\pythonw.exe switchLanguage.py")

    WinGet, hWnd, ID, A
    ControlGetFocus, vCtlClassNN, % "ahk_id " hWnd
    ControlGet, hCtl, Hwnd,, % vCtlClassNN, % "ahk_id " hWnd
    acc := Acc_ObjectFromWindow(hCtl)
    ;convertValue(oAcc,oAcc_childID,switchLanguage)
    convertValue(acc,vChildID,switchLanguage)
}


;https://docs.microsoft.com/en-us/windows/win32/winauto/event-constants (event values)
;0x0020 - EVENT_SYSTEM_DESKTOPSWITCH


/*
oAcc := Acc_ObjectFromPoint(vChildID)

;get role number
vRole := "", try vRole := oAcc.accRole(vChildID)
;get role text method 1
vRoleText1 := Acc_Role(oAcc, vChildID)
;get role text method 2 (using role number from earlier)
vRoleText2 := (vRole = "") ? "" : Acc_GetRoleText(vRole)
vName := "", try vName := oAcc.accName(vChildID)
vValue := "", try vValue := oAcc.accValue(vChildID)
oAcc := ""
MsgBox %vRole% , %vRoleText1% , %vRoleText2%, %vValue%
*/
