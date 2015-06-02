from datetime import datetime, timedelta
from dateutil.tz import tzutc
import types
import re


__HEADERS = ["SourcedFrom", "FileTimeUtc",
             "Botnet", "SourceIp",
             "SourcePort", "SourceIpAsnNr",
             "TargetIp", "TargetPort",
             "Payload", "SourceIpCountryCode",
             "SourceIpRegion", "SourceIpCity",
             "SourceIpPostalCode", "SourceIpLatitude",
             "SourceIpLongitude", "SourceIpMetroCode",
             "SourceIpAreaCode", "HttpRequest",
             "HttpReferrer", "HttpUserAgent",
             "HttpMethod", "HttpVersion",
             "HttpHost", "Custom Field 1",
             "Custom Field 2", "Custom Field 3",
             "Custom Field 4", "Custom Field 5"]


__INTELMQ_TX = {"SourcedFrom": None,  # IGNORE
                "FileTimeUtc": "source_time",
                "Botnet": None,  # IS USED
                "SourceIp": "source_ip",
                "SourcePort": "source_port",
                "SourceIpAsnNr": "source_asn",
                "TargetIp": "destination_ip",
                "TargetPort": "destination_port",
                "Payload": None,  # IGNORE
                "SourceIpCountryCode": "source_cc",
                "SourceIpRegion": None, # IGNORE
                "SourceIpCity": "source_city",
                "SourceIpPostalCode": None,  # IGNORE
                "SourceIpLatitude": "source_latitude",
                "SourceIpLongitude": "source_longitude",
                "SourceIpMetroCode": None,  # IGNORE
                "SourceIpAreaCode": None,  # IGNORE
                "HttpRequest": None,  # IGNORE
                "HttpReferrer": None,  # IGNORE
                "HttpUserAgent": "user_agent",
                "HttpMethod": None,   # IGNORE
                "HttpVersion": None,  # IGNORE
                "HttpHost": None,  # IGNORE
                "Custom Field 1": None,  # IGNORE
                "Custom Field 2": None,  # IGNORE
                "Custom Field 3": None,  # IGNORE
                "Custom Field 4": None,  # IGNORE
                "Custom Field 5": None}  # IGNORE

