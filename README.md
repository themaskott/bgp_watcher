# BGP watcher

Watching BGP for fake annoucements regarding a specific set of prefixes


<p align="center">
  <img src="img/HuntForRedOctober.jpg" />
</p>


## Purpose

The aim of this project is to watch a define set of prefixes over several BGP collectors, in order to detect inconsistancies in annoucements and prevent hijackings.

Due to its trust based nature, BGP is very likely to be abuse either by network administrators (that use it for load balancing or anti-ddos purposes) or by attackers whiling ot hijack a range of IP addresses.

The very difficulty while monitoring BGP is to discern whether a misconfiguration is still legitimate or reveal a possible attack. To to so, this project will try to reduce the number of those legitimate misconfiguration, ending with a human-handprocessing number of cases.


## 1 - Which prefixes ?

I chose to monitor all french prefixes registered within the IRR RIPE database.

Those  prefixes are extracted from the IRR RIPE database at : ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz and saved as `datas/french_prefixes.json`

(see [irr.py](irr.py))

## 2 - Parameters

Different parameters can be set in [common.py](common.py), such as :
- collectors to be used
- year / month / days range used to build the history

List of existing collectors :

| Num | City | Type | Owner |
|-----|------|------|-------|
|RRC00 |	Amsterdam, NL  |	 multihop 	global|
|RRC01 |	London, GB 	   |  IXP 	LINX | LONAP
|RRC03 |	Amsterdam, NL | IXP 	AMS-IX | NL-IX
|RRC04 |	Geneva, CH 	  |   IXP |	CIXP
|RRC05 |	Vienna, AT 	  |   IXP |	VIXP
|RRC06 |	Otemachi, JP 	| IXP 	| DIX-IE
|RRC07 |	Stockholm, SE |   IXP | Netnod
|RRC10 |	Milan, IT 	  |   IXP |	MIX
|RRC11 |	New York, US  |   IXP |	NYIIX
|RRC12 |	Frankfurt, DE |	 IXP 	| DE-CIX
|RRC13 | 	Moscow, RU 	  |   IXP |	MSK-IX
|RRC14 |	Palo Alto, US |	IXP 	| PAIX
|RRC15 |	Sao Paolo, BR |	 IXP 	| PTTMetro-SP
|RRC16 |	Miami, FL, US |	 IXP 	| Equinix Miami
|RRC18 |	Barcelona, ES |	 IXP 	| CATNIX
|RRC19 |	Johannesburg, ZA | IXP |	NAP Africa JB
|RRC20 |	Zurich, CH 	  |   IXP |	SwissIX
|RRC21 |	Paris, FR 	  |   IXP |	France-IX Paris and France-IX Marseille
|RRC22 | 	Bucharest, RO |	 IXP 	| Interlan
|RRC23 |	Singapore, SG |	 IXP 	| Equinix Singapore
|RRC24 |	Montevideo, UY| 	 multihop |	LACNIC region
|RRC25 |	Amsterdam, NL |	 multihop 	global
|RRC26 |	Dubai, AE 	  |   IXP |	UAE-IX


## 3 - Build an history

The history is constructed by parsing one bview per day from the defined period in `common.py` and storing all monitored prefixes announced during that period and ASes that announced those prefixes.

Then, this history will be used to discard inconsistancies in further annoucements.

A prefix could be announced by :
- its legitimate owner (the AS declared by the organisation owning this prefix)
- another AS owned by the same organisation (most of the time for network administration purposes)
- an AS unrelated to the legitimate one

The major difficulty while searching hijackings is to determine if an inconsistancy is a real hijacking or due to a network administration task.


## 4 - Monitor latest bview

After that, latests bview from considered collectors are parsed in order to extract :
- MOAS (Multiple Origin AS) : a prefix announced by more than one AS
- a foreign AS announcing a french prefix : if the announcement has not be seeing in previous history, it is to be considered as an inconsistancy

## 5 - Watch the upadtes

Finaly, latests updates from considered collectors are parsed every 5 minutes to extract :
- MOAS
- foreign AS announcing a french prefix
- a subnet of a french prefix announced by a foreign AS (known as more specific announcement)

## Requirements

`bgpdump` as to be build and placed inside the same folder : https://github.com/RIPE-NCC/bgpdump

## Ressources

- Collectors : https://data.ris.ripe.net/rrc01/ (change collector number)
- Collectors : https://www.ris.ripe.net/peerlist/all.shtml
- AS : https://www.cidr-report.org/as2.0/autnums.html
- RIPE : ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz

## Run

