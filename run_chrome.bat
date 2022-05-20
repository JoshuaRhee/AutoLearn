@echo off

rem Change the path for your chrome.
path C:\Program Files (x86)\Google\Chrome\Application;

rem This line shouldn't be changed.
start chrome.exe --remote-debugging-port=9222 --user-data-dir="%cd%\temp_chrome"