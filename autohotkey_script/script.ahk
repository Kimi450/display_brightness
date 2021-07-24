#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#`:: Run python C:\Users\karan\Desktop\playground\display_brightness\display_brightness.py -tg
#1:: Run python C:\Users\karan\Desktop\playground\display_brightness\display_brightness.py -l 100
#2:: Run python C:\Users\karan\Desktop\playground\display_brightness\display_brightness.py -l 50
#3:: Run python C:\Users\karan\Desktop\playground\display_brightness\display_brightness.py -l 0
#4:: Run python C:\Users\karan\Desktop\playground\display_brightness\display_brightness.py -l custom
#5:: Run python C:\Users\karan\Desktop\playground\display_brightness\display_brightness.py -wc
