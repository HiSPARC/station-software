@echo off
call "%~dp0..\..\..\user\startstop\runmanually.bat" 0 \admin\nsclientpp\x32 active_check.py bufferdb %1 %2
