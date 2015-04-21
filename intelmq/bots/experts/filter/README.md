Configuration guidelines and examples for this bot
Definition and usage of bot

XXX to be edited

Previous version:

Bot zpracuje všechny události, které prošli geofilterem na základě nastavení uloženého v souboru s json formátem (viz filter_example.json).
Json konfigurace je zpracována takto:
Každý filtr je zpracován samostatně nezávisle na ostatních
Konfigurace filtru je načtena znovu při každém běhu bota (např. každý den)
Filtr může být buď „type“ exclude nebo include
    exclude znamená, že události, které podmínku filtru splňují, zahodíme
    include znamená, že události, které podmínku filtru splňují, předáváme dál
Filtr může obsahovat položky následující typu:
Taxonomy - hodnoty popsány zde: https://github.com/certtools/intelmq/blob/master/docs/DataHarmonization.md#typetaxonomy-mapping
Type - hodnoty popsány zde: https://github.com/certtools/intelmq/blob/master/docs/DataHarmonization.md#typetaxonomy-mapping
ASN – řetězec s číselným označením autonomního systému, např. "12345"
CIDR – adresa sítě a maska, např. "192.168.100.0/24"
Recipient – email adresáta povolující wildcard před doménou, tedy např. "*@isp.cz"
CC – country code, např. „CZ“ nebo „RU“
V každém poli může být více hodnot a vyhodnocují se logikou „nebo“ - pokud aspoň jeden záznam splňuje podmínku, je splněna podmínka daného typu (např. v typu recipient stačí, pokud dojde ke shodě aspoň v jedné z emailových adres)
Typy jsou mezi sebou vyhodnocována logikou „a zároveň“, musí být tedy být splněny podmínky všech typů, aby byla splněna podmínka celé výjimky (např. musí být splněn typ Taxonomy a zároveň Recipient)