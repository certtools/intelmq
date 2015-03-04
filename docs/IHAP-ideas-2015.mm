<map version="1.0.0">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node COLOR="#000000" CREATED="1421842773366" ID="ID_47318868" MODIFIED="1421849244024" TEXT="IHAP / intelmq">
<font NAME="SansSerif" SIZE="20"/>
<hook NAME="accessories/plugins/AutomaticLayout.properties"/>
<node COLOR="#0033ff" CREATED="1421842798019" ID="ID_659195387" MODIFIED="1421842998121" POSITION="right" TEXT="Frontend">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421842998835" ID="ID_57350885" MODIFIED="1421843012816" TEXT="Fetching of data">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421843371655" ID="ID_1888032244" MODIFIED="1421843437857" TEXT="generic RTIR fetcher">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="yes"/>
<node COLOR="#111111" CREATED="1423578234843" ID="ID_966259536" MODIFIED="1423578248067" TEXT="add a field for RTIR ticket id and pass it through the network"/>
</node>
<node COLOR="#990000" CREATED="1421843383614" ID="ID_443723107" MODIFIED="1421843394217" TEXT="generic IMAP folder fetcher">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1421843398046" ID="ID_557246318" MODIFIED="1421843404610" TEXT="generic url fetcher">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1421843407798" ID="ID_1825399408" MODIFIED="1421843413387" TEXT="generic xmpp fetcher">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421843414118" ID="ID_136029509" MODIFIED="1421843419627" TEXT="SIE fetcher">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421843013124" ID="ID_507757925" MODIFIED="1421843030696" TEXT="Parsing">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421843497538" ID="ID_1721781218" MODIFIED="1421843507000" TEXT="csv parser &amp; mapper">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1421843508123" ID="ID_1724602800" MODIFIED="1421843553294" TEXT="unzipper">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#990000" CREATED="1421843554577" ID="ID_1386909559" MODIFIED="1421843563630" TEXT="PGP decryptor">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421843564345" ID="ID_1829025511" MODIFIED="1421843564345" TEXT="">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421843944781" ID="ID_1835838888" MODIFIED="1421843947154" TEXT="Normalise">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421843953732" ID="ID_723649375" MODIFIED="1421843959938" TEXT="f.ex. all times to UTC">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421844003603" ID="ID_1361633218" MODIFIED="1421844010867" TEXT="other normalisation steps?">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421843053337" ID="ID_77268250" MODIFIED="1421843059542" POSITION="right" TEXT="Middle part">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421843060193" ID="ID_858273240" MODIFIED="1421929810247" TEXT="Sanity checks">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="yes"/>
<node COLOR="#990000" CREATED="1421843652999" ID="ID_425658834" MODIFIED="1421843661075" TEXT="Syntactic checks">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421843666438" ID="ID_402106786" MODIFIED="1421843669572" TEXT="timestamps"/>
<node COLOR="#111111" CREATED="1421843687149" ID="ID_1210845080" MODIFIED="1421843690594" TEXT="IP address"/>
<node COLOR="#111111" CREATED="1421843693213" ID="ID_587783317" MODIFIED="1421843696298" TEXT="ASN "/>
</node>
<node COLOR="#990000" CREATED="1421843670552" ID="ID_624309513" MODIFIED="1421843680562" TEXT="semantic checks">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421843696836" ID="ID_1192614336" MODIFIED="1421843711889" TEXT="country code check"/>
<node COLOR="#111111" CREATED="1421843721860" ID="ID_1084017752" MODIFIED="1421843723404" TEXT="ASN"/>
<node COLOR="#111111" CREATED="1421843724147" ID="ID_1426140977" MODIFIED="1421843726009" TEXT="IP address"/>
<node COLOR="#111111" CREATED="1421843726875" ID="ID_1078259684" MODIFIED="1421843730761" TEXT="timestamp is realistic">
<node COLOR="#111111" CREATED="1421845811184" ID="ID_940653163" MODIFIED="1421845813422" TEXT="too old?"/>
<node COLOR="#111111" CREATED="1421845814064" ID="ID_1248421599" MODIFIED="1421845816942" TEXT="in the future?"/>
</node>
</node>
<node COLOR="#990000" CREATED="1421843831417" ID="ID_1537732032" MODIFIED="1421843843392" TEXT="Document all checks (EBNF,regexp,...)">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421843063921" ID="ID_1948389043" MODIFIED="1421843068262" TEXT="Data enrichment">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421843895790" ID="ID_1039438265" MODIFIED="1421843899307" TEXT="IP2ASN">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421844467460" ID="ID_866664689" MODIFIED="1421844469257" TEXT="Qualle"/>
<node COLOR="#111111" CREATED="1421844472700" ID="ID_1723171803" MODIFIED="1421844477011" TEXT="Cymru">
<icon BUILTIN="button_ok"/>
</node>
</node>
<node COLOR="#990000" CREATED="1421843899710" ID="ID_1768789146" MODIFIED="1421843902667" TEXT="contact email">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421843903118" ID="ID_1226173695" MODIFIED="1421843918827" TEXT="country code">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421843919437" ID="ID_330052964" MODIFIED="1421929943529" TEXT="maxmind - geoip">
<icon BUILTIN="button_ok"/>
<node COLOR="#111111" CREATED="1421929962725" ID="ID_359738246" MODIFIED="1421929968245" TEXT="auto-update"/>
</node>
<node COLOR="#111111" CREATED="1421843922541" ID="ID_456013628" MODIFIED="1421844461439" TEXT="cymru / RIPE">
<icon BUILTIN="button_ok"/>
</node>
</node>
</node>
<node COLOR="#00b439" CREATED="1421843868903" ID="ID_470155521" MODIFIED="1421930003841" TEXT="Verification">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="help"/>
<node COLOR="#990000" CREATED="1421843871751" ID="ID_1043272594" MODIFIED="1421843886471" TEXT="f. ex. is this really an open recursor?">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421843886934" ID="ID_992218467" MODIFIED="1421843890244" TEXT="verify if possible!">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421843079672" ID="ID_520647116" MODIFIED="1421843081501" TEXT="Filtering">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421844059584" ID="ID_755243145" MODIFIED="1421844064430" TEXT="constituency check">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421844052113" ID="ID_796491376" MODIFIED="1421844070294" TEXT="country code == AT ?">
<font NAME="SansSerif" SIZE="12"/>
</node>
<node COLOR="#111111" CREATED="1421844072937" ID="ID_1428479044" MODIFIED="1421844079726" TEXT=".at domain?"/>
<node COLOR="#111111" CREATED="1421844080976" ID="ID_698350738" MODIFIED="1421844081798" TEXT="..."/>
</node>
<node COLOR="#990000" CREATED="1421844087752" ID="ID_863372744" MODIFIED="1421844099397" TEXT="taxonomy == test ? --&gt; filter out">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421843109256" ID="ID_137313006" MODIFIED="1421844446994" TEXT="VIP support">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="help"/>
<node COLOR="#990000" CREATED="1421844380895" ID="ID_259306474" MODIFIED="1421844429787" TEXT="What is a VIP?">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421844333360" ID="ID_1019500048" MODIFIED="1421844436554" TEXT="DB of VIP keys (ASNs, cidr, domains)">
<font NAME="SansSerif" SIZE="12"/>
</node>
</node>
<node COLOR="#990000" CREATED="1421844402365" ID="ID_941423118" MODIFIED="1421844418485" TEXT="What happens when a VIP match happens?">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421845052137" ID="ID_1470451793" MODIFIED="1421845060686" TEXT="How do they want to be notified?">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421845200524" ID="ID_406799882" MODIFIED="1421845287117" TEXT="Variant 1: alert CERT team">
<icon BUILTIN="yes"/>
</node>
<node COLOR="#111111" CREATED="1421845206547" ID="ID_1554539342" MODIFIED="1421845229265" TEXT="Variant 2: alert VIP team directly"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421843262307" ID="ID_1980425040" MODIFIED="1421846140390" POSITION="right" TEXT="Eventdb / ES">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421845725387" ID="ID_407764779" MODIFIED="1421845728241" TEXT="no filtering">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421845730315" ID="ID_236234825" MODIFIED="1421845882353" TEXT="every log record gets stored no matter what">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421845895470" ID="ID_671289394" MODIFIED="1421845901931" TEXT="maybe filter out &quot;test&quot; status">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421846023874" ID="ID_975826125" MODIFIED="1421846118861" TEXT="&quot;handler user interface&quot; accesses the Eventdb, groups by email,not_seen addr;&#xa;update eventdb set status = seen where ...">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421846230082" ID="ID_1726574987" MODIFIED="1421846244618" TEXT="Functionality 1: be a queue between the real time part and the Backend logic">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421846245570" ID="ID_414691201" MODIFIED="1421846264720" TEXT="Functionality 2: hold the data for later offline statistics, queries etc">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421846483227" ID="ID_1446259490" MODIFIED="1421846484336" TEXT="DB">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421846484931" ID="ID_39207254" MODIFIED="1421846504151" TEXT="Postgresql">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="full-1"/>
<icon BUILTIN="yes"/>
<node COLOR="#111111" CREATED="1421847225626" ID="ID_538800582" MODIFIED="1421847230513" TEXT="on it&apos;s own instance / DB"/>
</node>
<node COLOR="#990000" CREATED="1421846488465" ID="ID_251338328" MODIFIED="1421846496770" TEXT="ES">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="full-2"/>
<node COLOR="#111111" CREATED="1421847237794" ID="ID_93571294" MODIFIED="1421847245699" TEXT="separate VM">
<icon BUILTIN="button_ok"/>
</node>
</node>
<node COLOR="#990000" CREATED="1421846562752" ID="ID_1195512401" MODIFIED="1421847262111" TEXT="Portal for clients / constituency">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="full-3"/>
<icon BUILTIN="help"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421842809156" ID="ID_910567712" MODIFIED="1421846269727" POSITION="right" TEXT="Backend Logic">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421842838304" ID="ID_728557641" MODIFIED="1421843023343" TEXT="Notifications">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421842840713" ID="ID_1405523901" MODIFIED="1421845311099" TEXT="via RTIR">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421844622263" ID="ID_3426867" MODIFIED="1421844775939" TEXT="Variant 1: mail to RTIR">
<font NAME="SansSerif" SIZE="12"/>
</node>
<node COLOR="#111111" CREATED="1421844631767" ID="ID_20285815" MODIFIED="1423577726738">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Variant 2: scripts for eyeballing go to eventDB
    </p>
    <p>
      and fetch the daily data. RTIR stays &quot;mailer&quot;.
    </p>
    <p>
      
    </p>
    <p>
      see document &quot;handler user interface&quot;
    </p>
  </body>
