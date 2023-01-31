@echo off

call %~dp0Python310\Lib\venv\scripts\nt\activate
cd %~dp0kur\proj\bot
set TOKEN=MTA0NzQ0NTQ2MDM4MzY5NDg2OQ.Gr2tug.UnxBcuC9wwiXBB-8nUOxtAGW-u7xVJQlWTo6cc
python botrun.py

pause