::������Ŀ¼��html�ļ�����������������ָ��Ŀ¼
@echo off&setlocal EnableDelayedExpansion 
set sum=1
for /R %%i in (*.html) do (
ren "%%i" "!sum!.html"
set /a sum+=1
)
for /R %%i in (*.html) do (
copy "%%i" "E:\code\input\"
)