```shell
$ python3 watcher.py
BGP watcher
    Collectors : 6/14/26
    History : 25 to 29 of 06-2022

[+] Seting up env
[+] Checking ripe.db.inetnum.gz
[*] Updating french prefixes from ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz
[+] Checking french ASes db
[*] Updating french ASes from https://www.cidr-report.org/as2.0/autnums.html
[+] Building history
        [+] Downloading https://data.ris.ripe.net/rrc06/2022.06/bview.20220625.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-25-rrc06-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-25-rrc06-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc06/2022.06/bview.20220626.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-26-rrc06-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-26-rrc06-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc06/2022.06/bview.20220627.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-27-rrc06-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-27-rrc06-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc06/2022.06/bview.20220628.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-28-rrc06-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-28-rrc06-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc14/2022.06/bview.20220625.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-25-rrc14-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-25-rrc14-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc14/2022.06/bview.20220626.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-26-rrc14-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-26-rrc14-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc14/2022.06/bview.20220627.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-27-rrc14-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-27-rrc14-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc14/2022.06/bview.20220628.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-28-rrc14-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-28-rrc14-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc26/2022.06/bview.20220625.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-25-rrc26-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-25-rrc26-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc26/2022.06/bview.20220626.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-26-rrc26-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-26-rrc26-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc26/2022.06/bview.20220627.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-27-rrc26-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-27-rrc26-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc26/2022.06/bview.20220628.0800.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-28-rrc26-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-28-rrc26-dump.txt
[+] Checking latests bview
        [+] Downloading https://data.ris.ripe.net/rrc06/latest-bview.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc06-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc06-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc14/latest-bview.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc14-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc14-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc26/latest-bview.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc26-bview.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc26-dump.txt
[>] Prefix 62.244.102.0/24       announced by 31693/8565         Tag moas
[>] Prefix 77.111.208.0/22       announced by 53550/200077       Tag moas
[>] Prefix 81.171.106.0/24       announced by 12989/33438        Tag moas
[>] Prefix 83.243.16.0/21        announced by 31216/4455         Tag moas
[>] Prefix 89.30.40.0/21         announced by 31216/4455         Tag moas
[>] Prefix 89.30.109.0/24        announced by 31216/201313/4455  Tag moas
[>] Prefix 89.30.121.0/24        announced by 31216/4455         Tag moas
[>] Prefix 91.199.242.0/24       announced by 55569/44788/19750  Tag moas
[>] Prefix 91.212.98.0/24        announced by 55569/44788        Tag moas
[>] Prefix 178.171.72.0/22       announced by 9009/213296        Tag moas
[>] Prefix 185.3.24.0/22         announced by 15830/24990        Tag moas
[>] Prefix 185.37.220.0/22       announced by 200077/53550       Tag moas
[>] Prefix 185.37.220.0/24       announced by 53550/200077       Tag moas
[>] Prefix 185.147.212.0/24      announced by 12989/33438        Tag moas
[>] Prefix 185.175.103.0/24      announced by 47582/206819       Tag moas
[>] Prefix 185.253.54.0/24       announced by 834/210619         Tag moas
[>] Prefix 193.26.22.0/24        announced by 61317/12874        Tag moas
[>] Prefix 193.27.78.0/23        announced by 31216/4455         Tag moas
[>] Prefix 193.104.158.0/24      announced by 202213/50183       Tag moas
[>] Prefix 193.202.125.0/24      announced by 31216/4455         Tag moas
[>] Prefix 193.218.12.0/22       announced by 31216/4455         Tag moas
[>] Prefix 194.0.9.0/24  announced by 2484/2486  Tag moas
[>] Prefix 194.50.95.0/24        announced by 31216/4455         Tag moas
[>] Prefix 212.180.11.0/24       announced by 65154/4589         Tag moas
[>] Prefix 212.180.17.0/24       announced by 65154/4589         Tag moas
[>] Prefix 217.69.16.0/20        announced by 15830/24990        Tag moas
[>] Prefix 185.144.12.0/24       announced by 834/207459         Tag moas
[>] Prefix 62.244.102.0/24       announced by 31693/8565         Tag moas
[>] Prefix 77.111.208.0/22       announced by 53550/200077       Tag moas
[>] Prefix 81.171.106.0/24       announced by 12989/33438        Tag moas
[>] Prefix 83.243.16.0/21        announced by 31216/4455         Tag moas
[>] Prefix 89.30.40.0/21         announced by 31216/4455         Tag moas
[>] Prefix 89.30.109.0/24        announced by 31216/201313/4455  Tag moas
[>] Prefix 89.30.121.0/24        announced by 31216/4455         Tag moas
[>] Prefix 91.199.242.0/24       announced by 55569/44788/19750  Tag moas
[>] Prefix 91.212.98.0/24        announced by 55569/44788        Tag moas
[>] Prefix 178.171.72.0/22       announced by 9009/213296        Tag moas
[>] Prefix 185.3.24.0/22         announced by 15830/24990        Tag moas
[>] Prefix 185.37.220.0/22       announced by 200077/53550       Tag moas
[>] Prefix 185.37.220.0/24       announced by 53550/200077       Tag moas
[>] Prefix 185.147.212.0/24      announced by 12989/33438        Tag moas
[>] Prefix 185.175.103.0/24      announced by 47582/206819       Tag moas
[>] Prefix 185.253.54.0/24       announced by 834/210619         Tag moas
[>] Prefix 193.26.22.0/24        announced by 61317/12874        Tag moas
[>] Prefix 193.27.78.0/23        announced by 31216/4455         Tag moas
[>] Prefix 193.104.158.0/24      announced by 202213/50183       Tag moas
[>] Prefix 193.202.125.0/24      announced by 31216/4455         Tag moas
[>] Prefix 193.218.12.0/22       announced by 31216/4455         Tag moas
[>] Prefix 194.0.9.0/24  announced by 2484/2486  Tag moas
[>] Prefix 194.50.95.0/24        announced by 31216/4455         Tag moas
[>] Prefix 212.180.11.0/24       announced by 65154/4589         Tag moas
[>] Prefix 212.180.17.0/24       announced by 65154/4589         Tag moas
[>] Prefix 217.69.16.0/20        announced by 15830/24990        Tag moas
[>] Prefix 185.144.12.0/24       announced by 834/207459         Tag moas
[>] Prefix 62.244.102.0/24       announced by 31693/8565         Tag moas
[>] Prefix 77.111.208.0/22       announced by 53550/200077       Tag moas
[>] Prefix 81.171.106.0/24       announced by 12989/33438        Tag moas
[>] Prefix 83.243.16.0/21        announced by 31216/4455         Tag moas
[>] Prefix 89.30.40.0/21         announced by 31216/4455         Tag moas
[>] Prefix 89.30.109.0/24        announced by 31216/201313/4455  Tag moas
[>] Prefix 89.30.121.0/24        announced by 31216/4455         Tag moas
[>] Prefix 91.199.242.0/24       announced by 55569/44788/19750  Tag moas
[>] Prefix 91.212.98.0/24        announced by 55569/44788        Tag moas
[>] Prefix 178.171.72.0/22       announced by 9009/213296        Tag moas
[>] Prefix 185.3.24.0/22         announced by 15830/24990        Tag moas
[>] Prefix 185.37.220.0/22       announced by 200077/53550       Tag moas
[>] Prefix 185.37.220.0/24       announced by 53550/200077       Tag moas
[>] Prefix 185.147.212.0/24      announced by 12989/33438        Tag moas
[>] Prefix 185.175.103.0/24      announced by 47582/206819       Tag moas
[>] Prefix 185.253.54.0/24       announced by 834/210619         Tag moas
[>] Prefix 193.26.22.0/24        announced by 61317/12874        Tag moas
[>] Prefix 193.27.78.0/23        announced by 31216/4455         Tag moas
[>] Prefix 193.104.158.0/24      announced by 202213/50183       Tag moas
[>] Prefix 193.202.125.0/24      announced by 31216/4455         Tag moas
[>] Prefix 193.218.12.0/22       announced by 31216/4455         Tag moas
[>] Prefix 194.0.9.0/24  announced by 2484/2486  Tag moas
[>] Prefix 194.50.95.0/24        announced by 31216/4455         Tag moas
[>] Prefix 212.180.11.0/24       announced by 65154/4589         Tag moas
[>] Prefix 212.180.17.0/24       announced by 65154/4589         Tag moas
[>] Prefix 217.69.16.0/20        announced by 15830/24990        Tag moas
[>] Prefix 185.144.12.0/24       announced by 834/207459         Tag moas
[+] Computing all FR subnets
[+] Update n°1
        [+] Downloading https://data.ris.ripe.net/rrc06/latest-update.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc06-update.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc06-update-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc14/latest-update.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc14-update.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc14-update-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc26/latest-update.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc26-update.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc26-update-dump.txt
[+] Update n°2
        [+] Downloading https://data.ris.ripe.net/rrc06/latest-update.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc06-update.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc06-update-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc14/latest-update.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc14-update.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc14-update-dump.txt
        [+] Downloading https://data.ris.ripe.net/rrc26/latest-update.gz
        [+] Parsing datas_rrc06-14-26_202206/2022-06-30-rrc26-update.gz
        [+] Processing datas_rrc06-14-26_202206/2022-06-30-rrc26-update-dump.txt
[>] Prefix 81.253.99.0/24        announced by 8376       Tag more_spec
[>] Prefix 171.18.128.0/22       announced by 397993     Tag more_spec
[>] Prefix 163.116.226.0/24      announced by 55256      Tag more_spec
[>] Prefix 178.236.232.0/24      announced by 134548     Tag more_spec
[>] Prefix 81.253.99.0/24        announced by 8376       Tag more_spec
[>] Prefix 171.18.128.0/22       announced by 397993     Tag more_spec
[>] Prefix 163.116.226.0/24      announced by 55256      Tag more_spec
[>] Prefix 178.236.232.0/24      announced by 134548     Tag more_spec
[>] Prefix 81.253.99.0/24        announced by 8376       Tag more_spec
[>] Prefix 171.18.128.0/22       announced by 397993     Tag more_spec
[>] Prefix 163.116.226.0/24      announced by 55256      Tag more_spec
[>] Prefix 178.236.232.0/24      announced by 134548     Tag more_spec
```
