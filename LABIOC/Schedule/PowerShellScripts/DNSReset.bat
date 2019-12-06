
for /F "skip=3 tokens=1,2,3* delims= " %%G in ('netsh interface show interface') DO (
IF "%%H"=="Connected" netsh interface ip set dns name = "%%J" source = dhcp)