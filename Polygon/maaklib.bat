SETLOCAL EnableExtensions

for %%I in (library\whalm\*.geo) do C:\Users\Tjibbe\AppData\Local\Programs\Python\Python38\python.exe parser.py "%%~nI"
