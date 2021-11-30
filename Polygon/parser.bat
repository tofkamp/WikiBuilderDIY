SETLOCAL EnableExtensions
rem del Library\whalm.json
rem for %%I in (library\whalm\*.geo) do C:\Users\Tjibbe\AppData\Local\Programs\Python\Python38\python.exe parser.py --library library/whalm.json --objpath obj "%%I"

C:\Users\Tjibbe\AppData\Local\Programs\Python\Python38\python.exe parser.py --library library\whalm.json --objpath obj -i %1 %2 %3 %4 %5 %6 %7 %8 %9
rem C:\Users\Tjibbe\AppData\Local\Programs\Python\Python38\python.exe parser.py --objpath obj -i %1 %2 %3 %4 %5 %6 %7 %8 %9

copy Library\Whalm.json c:\users\tjibbe\unity\fps3\Library /Y
