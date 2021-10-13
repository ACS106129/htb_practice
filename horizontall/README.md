# Horizontall

## Ifconfig

```
inet 10.10.14.46 destination 10.10.14.46
inet6 fe80::c5a7:fe18:4b74:a136
```

## Nmap

> sudo nmap -sC -sV -A 10.10.11.105 | tee [nmap.log](./nmap.log)

### Redirect to certain domain, but the domain not match the ip

- Add the ip-domain to `/etc/hosts`

> 10.10.11.105 horizontall.htb

- And then use this domain to analysis

## Gobuster

> gobuster dir -u horizontall.htb -w /usr/share/wordlists/dirb/common.txt -t 100 | tee [gobuster.log](./gobuster.log)

=> Nothing special

## Nikto

> nikto -h horizontall.htb | tee [nikto.log](./nikto.log)

## Find source at site

Look there are any hints in those files

### [App.c68eb462.js](./site/app.c68eb462.js)

> cat [app.c68eb462.js](./site/app.c68eb462.js) | grep horizontall.htb

```
...data:function(){return{reviews:[]}},methods:{getReviews:function(){var t=this;r.a.get("http://api-prod.horizontall.htb/reviews").then(...
```

=> **api-prod.horizontall.htb** may be exist

- Add the domain to `/etc/hosts` in order to match ip

> 10.10.11.105 api-prod.horizontall.htb

### Gobuster

> gobuster dir -u api-prod.horizontall.htb -w /usr/share/wordlists/dirb/common.txt -t 100 | tee [gobuster_api-prod.log](./gobuster_api-prod.log)

### Nikto

> nikto -h api-prod.horizontall.htb | tee [nikto_api-prod.log](./nikto_api-prod.log)


