# BGP watcher

Watching BGP for fake annoucements regarding a specific set of prefixes


## Purpose

The aim of this project is to watch a define set of prefixes over several BGP collectors, in order to detect inconsistencies in annoucements and prevent hijackings.


## 1 - Which prefixes ?

I chose to monitor all french prefixes registered within the IRR RIPE database.

Those  prefixes are extracted from the IRR RIPE database at : `ftp://ftp.ripe.net/ripe/dbase/split/ripe.db.inetnum.gz` and saved as `datas/french_prefixes.json`

(see [irr.py](irr.py))

## 2 - Parameters

Different parameters can be set in [common.py](common.py), such as :
- collectors to be used
- year / month / days range used to build the history

## 3 - Build an history

The history is constructed by parsing one bview per day from the difined ranged in `common.py` and storing all monitored prefixes announced during that period and ASes that announced those prefixes.


## 4 - Monitor latest bview


## 5 - Watch the upadtes

## Requirements