# added with:
# cat ~/dcu-mapping.tsv | cut -f2,3 | sed 's/\t/\\t/g;s/$/\\n"/g;s/^/"/g'
__THREAT_CODES = dict(map(lambda x: x.split("\t"), (
    "B106-Agent\tmalware\n"
    "B106-AgentBypass\tmalware\n"
    "B106-Ainslot\tbackdoor\n"
    "B106-Amighelo\tmalware\n"
    "B106-Ardamax\tmalware\n"
    "B106-Arhost\tmalware\n"
    "B106-Assasin\tbackdoor\n"
    "B106-AutInject\tbackdoor\n"
    "B106-Autoac\tbackdoor\n"
    "B106-Autorun\tmalware\n"
    "B106-Balidor\tmalware\n"
    "B106-Bancos\tbackdoor\n"
    "B106-Bandok\tbackdoor\n"
    "B106-Banker\tbackdoor\n"
    "B106-Banload\tbackdoor\n"
    "B106-Bariori\tbackdoor\n"
    "B106-Beastdoor\tbackdoor\n"
    "B106-Beaugrit\tbackdoor\n"
    "B106-Bexelets\tbackdoor\n"
    "B106-Bezigate\tbackdoor\n"
    "B106-Bifrose\tbackdoor\n"
    "B106-Binder\tvulnerable service\n"
    "B106-Bisar\tbackdoor\n"
    "B106-Bladabindi\tbackdoor\n"
    "B106-Blohi\tbackdoor\n"
    "B106-BrowserPassview\tvulnerable service\n"
    "B106-Cakl\tbackdoor\n"
    "B106-Cashback\tmalware\n"
    "B106-CB\tmalware\n"
    "B106-Ceatrg\tmalware\n"
    "B106-Cechip\tbackdoor\n"
    "B106-CeeInject\tmalware\n"
    "B106-Chir\tmalware\n"
    "B106-Chuchelo\tbackdoor\n"
    "B106-Comame\tbackdoor\n"
    "B106-Comisproc\tmalware\n"
    "B106-Comitsproc\tmalware\n"
    "B106-Comrerop\tbackdoor\n"
    "B106-Comroki\tbackdoor\n"
    "B106-Comsirig\tbackdoor\n"
    "B106-Coolvidoor\tbackdoor\n"
    "B106-Coremhead\tbackdoor\n"
    "B106-Crime\tbackdoor\n"
    "B106-Danglo\tmalware\n"
    "B106-Darkddoser\tbackdoor\n"
    "B106-Darkmoon\tbackdoor\n"
    "B106-Decay\tbackdoor\n"
    "B106-Defsel\tbackdoor\n"
    "B106-Delf\tbackdoor\n"
    "B106-DelfInject\tmalware\n"
    "B106-Delfsnif\tbackdoor\n"
    "B106-Dimegup\tbackdoor\n"
    "B106-Dokstormac\tbackdoor\n"
    "B106-Dooxud\tmalware\n"
    "B106-Dorkbot\tmalware\n"
    "B106-Dusvext\tmalware\n"
    "B106-Dynamer\tbackdoor\n"
    "B106-Effbee\tbackdoor\n"
    "B106-EyeStye\tbackdoor\n"
    "B106-Fareit\tmalware\n"
    "B106-Farfli\tbackdoor\n"
    "B106-Folyris\tmalware\n"
    "B106-Frosparf\tbackdoor\n"
    "B106-Fynloski\tmalware\n"
    "B106-Gamarue\tmalware\n"
    "B106-Gaobot\tbotnet drone\n"
    "B106-Geratid\tbotnet drone\n"
    "B106-Gernidru\tbackdoor\n"
    "B106-Geycript\tmalware\n"
    "B106-Gratem\tbackdoor\n"
    "B106-GSpot\tbackdoor\n"
    "B106-Habbo\tbackdoor\n"
    "B106-Hamweq\tbotnet drone\n"
    "B106-Hanictik\tbackdoor\n"
    "B106-Hiderun\tmalware\n"
    "B106-HistBoader\tbackdoor\n"
    "B106-Horsamaz\tbackdoor\n"
    "B106-Hoygunver\tbackdoor\n"
    "B106-Hupigon\tbackdoor\n"
    "B106-Inject\tbackdoor\n"
    "B106-Injector\tbackdoor\n"
    "B106-IRCbot\tbackdoor\n"
    "B106-Ircbrute\tbackdoor\n"
    "B106-Itsproc\tbackdoor\n"
    "B106-Jenxcus\tbackdoor\n"
    "B106-Keygen\tvulnerable service\n"
    "B106-Keylogger\tbackdoor\n"
    "B106-Kilim\tbackdoor\n"
    "B106-KKmaka\tmalware\n"
    "B106-Klovbot\tbackdoor\n"
    "B106-Knowlog\tmalware\n"
    "B106-Ldpinch\tbackdoor\n"
    "B106-Lenc\tbackdoor\n"
    "B106-Leodon\tbackdoor\n"
    "B106-Levitiang\tmalware\n"
    "B106-Lybsus\tbackdoor\n"
    "B106-Lypsacop\tbackdoor\n"
    "B106-Mafod\tbackdoor\n"
    "B106-Malagent\tbackdoor\n"
    "B106-Malex\tbackdoor\n"
    "B106-Meredrop\tbackdoor\n"
    "B106-Mielit\tbackdoor\n"
    "B106-Misbot\tbackdoor\n"
    "B106-Mobibez\tbackdoor\n"
    "B106-Mosripe\tmalware\n"
    "B106-Mosucker\tbackdoor\n"
    "B106-Msposer\tbackdoor\n"
    "B106-MULTI\tmalware\n"
    "B106-Napolar\tmalware\n"
    "B106-Naprat\tbackdoor\n"
    "B106-Nayrabot\tmalware\n"
    "B106-Necast\tbackdoor\n"
    "B106-Neeris\tmalware\n"
    "B106-Nemim\tbackdoor\n"
    "B106-Neop\tbackdoor\n"
    "B106-Neshta\tmalware\n"
    "B106-Netbot\tbotnet drone\n"
    "B106-NetWiredRC\tbackdoor\n"
    "B106-Neurevt\tbackdoor\n"
    "B106-Nitol\tbackdoor\n"
    "B106-Noancooe\tbackdoor\n"
    "B106-Nosrawec\tbackdoor\n"
    "B106-Nuqel\tmalware\n"
    "B106-Nusump\tbackdoor\n"
    "B106-Obfuscator\tmalware\n"
    "B106-Otran\tbackdoor\n"
    "B106-Parama\tbackdoor\n"
    "B106-Parite\tmalware\n"
    "B106-PcClient\tbackdoor\n"
    "B106-Pdfjsc\tmalware\n"
    "B106-Poison\tbackdoor\n"
    "B106-Poisonivy\tbackdoor\n"
    "B106-Pontoeb\tbackdoor\n"
    "B106-Popiidor\tbackdoor\n"
    "B106-PossibleMalware\tmalware\n"
    "B106-Prorat\tbackdoor\n"
    "B106-Prosti\tbackdoor\n"
    "B106-Protos\tbackdoor\n"
    "B106-Pushbot\tbackdoor\n"
    "B106-Ramnit\tbackdoor\n"
    "B106-Ranos\tbackdoor\n"
    "B106-Rbot\tbackdoor\n"
    "B106-Rebhip\tmalware\n"
    "B106-Remhead\tbackdoor\n"
    "B106-Rimod\tbackdoor\n"
    "B106-Ritros\tmalware\n"
    "B106-Runner\tbackdoor\n"
    "B106-Sality\tmalware\n"
    "B106-Scar\tmalware\n"
    "B106-Sdbot\tbackdoor\n"
    "B106-Sharke\tbackdoor\n"
    "B106-Silby\tbackdoor\n"
    "B106-SillyShareCopy\tmalware\n"
    "B106-Sisproc\tbackdoor\n"
    "B106-Sisron\tbackdoor\n"
    "B106-Skypams\tbackdoor\n"
    "B106-Small\tmalware\n"
    "B106-Smpdoss\tmalware\n"
    "B106-Sormoeck\tbackdoor\n"
    "B106-Splori\tbackdoor\n"
    "B106-Spybot\tbackdoor\n"
    "B106-Squida\tmalware\n"
    "B106-SSonce\tbackdoor\n"
    "B106-Sulunch\tmalware\n"
    "B106-Swisyn\tbackdoor\n"
    "B106-Swrort\tbackdoor\n"
    "B106-SynFlood\tbackdoor\n"
    "B106-Tapazom\tbackdoor\n"
    "B106-Tawsebot\tmalware\n"
    "B106-Tearspear\tbackdoor\n"
    "B106-Tendrit\tmalware\n"
    "B106-Tenpeq\tbackdoor\n"
    "B106-Tobfy\transomware\n"
    "B106-Tocofob\tbackdoor\n"
    "B106-Toobtox\tbackdoor\n"
    "B106-Tumpadex\tmalware\n"
    "B106-Turkojan\tbackdoor\n"
    "B106-Twores\tbackdoor\n"
    "B106-Vahodon\tvulnerable service\n"
    "B106-Vake\tbackdoor\n"
    "B106-VB\tbackdoor\n"
    "B106-Vbcrypt\tmalware\n"
    "B106-Vbinder\tmalware\n"
    "B106-VBInject\tmalware\n"
    "B106-Vburses\tbackdoor\n"
    "B106-Vharke\tbackdoor\n"
    "B106-Vinject\tbackdoor\n"
    "B106-Virut\tbackdoor\n"
    "B106-Vobfus\tmalware\n"
    "B106-Vonriamt\tmalware\n"
    "B106-Vtub\tmalware\n"
    "B106-Weenkay\tbackdoor\n"
    "B106-Wervik\tmalware\n"
    "B106-Xtrat\tbackdoor\n"
    "B106-Xyligan\tbackdoor\n"
    "B106-Yemrok\tbackdoor\n"
    "B106-Zacusca\tbackdoor\n"
    "B106-Zbot\tbackdoor\n"
    "B106-Zegost\tbackdoor\n"
    "B58-CODE1\tbotnet drone\n"
    "B58-DGA1\tbotnet drone\n"
    "B58-NOTC\tbotnet drone\n"
    "B58\tmalware\n"
    "B58-CHTOZ\tmalware\n"
    "B58-CRSH\tmalware\n"
    "B58-DGA2\tmalware\n"
    "B58-DNS\tmalware\n"
    "B58-XPLT\tmalware configuration\n"
    "B93-CONFIG\tmalware configuration\n"
    "B93-HD\tmalware configuration\n"
    "B93-PLUGINS\tmalware configuration\n"
    "B54-BASE\tblacklist\n"
    "B54-CONFIG\tmalware configuration\n"
    "B54-CONFIG\tmalware configuration\n"
    "B54-INIT\tmalware\n"
    "B54-OLD\tblacklist\n"
    "B54-CODE 1\tblacklist\n"
    "B54-CODE 1\tblacklist\n"
    "B54-DNS\tblacklist\n"
    "Conficker\tmalware\n"
    "B157-N3\tmalware\n"
    "B157-O3\tmalwarew\n"
    "B157-R0\tmalware\n"
    "B157-R1\tmalware\n"
    "B157-RL\tc&c\n"
    "B157\tbackdoor\n"
    "B157-DGA\tbackdoor\n"
    "Rustock\tbotnet drone\n"
    "B68-1-32\tbotnet drone\n"
    "B68-1-64\tbotnet drone\n"
    "B68-2-32\tbotnet drone\n"
    "B68-2-64\tbotnet drone\n"
    "B68-DNS\tblacklist\n"
    "B68-TCP\tblacklist\n"
    "B68\tbotnet drone\n"
    "B68-2-64\tbotnet drone\n"
    "Waledac\tbotnet drone\n"
    "zbot\tmalware\n"
    "B75-S1\tbotnet drone\n"
    "B75-S12\tbotnet drone\n"
    "B75-S2\tbotnet drone"
).split("\n")))

