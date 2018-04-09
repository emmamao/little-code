::遍历子目录的html文件，重命名并拷贝到指定目录
@echo off&setlocal EnableDelayedExpansion 
set sum=1
for /R %%i in (*.html) do (
ren "%%i" "!sum!.html"
set /a sum+=1
)
for /R %%i in (*.html) do (
copy "%%i" "E:\code\input\"
)
