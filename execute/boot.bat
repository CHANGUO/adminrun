@echo off
rem 直接启动第一个参数的文件
set "var=%1"
set "var=%var:$= %"
rem echo %var%
start "" "%var%"