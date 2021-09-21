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