</html>
</richcontent>
<arrowlink DESTINATION="ID_1522158750" ENDARROW="Default" ENDINCLINATION="307;0;" ID="Arrow_ID_1730775176" STARTARROW="None" STARTINCLINATION="307;0;"/>
<font NAME="SansSerif" SIZE="12"/>
<icon BUILTIN="yes"/>
</node>
</node>
<node COLOR="#990000" CREATED="1421844788785" ID="ID_1558324152" MODIFIED="1421845455919" TEXT="direct">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="help"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421848178531" ID="ID_1522158750" MODIFIED="1421848533933" TEXT="Handler User Interface">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="yes"/>
<node COLOR="#990000" CREATED="1421848544336" ID="ID_32543135" MODIFIED="1421848545583" TEXT="TBD">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421845592527" ID="ID_1167066192" MODIFIED="1421845599045" TEXT="Squelcher">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421845651885" ID="ID_447895522" MODIFIED="1421845661379" TEXT="support type, feed, taxonomy">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421843131407" ID="ID_1976194356" MODIFIED="1421843134796" POSITION="right" TEXT="Supporting data">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421843135167" ID="ID_1993419286" MODIFIED="1421843136844" TEXT="contactdb">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421845472291" ID="ID_1586978721" MODIFIED="1421845543751" TEXT="internal">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="yes"/>
<node COLOR="#111111" CREATED="1421845550017" ID="ID_519064503" MODIFIED="1421845554530" TEXT="AScontacts"/>
</node>
<node COLOR="#990000" CREATED="1421930621592" ID="ID_385335069" MODIFIED="1421930635983" TEXT="write down the API">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="yes"/>
</node>
<node COLOR="#990000" CREATED="1421845475043" ID="ID_1960925760" MODIFIED="1421845480699" TEXT="RIPE lookups">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421843137790" ID="ID_1013623429" MODIFIED="1421843145252" TEXT="qualle / BGP">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421845273434" ID="ID_1405941457" MODIFIED="1421930588596" TEXT="maxmind">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
</node>
<node COLOR="#00b439" CREATED="1421843145607" ID="ID_1478669150" MODIFIED="1421843207903" TEXT="cymru lookups">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421842870975" ID="ID_957488191" MODIFIED="1421842927058" POSITION="right" TEXT="Testing">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421847873317" ID="ID_1520942509" MODIFIED="1421847880164" TEXT="define test cases for every bot">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421847881212" ID="ID_424837519" MODIFIED="1421847893844" TEXT="automatic regression testing mechanisms">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421847150509" ID="ID_1723925132" MODIFIED="1421847154147" POSITION="right" TEXT="Security considerations">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421847154548" ID="ID_944579299" MODIFIED="1421848009439" TEXT="don&apos;t have long running bots that talk to the external Internet. Terminate them after fetching">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<icon BUILTIN="help"/>
</node>
<node COLOR="#00b439" CREATED="1421847793767" ID="ID_1363007715" MODIFIED="1421847807507" TEXT="Extreme syntax validations, no pardon whatsoever">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421847808527" ID="ID_1381812703" MODIFIED="1421847822517" TEXT="If some input does not match a regexp/EBNF, ignore it and log">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421847830478" ID="ID_287556463" MODIFIED="1421847843741" TEXT="Limits on inputs">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421847845485" ID="ID_133549361" MODIFIED="1421847851804" TEXT="if limit is exceeded, log">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421847997888" ID="ID_894417288" MODIFIED="1421848002223" TEXT="timeouts">
<font NAME="SansSerif" SIZE="14"/>
<icon BUILTIN="button_ok"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421847858909" ID="ID_1011715631" MODIFIED="1421847862301" POSITION="right" TEXT="Alerting / Monitoring">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
</node>
<node COLOR="#0033ff" CREATED="1421842937389" ID="ID_1902632655" MODIFIED="1421842941704" POSITION="left" TEXT="Data-sharing">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
</node>
<node COLOR="#0033ff" CREATED="1421842943086" ID="ID_654494863" MODIFIED="1421842972105" POSITION="left" TEXT="Coordination w. other teams">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421848033193" ID="ID_331455420" MODIFIED="1421848039383" TEXT="CNCS.gov.pt">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421848053311" ID="ID_925916220" MODIFIED="1421929071857" TEXT="company">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421848068431" ID="ID_1554813459" MODIFIED="1421848072221" TEXT="ENISA">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421842846648" ID="ID_1158101577" MODIFIED="1421929046317" POSITION="left" TEXT="Persons / Know-how">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421842867624" ID="ID_1255132216" MODIFIED="1421929037949" TEXT="Who does what?">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421848119525" ID="ID_1185766708" MODIFIED="1421848160983" TEXT="Aaron">
<font NAME="SansSerif" SIZE="14"/>
<node COLOR="#111111" CREATED="1421848135277" ID="ID_1372847014" MODIFIED="1421848157543" TEXT="write work packages / tasks"/>
</node>
<node COLOR="#990000" CREATED="1421848094070" ID="ID_1907107232" MODIFIED="1421848095557" TEXT="mib">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421848096429" ID="ID_620825712" MODIFIED="1421848098612" TEXT="stelen">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421848099126" ID="ID_714156185" MODIFIED="1421848100628" TEXT="Bernhard">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421842883663" ID="ID_1361363666" MODIFIED="1421842927059" POSITION="left" TEXT="Migration path">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421848417267" ID="ID_1822644944" MODIFIED="1421848420534" TEXT="Pilot">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421848399108" ID="ID_1158320100" MODIFIED="1421848423825" TEXT="n6 v2 via intelmq">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421848425828" ID="ID_1882663559" MODIFIED="1421848429986" TEXT="send via RTIR">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421929240448" ID="ID_652253656" MODIFIED="1421929245593" TEXT="Postgresql">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
<node COLOR="#00b439" CREATED="1421848435691" ID="ID_1673669154" MODIFIED="1421848443673" TEXT="Step by step each feed">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
<node COLOR="#990000" CREATED="1421848445731" ID="ID_291961275" MODIFIED="1421848449329" TEXT="shadowserver">
<font NAME="SansSerif" SIZE="14"/>
</node>
<node COLOR="#990000" CREATED="1421848449979" ID="ID_1621383215" MODIFIED="1421848452381" TEXT="....">
<font NAME="SansSerif" SIZE="14"/>
</node>
</node>
</node>
<node COLOR="#0033ff" CREATED="1421842887638" ID="ID_1777305405" MODIFIED="1421842927060" POSITION="left" TEXT="Security policies">
<edge STYLE="sharp_bezier" WIDTH="8"/>
<font NAME="SansSerif" SIZE="18"/>
<node COLOR="#00b439" CREATED="1421929267556" ID="ID_14880875" MODIFIED="1421929273365" TEXT="define">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
<node COLOR="#00b439" CREATED="1421929273972" ID="ID_1471566839" MODIFIED="1421929278237" TEXT="audit">
<edge STYLE="bezier" WIDTH="thin"/>
<font NAME="SansSerif" SIZE="16"/>
</node>
</node>
</node>
</map>
