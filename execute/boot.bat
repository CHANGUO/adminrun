@echo off
rem ֱ��������һ���������ļ�
set "var=%1"
set "var=%var:$= %"
rem echo %var%
start "" "%var%"