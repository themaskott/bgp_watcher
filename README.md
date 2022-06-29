# BGP watcher

Watching BGP for fake annoucements regarding a specific set of prefixes


## Purpose

The aim of this project is to watch a define set of prefixes over several BGP collectors, in order to detect inconsistancies in annoucements and prevent hijackings.


## 1 - Which prefixes ?

I chose to monitor all french prefixes registered within the IRR RIPE database.

Those  prefixes are extracted from the IRR RIPE database at : `ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz` and saved as `datas/french_prefixes.json`

(see [irr.py](irr.py))

## 2 - Parameters

Different parameters can be set in [common.py](common.py), such as :
- collectors to be used
- year / month / days range used to build the history

## 3 - Build an history

The history is constructed by parsing one bview per day from the defined ranged in `common.py` and storing all monitored prefixes announced during that period and ASes that announced those prefixes.

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