def convert_windows_timestamp(windows_ts):
    """Convert a windows file utc timestamp to a datetime object"""
    us = int(windows_ts)/10
    dt = datetime(1601, 1, 1, tzinfo=tzutc()) + timedelta(microseconds=us)
    return dt


def dcu_headers():
    """Preferred way of retrieving the dcu format"""
    return __HEADERS


def convert_threatcode_to_type(threat_code):
    """Converts threat code to IntelMQ type"""
    return __THREAT_CODES.get(threat_code, "unknown")

def convert_dcu_fields(fields):
    """Converts the given dict of microsoft dcu fields to new fields"""
    converted_fields = []
    for key, value in fields.items():
        converted_key = __INTELMQ_TX.get(key)
        converted_value = value

        if key == "Botnet":
            converted_value = convert_threatcode_to_type(value)
            converted_key = "type"

        if key == "SourceIpAsnNr":
            converted_value = re.match("([Aa][Ss])?([0-9]+)", value).group(2)

        if key == "FileTimeUtc":
            converted_value = str(convert_windows_timestamp(value))

        if converted_key and converted_value:
            converted_fields.append((converted_key, converted_value))

            if key == "Botnet":
                # FIXME: what do we do with the dcu threat code? At the moment just 
                # writing it into malware field, so maybe an expert can do something with that
                # Another mapping table? Also it isn't conforming to the ontology...
                converted_fields.append(("malware", value)) 
                                                            

    return dict(converted_fields)
