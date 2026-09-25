# BPH Sanctions & Enforcement Timeline

**Version:** 1.3
**Last Updated:** 2026-09-25
**Maintainer:** CrimsonVector Research

---

> **Purpose:** Chronological record of all sanctions, law enforcement operations, provider lifecycle events, and evasion responses related to Bulletproof Hosting (BPH) and Threat Activity Enabler (TAE) networks. Entries are in reverse-chronological order (newest first) for rapid analyst reference.

> **Legend:**
> - **Sanctions** -- Designation by OFAC, EU, UK, AU, NZ, or other authority
> - **LE Operation** -- Law enforcement seizure, takedown, or arrest
> - **Private-sector disruption** -- Takedown led by a company (civil legal action, platform enforcement) rather than law enforcement
> - **Provider Event** -- Incorporation, registration, dissolution, or transfer of hosting entity or AS resource
> - **Evasion** -- Rebranding, prefix migration, front-company creation, or other sanctions/LE circumvention
> - **Intelligence** -- Publication of key research, reports, or disclosures; also threat-actor events with no enforcement component

> **2026-09-25 audit.** Every entry was re-checked against primary or vendor sources. Corrected entries carry the corrected facts directly; material corrections are called out in italics. Source IDs refer to `sources/SOURCE_INDEX.md`; entries added in this revision also link their sources inline with a reliability grade (A-E). "Headline-level" marks items whose detail was not read in full.

---

## 2026

**2026-09-22** | **Private-sector disruption + LE Operation** | **Microsoft Takes Down EvilTokens Device-Code PhaaS; Two Arrested in the UK**
> Microsoft disrupted "EvilTokens", a device-code phishing-as-a-service kit tied to about 12,000 Microsoft account compromises; UK police arrested two people. Phishing infrastructure enabler; moderate BPH relevance. [Sources: [Microsoft](https://www.microsoft.com/en-us/security/blog/2026/09/22/unmasking-eviltokens-getting-to-the-root-of-device-code-phishing/) (B); [The Record](https://therecord.media/two-arrested-in-uk-after-microsoft-takedown-eviltokens) (C)] *Headline-level.*

**2026-09-20** | **Intelligence** | **ShinyHunters Hijacks Cl0p's Data-Leak Site**
> ShinyHunters hacked and took over Cl0p's dark-web leak site (reported 20-22 Sept) and threatened to extort the ransomware gang. Relevant to Cl0p infrastructure tracking -- see [`CL0P_HOSTZEALOT_REUSE.md`](CL0P_HOSTZEALOT_REUSE.md). [Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/shinyhunters-hacks-clop-leak-site-threatens-to-extort-ransomware-gang/) (C); [The Record](https://therecord.media/shinyhunters-clop-cyberattack-website) (C)]

**~2026-09-15** | **LE Operation** | **NightmareStresser DDoS-for-Hire Domains Seized (Operation PowerOFF)**
> Seizure warrants from the District of Alaska (FBI Anchorage with the RCMP) took down nightmare-stresser[.]com and nightmarestresser[.]org, a booter used in hundreds of thousands of DDoS attacks since 2022. Archived snapshots show the site fronted by **BlazingFast** DDoS protection -- a provider lead for this database. [Sources: [The Hacker News](https://thehackernews.com/2026/09/us-seizes-nightmarestresser-domains.html) (C); [Help Net Security](https://www.helpnetsecurity.com/2026/09/17/fbi-nightmarestresser-ddos-for-hire-service-seized/) (C)] *Date inferred from "Tuesday" wording.*

**2026-09-09** | **Sanctions + LE Operation** | **US Disrupts Xinbi Guarantee (Huione/Tudou Successor Marketplace)**
> OFAC designated Xinbi Guarantee and two affiliates while the DOJ Scam Center Strike Force and Secret Service seized its Telegram channels and two wallets (~$12M); $52.8M in USDT was frozen across 52 wallets with Elliptic's help. Elliptic calls Xinbi the second-largest illicit marketplace ever (~$30B since ~2022; Treasury cites $24B); Treasury says DPRK hackers and Prince Group entities used it. After the freeze Xinbi moved from USDT to USDD. The UK had designated Xinbi first, on 2026-03-26. [Sources: OFAC-XINBI-2026; [The Hacker News](https://thehackernews.com/2026/09/us-disrupts-xinbi-guarantee-scam.html) (C); [Chainalysis](https://www.chainalysis.com/blog/ofac-sanctions-xinbi-cybercriminal-crypto-marketplace/) (B)]

**2026-09-01** | **LE Operation** | **Sality P2P Botnet Disrupted**
> US (USAO C.D. Cal.), Bulgarian, Hungarian and Romanian authorities, with CrowdStrike and Shadowserver, sinkholed Sality's P2P networks (v3 and v4) by peer-list manipulation and seized payload domains (operation 2026-08-31; >15,000 infected machines). Sality modules included proxy services and DDoS. [Sources: [The Hacker News](https://thehackernews.com/2026/09/authorities-turn-salitys-p2p-network.html) (C); [CrowdStrike](https://www.crowdstrike.com/en-us/blog/inside-sality-botnet-disruption-operation/) (B)]

**2026-08-26** | **LE Operation** | **DOJ/FBI Seize QScan and QTRouter (PRC "QTFY" Proxy/ORB Platform)**
> A court-authorised seizure took the domains hard-coded into QScan (an IoT scanner and infector) and QTRouter (an obfuscation network) operated by the "QTFY" technical-quartermaster group, whose staff work for Nanjing Xinjiuwei Network Technology Co. and whose customers include the MSS and PLA. QTRouter chained compromised IoT devices, **bulk-bought Chinese commercial proxy subscriptions and leased VPSs** through Clash; reported victims include NASA, the Federal Reserve, DOE, DOJ, HHS, NIH and the US Senate. Lumen Black Lotus Labs tracked it as "Fast Labyrinth"/"QTProxy". Added to the database as a T1 anonymization/proxy enabler. [Sources: DOJ-QTFY-2026; LUMEN-QTFY-2026]

**2026-08-26** | **Sanctions** | **US Designates Autistici/Inventati as a Specially Designated Global Terrorist (Outlier)**
> The State Department designated the Italian hosting and email collective Autistici/Inventati under E.O. 13224, citing hosting, encrypted email and anonymity services for "far-left" groups (~16,000 mailboxes, 1,500 websites). The .org registry disabled autistici.org, PayPal froze its account, and the collective announced it would shut down. A contested counter-terrorism designation of a hosting provider -- a legal and political outlier, not criminal BPH. [Sources: [State Department](https://www.state.gov/releases/office-of-the-spokesperson/2026/08/designation-of-autistici-inventati-as-a-specially-designated-global-terrorist/) (A); [The Record](https://therecord.media/autistici-inventati-shuts-down-after-us-terrorist-designation) (C)]

**~2026-08-25** | **Sanctions** | **OFAC "Operation Economic Outcast" (Iran)**
> About 60 Iran-linked individuals, entities and vessels, including MOIS-linked cyber actors (Mabna Institute members), with Treasury flagging digital-asset rails; Rewards for Justice offered up to $10M. Followed a DOJ superseding indictment of 17 Iranians (~2026-08-19). [Source: [The Hacker News](https://thehackernews.com/2026/08/us-sanctions-iran-linked-hackers-behind.html) (C)] *Date inferred from reporting.*

**2026-08-19** | **Intelligence** | **Intel 471 -- "A New Era of Bulletproof Hosting Providers Emerge"**
> After action against the operators yalishanda (Media Land), ccweb and whost, roughly 80% of ~2,240 tracked yalishanda customer domains stayed online into June 2026 -- some by moving to mainstream clouds -- and demand shifted to new services: OtusCloud, reming's fast-flux proxy service and fluxy's "VIP FAST FLUX". [Source: INTEL471-BPH-2026]

**2026-08-12** | **Intelligence** | **Team Cymru Cl0p Retrospective -- HostZealot Most-Used Provider**
> "Cl0p 'Til You Drop -- 6 Years, 10 Campaigns, 8 Zero-Days" finds HostZealot the most frequently observed provider across Cl0p's campaigns (four of nine with infrastructure data: Accellion, GoAnywhere, MOVEit, Cleo); ColoCrossing, Datacampus, Datahome, Ghostnet and OVH recur across 3+ campaigns; about two-thirds of observed ASNs (53 of 79) appear in a single campaign. Independently reproduced from CISA, Mandiant, Lumen and Huntress IOC lists in this repository's analysis. [Sources: TEAMCYMRU-CL0P-2026; see `CL0P_HOSTZEALOT_REUSE.md`]

**2026-08-12** | **Sanctions (policy)** | **Presidential Memorandum on Transnational Cyber-Enabled Crime**
> "Expanding Capabilities to Combat Transnational Cyber-Enabled Crime" authorises vetted US "Participating Companies", under the National Coordination Center (DOJ/DHS co-executive directors), to conduct cyber surveillance and cyber effects operations against foreign cyber-enabled criminal organisations, subject to a $1M bond or escrow, operating procedures within 60 days and a report within 180 days. Builds on E.O. 14390; BPH/TAE operators are potentially in scope. [Source: WH-PM-2026-08-12]

**2026-08-08** | **Sanctions** | **New Zealand Designates Media Land's Volosovik**
> New Zealand's Russia Sanctions Act action against 33 individuals and entities includes Aleksandr Volosovik (Media Land), CARR/Z-Pentest figures Pankratova and Degtyarenko, and a GRU Unit 29155 officer. [Source: NZ-MFAT-RUSSIA-2026-08]

**2026-08-07** | **Sanctions** | **OFAC -- Iranian Exchanges Shelbit and Aban Tether (sb0598)**
> Designated for funding Iran's IRGC; Aban Tether had processed transactions with Nobitex, Wallex, Bitpin and Ramzinex. Follows OFAC's 2026-07-16 addition of four Central Bank of Iran crypto wallets to the SDN list (Tether froze ~$131M). [Sources: [Treasury sb0598](https://home.treasury.gov/news/press-releases/sb0598) (A); [CoinDesk](https://www.coindesk.com/policy/2026/08/07/u-s-widens-iran-crypto-crackdown-with-sanctions-on-two-exchanges) (C)]

**2026-07-23** | **Sanctions** | **EU 21st Russia Package -- Third-Country Crypto Tool**
> 218 listings; transaction bans on 11 crypto-asset service providers (effective 2026-08-23); a new legal tool for full bans on third-country crypto-asset services; further A7-network listings. Extends the 20th package's category approach to corridors outside Russia. [Source: EU-21ST-PACKAGE]

**2026-07-21** | **LE Operation** | **Kratos Phishing-as-a-Service Dismantled**
> US and German law enforcement took down the Kratos Microsoft 365 adversary-in-the-middle PhaaS kit (reported 2026-07-23). [Source: [The Hacker News](https://thehackernews.com/2026/07/police-dismantle-kratos-phishing-kit.html) (C)] *Headline-level.*

**2026-07-16** | **Intelligence** | **Hunt.io Eastern-Europe Infrastructure Report -- Proton66 / ShinyHunters**
> Hunt.io counted 3,900+ servers enabling threat activity across 302 Eastern European providers in three months, and linked Proton66 to exploitation of Oracle PeopleSoft zero-day CVE-2026-35273 attributed to ShinyHunters. [Source: HUNTIO-EE-2026]

**2026-07-14** | **LE Operation** | **DOJ Unseals Media Land / ML.Cloud Indictment (Operation Riptide)**
> The Northern District of Ohio unsealed an indictment -- returned under seal on 2024-12-05 -- charging Alexander Alexandrovich Volosovik (43), Kirill Andreevich Zatolokin (34), and Yulia Vladimirovna Pankova (29), together with corporate defendants Medialand LLC and ML.Cloud LLC, with conspiracy to commit and aid computer fraud, wire fraud, and money-laundering conspiracy. DOJ's headline figure is **more than $62M in victim losses**; the release cites 42 US victim organisations across 21 states (the indictment enumerates 44, including one each in Canada and the UK). Medialand infrastructure operated out of China, Finland, the Netherlands, and the United States. Rewards for Justice offers up to $10M for information on foreign-government-linked associates or use. Part of Operation Riptide, an FBI campaign against cybercrime infrastructure (distinct from the EU sanctions of the previous day). [Source: DOJ-MEDIALAND-INDICTMENT]

**2026-07-13** | **Sanctions** | **EU + UK Cyber Sanctions the Same Day -- Media Land, ML.Cloud, Z-Pentest**
> Council Implementing Regulation (EU) 2026/1714 (cyber-attacks regime, Reg. 2019/796) adds **8 natural persons and 4 entities**: Media Land LLC, ML.Cloud, Z-Pentest and LLC Impuls; the persons include Aleksandr Volosovik, Vitaly Kovalev ("Stern"), Lumma developers Voronin and Gordienko, CARR's Pankratova and Degtyarenko, and Bashev (owner of Impuls, linked to GRU Unit 29155). The Council's "nine individuals" headline also counts Kasyanenko, listed the same day under the separate destabilising-activities regime -- this resolves the count discrepancy flagged in the previous version. The UK made **24 designations** the same day (14 under the Cyber regime, including Lumma-linked Voronin, Gordienko and Zhurkin, GRU officers, CARR figures and OOO Impuls, plus 10 Rybar individuals under the Russia regime); Media Land was already UK-listed (Nov 2025), so the July UK notice contains no Media Land entry. [Sources: EU-CYBER-2026-1714; OFSI-CYBER-2026-07]
>
> *Corrections: "GRU Unit 29155 members" overstated the EU listing (only Bashev and Impuls are linked); the "CYB0115-CYB0129" range spans 15 IDs and remains unverified.*

**2026-07-13** | **Sanctions** | **OFAC -- First VPN Service (1VPNS) + Rashevskyi + Silayev**
> OFAC designated First VPN Service (1VPNS), its 45-year-old Ukrainian administrator Dmytro Rashevskyi, and Belarusian cryptor seller Yegeniy Vladimirovich Silayev under E.O. 13694 as amended, in furtherance of E.O. 14390. 1VPNS had advertised on criminal forums since 2014, kept no logs and refused law-enforcement cooperation; Rashevskyi used false identities ("Maksim Sorin", "Roman Chabanenko") to procure infrastructure. Follows Operation Saffron (May 2026). The UK did not co-designate 1VPNS. [Source: OFAC-1VPNS]

**2026-07-02** | **LE Operation + Private-sector disruption** | **FBI Seizes NetNut Domains; Google Disrupts the Popa Botnet**
> The FBI seized hundreds of domains tied to NetNut -- a residential-proxy service operated by NASDAQ-listed Israeli firm Alarum Technologies (ALAR) -- with a seizure notice thanking Google, Lumen and Shadowserver. Google disabled accounts used for C2 of the associated Popa botnet (at least 2M hijacked smart TVs, streaming boxes and Android devices) and set Play Protect to disable apps carrying NetNut SDKs; GTIG observed 316 distinct threat clusters using suspected NetNut exit nodes in a single week of June 2026. Alarum disputes the allegations and paused traffic on the affected network; its shares fell 23.6% after hours. Popa was first flagged by QiAnXin XLab in March 2025 and tied to NetNut in June 2026 by Krebs and Qurium. Builds on Google's January 2026 IPIDEA disruption. [Sources: GTIG-NETNUT; KREBS-NETNUT; KREBS-POPA-2026; QURIUM-POPA-2026]
>
> *Corrections: IRS-CI involvement and a "~67% stock fall within a week" were not supported by any source and were removed. Notable as a TAE profile the taxonomy now models under proxy enablers: a listed Western company whose commercial proxy service sourced exit nodes from a botnet.*

**2026-06-24** | **LE Operation** | **Operation Endgame -- June 2026 Action Week (SocGholish / Amadey / StealC)**
> Europol announced (action week 15-19 June; SocGholish strand announced 18 June, NL-led) the disruption of the SocGholish, Amadey and StealC networks: 326 servers and 142 domains seized or disrupted, more than EUR 41M (~$47M) in crypto frozen, 27M credentials recovered and 14,971 infected WordPress sites cleaned. [Source: EUROPOL-ENDGAME-2026]

**2026-06-23** | **Sanctions + LE Operation** | **Prince Group / Huione Laundering Ecosystem (US Coordinated Action)**
> OFAC (sb0538) sanctioned 35 targets (9 individuals and 26 entities) tied to the Prince Group transnational criminal organisation, including front companies and scam-compound investors; second-in-command Hu Xiaowei had already been designated in October 2025 under the alias "Chen Xiao'er". DOJ announced the seizure of a cloud-computing account hosting backend infrastructure for Huione subsidiaries (FBI San Francisco, IRS-CI). FinCEN proposed amending its October 2025 Huione Group Section 311 final rule to cover Cambodia-based H-Pay Service PLC and "any successor entity" (Federal Register 2026-12794, published 25 June; still a proposal). FinCEN found at least $4B laundered through Huione. [Sources: OFAC-HUIONE-PRINCE; FINCEN-HPAY-2026]
>
> *Corrections: AUSTRAC's involvement was not found in any source; the "$98B inflows" figure is unverified.*

**2026-06-10** | **LE Operation** | **AudiA6 Crypto Cash-Out Service Dismantled**
> Europol, DOJ, the Secret Service and Georgian authorities took down AudiA6, a cash-out service for ransomware actors (~10,333 BTC processed); administrators Ruslan Tkachuk and Alexander Ledenev were arrested in Georgia. [Source: [The Hacker News](https://thehackernews.com/2026/06/europol-disrupts-audia6-crypto.html) (C)]

**2026-06-02** | **Sanctions** | **OFAC "Economic Fury" -- Iranian Cryptocurrency Exchanges**
> OFAC (sb0519) designated four Iranian exchanges -- Nobitex, Wallex, Bitpin and Ramzinex -- which together handled about $7.7B, roughly 78% of Iran's attributed 2025 crypto volume. Nobitex was designated under counterterrorism E.O. 13224 (material support to the IRGC) and E.O. 13902, together with four of its executives; the others under the Iran financial-sector authority. [Source: OFAC-IRAN-FURY]

**2026-06-01** | **Intelligence** | **Check Point -- WorkTitans Seizure Hit Iranian Operations**
> Check Point reported that three Iranian threat groups, including MuddyWater (MOIS), used WorkTitans/THE.Hosting infrastructure for core operations, so the May FIOD seizure likely affected Iranian cyber operations. [Source: CHECKPOINT-WORKTITANS-IRAN-2026]

**2026-05-28** | **LE Operation** | **Residential-Proxy Botnet Takedown (Press-Attributed to Asocks)**
> Dutch police (Politie) and NCSC-NL announced the takedown of a residential-proxy botnet of at least 17 million infected devices whose backend ran on more than 200 servers in the Netherlands; police seized a subset of those servers from a hosting provider, which then took the botnet offline. The authorities did not name the service; NL Times reported it was Asocks (asocks[.]com). The clearnet storefront reportedly stayed live. [Sources: NCSC-NL-ASOCKS; SILENTPUSH-CHINESEVPN]
>
> *Corrections: "~200 servers seized" -> a subset of 200+ backend servers; "~163 countries" was dropped (it is the SocksEscort figure).*

**2026-05-26** | **Sanctions** | **UK Designates Russian-Linked Crypto Exchanges (First Use of Reg. 17A)**
> The FCDO designated 18 targets under the Russia regime, including HTX (Huobi Global), Exmo Exchange Ltd, Rapira Group, Bitpapa IC FZC, Nueva Cryptologia (ABCEX) and Eurasian Savings Bank, plus Sergey Mendeleev (Garantex co-founder), Igor Gorin, Liran Cohen and Irina Akopyan. Several of these venues had been described in this repository as "active" Garantex successors. [Source: FCDO-UK-SANCTIONS-LIST; [gov.uk list](https://www.gov.uk/government/publications/list-of-russia-sanctions-designations-26-may-2026) (A)]

**2026-05-20** | **LE Operation** | **Operation Saffron -- First VPN (1VPNS) Dismantled**
> France and the Netherlands, with Europol and Eurojust, dismantled 1VPNS on 19-20 May: 33 servers taken down, 1vpns.com/.net/.org and onion domains seized, a suspected administrator arrested and thousands of users identified. FBI FLASH-20260521-001 published IOCs (~32 exit nodes in ~27 countries; used by at least 25 ransomware groups). [Source: EUROPOL-SAFFRON-2026]

**2026-05-18** | **LE Operation** | **FIOD Raid on THE.Hosting / WorkTitans B.V. (Stark Successor)**
> The Dutch FIOD raided data centres in Dronten and Schiphol-Rijk and searched businesses in Enschede and Almere, seizing 800+ servers plus laptops, phones and records from the Stark Industries successor network operating as THE.Hosting under WorkTitans B.V. Two men were arrested -- a 57-year-old from Amsterdam and a 39-year-old from The Hague -- for making economic resources available to EU-sanctioned entities; the press names them as WorkTitans owner Youssef Zinad and MIRhosting founder Andrey Nesterenko. Infrastructure tied to NoName057(16). [Sources: KREBS-FIOD-STARK; DARKREADING-ELLIO-STARK]
>
> *Effect disputed. ELLIO telemetry (via Dark Reading, ~2026-05-28) found scanning from the network at almost pre-raid levels **more than a week later**, and Check Point (June) linked Iranian operations to the network; later telemetry (a 94% drop in the indexed fleet) and a reported THE.Hosting closure notice point the other way. The MIRhosting "temporarily paused" quote could not be re-verified. Corrected 2026-09-25: Nesterenko is MIRhosting's founder, not a WorkTitans director.*

**2026-05** | **Intelligence** | **Intrinsec -- OMEGATECH, Virtualine's New Network**
> Tracing March 2026 malspam that delivered a JavaScript backdoor, Intrinsec assessed OMEGATECH (AS202412) as "yet another network created by hosting provider Virtualine, advertised on underground forums" (642,000+ honeypot hits from its IPs in March 2026) and linked GHOSTYNETWORKS (AS205759, Kentucky, registered January 2026) to the defunct AnonRDP-linked OPTIBOUNCE. Spamhaus now lists AS202412 under virtualine.org. [Source: INTRINSEC-OMEGATECH-2026]

**2026-05-06** | **Intelligence** | **Recorded Future / TAE Framework**
> Recorded Future publishes "Threat Activity Enablers: The Backbone of Today's Threat Landscape" (Stowe & Plude). Formally defines the TAE framework and introduces the Threat Density Score methodology for systematically quantifying malicious hosting concentration across providers. [Source: RF-TAE-2026]

**2026-04-28** | **Intelligence** | **Europol IOCTA 2026**
> Europol publishes the Internet Organised Crime Threat Assessment (IOCTA) 2026, "The evolving threat landscape -- how encryption, proxies and AI are expanding cybercrime" -- a comprehensive assessment covering BPH ecosystems, ransomware-as-a-service, cryptocurrency laundering pipelines, and AI-enabled cybercrime. [Source: IOCTA-2026]

**2026-04-23** | **Sanctions** | **EU 20th Russia Sanctions Package -- Sectoral CASP Ban**
> The EU's 20th package imposes a **transaction ban on crypto-asset service providers established in Russia and Belarus**, effective 2026-05-24, and lists CJSC TengriCoin (Meer.kg) and the RUBx stablecoin. It also activates the anti-circumvention tool against Kyrgyzstan for certain exports. Strategically a pivot: rather than keep naming individual platforms -- each of which spawned a successor -- the EU prohibited a whole category. [Source: EU-20TH-PACKAGE]
>
> *The previously quoted "120 listings, the largest in two years" is unverified. The 21st package (2026-07-23) extended the category approach to third countries.*

**2026-04-15** | **Evasion / Provider Event** | **Grinex Drained and Suspended; A7A5 Economy Contracts**
> Around 12:00 UTC on 2026-04-15, roughly $13-15M was drained from Grinex -- the Garantex successor exchange (Grinex claimed more than 1bn rubles and blamed foreign "special services"; Elliptic measured ~$15M in USDT). Grinex suspended operations on 16-17 April; Chainalysis raised the possibility of a false-flag exit. The A7A5 ruble stablecoin (issuer Old Vector) had no freeze function and did not technically depeg, but its economy ran through Grinex and on-chain volume reportedly collapsed (a ~96% figure is unverified). Chainalysis puts A7A5 flows at $93.3B "in less than a year"; Elliptic at more than $100B. Grinex, A7A5 and Old Vector remain sanctioned (OFAC/UK/EU); the change is operational, not legal. [Sources: CHAINALYSIS-A7A5; ELLIPTIC-GRINEX; TRM-A7A5-2026]

**2026-04-15** | **LE Operation** | **Operation PowerOFF Action Week -- 53 DDoS-for-Hire Domains**
> A 21-country action seized 53 domains, made 4 arrests, executed 25 search warrants and warned 75,000 identified users of booter services. [Sources: [Europol](https://www.europol.europa.eu/media-press/newsroom/news/operation-poweroff-53-domains-seized-in-fight-against-ddos-for-hire-services) (A, as cited); [BleepingComputer](https://www.bleepingcomputer.com/news/security/operation-poweroff-identifies-75k-ddos-users-takes-down-53-domains/) (C)]

**2026-04** | **Intelligence** | **Silent Push -- Triad Nexus / FUNNULL After Sanctions**
> Silent Push documents that Triad Nexus kept operating through "clean" front brands (Bole CDN, CDN1.ai and others) that were launched *before* the May 2025 sanctions, plus accounts at major cloud providers and geofencing of US IP ranges. [Source: SILENTPUSH-TRIADNEXUS-2026]
>
> *Correction: the earlier "175+ rotating CNAMEs" figure is unsourced; the FBI's May 2025 count is 548 FUNNULL CNAMEs linked to 332,000+ domains.*

**2026-03-26** | **Sanctions** | **UK Designates Xinbi Guarantee**
> The UK became the first country to sanction the Xinbi marketplace, together with the #8 Park scam compound and Legend Innovation Co. [Source: [BleepingComputer](https://www.bleepingcomputer.com/news/security/uk-sanctions-xinbi-marketplace-linked-to-asian-scam-centers/) (C)]

**2026-03-19** | **Intelligence** | **Recorded Future Insikt -- 2025 Year in Review: Malicious Infrastructure**
> Introduces the Threat Density List ranking hosting providers by malicious-activity concentration. The 2025 top ten: Virtualine, CrazyRDP, Stark Industries, Kaopu Cloud HK, Aeza, PrivateAlps, 4VPS, Defhost, Silent Connection, DolphinHost. [Source: RF-INFRA-2025]
>
> *The top-ten order is relayed from secondary summaries of RF CTA-2026-0319 and should be checked against the primary report.*

**2026-03-11** | **LE Operation** | **Operation Lightning -- SocksEscort (AVrecon) Residential-Proxy Botnet**
> Europol, the US and European partners disrupted SocksEscort, running since 2020: more than 369,000 compromised routers and IoT devices in 163 countries; 34 domains and 23 servers in 7 countries seized; $3.5M in crypto frozen. [Sources: [Europol](https://www.europol.europa.eu/media-press/newsroom/news/europol-and-international-partners-disrupt-socksescort-proxy-service) (A, snippet); [The Hacker News](https://thehackernews.com/2026/03/authorities-disrupt-socksescort-proxy.html) (C)]

**2026-03-06** | **Sanctions (policy)** | **E.O. 14390 -- Combating Cybercrime, Fraud, and Predatory Schemes Against American Citizens**
> Sets a policy and coordination mandate (a 60-day review, a 120-day action plan, an operational cell in the National Coordination Center, a victim-restoration recommendation and international engagement) but creates **no new blocking authority**; 2026 designations still rest on earlier orders such as E.O. 13694 (e.g. OFAC-1VPNS). [Source: E.O. 14390 text (A, read via a mirror)]

**2026-02** | **Intelligence** | **Censys / WorkTitans Migration Confirmation**
> Censys confirms the WorkTitans/THE.Hosting migration via RDP hostname fingerprint reuse: WIN-J9D866ESIJ2 was observed across pre- and post-sanctions infrastructure. [Source: CENSYS-BPH]

**2026-02** | **Intelligence** | **GreyNoise / PROSPERO-Proton66 and Ivanti EPMM**
> GreyNoise reports AS200593 (PROSPERO) as the dominant source of Ivanti EPMM mass exploitation: 346 of 417 sessions (83%) over 1-9 February came from a single address, 193[.]24[.]123[.]42. [Source: GREYNOISE-PROSPERO]

**2026-02** | **Intelligence** | **Sophos -- Ransomware Operators Leasing ISPsystem VMmanager VMs**
> Sophos shows that default ISPsystem VMmanager Windows templates reuse the same hostnames and identifiers, which appear across LockBit, Qilin, Conti, BlackCat, Ursnif, PureRAT, Lampion, Lumma and WantToCry infrastructure leased from bulletproof providers (MasterRDP among them). This repository associates Stark Industries and First Server Limited with that ecosystem; the provider naming could not be re-verified from the available summary. [Source: SOPHOS-VMMANAGER]

**2026-01-29** | **Private-sector disruption** | **Google GTIG Disrupts the IPIDEA Residential-Proxy Network**
> Legal action against IPIDEA's command domains, with Cloudflare, Spur and Lumen Black Lotus Labs, shrank the device pool by millions; more than 550 threat groups had used the network in a single week, and Play Protect now removes apps carrying its SDKs. Added to the database as a proxy enabler. [Source: GTIG-IPIDEA-2026]

**~2026-01-28** | **LE Operation** | **FBI Seizure of the RAMP Ransomware Forum (Reported)**
> RAMP's clear-web and onion domains reportedly displayed an FBI seizure notice. RAMP was where LockBit launched 5.0 in September 2025. [Sources: [RansomwareEDP brief](https://github.com/RansomwareEDP/Mapping/blob/main/briefs/edp-monthly-2026-07.html) (C/D)] *Needs primary FBI/DOJ confirmation.*

**2026-01-28** | **Sanctions (administrative)** | **UK Sanctions List Becomes the Single UK Source**
> OFSI's Consolidated List closed in favour of the FCDO-maintained UK Sanctions List, which now carries all UK designations. [Source: FCDO-UK-SANCTIONS-LIST]

**2026-01-07** | **LE Operation** | **Prince Group Chairman Chen Zhi Extradited to China; Tudou Winds Down**
> Chen Zhi and two associates were arrested in Cambodia and extradited to China (reported 2026-01-07). Tudou Guarantee then stopped transacting through its public Telegram groups and admin-wallet activity collapsed, although its gambling operations continue. [Sources: [CNN](https://www.cnn.com/2026/01/07/asia/chen-zhi-arrest-extradition-cambodia-china-intl-hnk) (C); ELLIPTIC-TUDOU]

---

## 2025

**2025-12-10** | **Intelligence (context)** | **Canada Lists 764, Maniac Murder Cult, Terrorgram Collective and IS-Mozambique**
> Public Safety Canada listed four separate terrorist entities under the Criminal Code: 764, the Maniac Murder Cult, the Terrorgram Collective and Islamic State-Mozambique. [Source: [Epoch Times](https://www.theepochtimes.com/world/canada-adds-4-entities-to-terrorist-list-including-online-group-inciting-youth-to-self-harm-5956483) (C)]
>
> *Corrected 2026-09-25: these are four listings, not one "764 network" with components, and no source ties them to BPH-hosted infrastructure; kept as context only.*

**2025-12-01** | **LE Operation** | **Operation Olympia -- Cryptomixer.io**
> Germany and Switzerland, with Europol and Eurojust, shut down Cryptomixer.io (action 24-28 November; announced 1 December): three servers in Zurich and the domain seized, more than EUR 25M in Bitcoin confiscated and 12TB of data obtained. The mixer had processed more than EUR 1.3B in Bitcoin since 2016.

**2025-11-19** | **Sanctions** | **US / UK / AU -- Media Land LLC + Yalishanda (Volosovik)**
> Coordinated action with differing lists. **OFAC** (sb0319): Media Land LLC; its sister company ML.Cloud LLC and 100%-owned subsidiaries Media Land Technology and Data Center Kirishi; and three leaders -- general director Aleksandr Volosovik ("Yalishanda"), Kirill Zatolokin and Yulia Pankova. **UK** (Cyber regime): Media Land LLC, ML.Cloud LLC, Volosovik, Zatolokin, Pankova and Andrei Kozlov. **Australia** (announced 20 November): Media Land LLC, ML.Cloud LLC, Volosovik and Zatolokin. Treasury called Media Land a launch pad for LockBit, BlackSuit and Play. [Sources: OFAC-MEDIALAND; AU-DFAT-MEDIALAND]

**2025-11-19** | **Sanctions** | **OFAC -- Aeza Follow-On: Hypercore, Smart Digital Ideas, Datavice, Makarov, Zakirov; UK Designates Aeza Group LLC**
> OFAC sanctioned Aeza's evasion network: UK front Hypercore Ltd (AS211522), Serbian Smart Digital Ideas DOO, Uzbek Datavice MCHJ (established 2025-07-03; Tax ID 312252645; Reg. 2868352; [CAATSA-RUSSIA] [CYBER4]; Linked To AEZA GROUP LLC), new Aeza executive Maksim Makarov and Ilya Zakirov, who set up new companies and payment channels -- all under E.O. 13694 as amended. The same day the UK designated **Aeza Group LLC** under the Russia regime (asset freeze plus director-disqualification, internet-services and trust-services sanctions). [Sources: OFAC-MEDIALAND; FCDO-UK-SANCTIONS-LIST]
>
> *The UK's 19 Nov notices list neither Datavice nor Hypercore; the observation that Hypercore appears as a `Subsidiaries` value on the Aeza Group LLC row of the UK list (checked 2026-07-17) could not be re-verified in September 2026. Corrected 2026-09-25: the earlier "AS215552" for Hypercore belongs to an unrelated Romanian holder.*

**2025-11-19** | **Intelligence** | **CISA/NSA/FBI/DC3 + International Partners -- BPH Guidance**
> CISA, NSA, FBI and DC3 (US), with ASD's ACSC (AU), the Canadian Centre for Cyber Security (CA), NCSC-NL (NL), NCSC-NZ (NZ) and NCSC-UK (UK), publish "Bulletproof Defense: Mitigating Risks From Bulletproof Hosting Providers" -- the first comprehensive interagency guidance on identifying and defending against BPH-sourced threats. Developed via the Joint Ransomware Task Force. [Source: CISA-BPH-2025]
>
> *Co-sealers are Five Eyes **plus the Netherlands** -- NCSC-NL is not a Five Eyes member.*

**2025-11-13** | **LE Operation** | **Operation Endgame 3.0 -- Rhadamanthys, VenomRAT, Elysium**
> Action 10-13 November: 1,025 servers taken down or disrupted and 20 domains seized; Rhadamanthys had 525,303 infections between March and November 2025. The alleged VenomRAT developer, an Albanian national, had been arrested in Athens on 2025-11-03 on a French European arrest warrant. [Source: EUROPOL-ENDGAME-2025]
>
> *Corrected label: Europol does not number phases; press usage makes this "3.0" (original May 2024; "2.0" May 2025).*

**2025-11-12** | **LE Operation** | **Dutch Police Seize ~250 Servers of a Bulletproof Hoster (Press-Attributed to CrazyRDP)**
> Dutch police seized about 250 physical servers in data centres in The Hague and Zoetermeer (announced 14 November), taking thousands of virtual servers offline; the unnamed hoster had been active since 2022 and appeared in 80+ investigations spanning ransomware, botnets, phishing and CSAM. Sources told BleepingComputer it was CrazyRDP, which went offline. [Sources: POLITIE-CRAZYRDP-2025; BLEEPINGCOMPUTER-BPH]
>
> *Corrections: police did not name the service and told BleepingComputer the case is **not connected to Operation Endgame**; the Limenet (AS394711) and Delis (AS211252) ASN attribution is community-sourced and both ASNs have since been re-issued to unrelated companies.*

**2025-11-06** | **Intelligence** | **Recorded Future Insikt / aurologic GmbH**
> Recorded Future Insikt publishes "Malicious Infrastructure Finds Stability with aurologic GmbH" -- naming aurologic as a central upstream hub for malicious hosting and documenting downstreams including Femo IT/Defhost, Global-Data (SWISSNETWORK02), the metaspinner-named AS209800, Railnet/Virtualine and Aeza. [Source: RF-AUROLOGIC]

**2025-10-23** | **Sanctions** | **EU 19th Russia Package -- A7A5 Ban**
> Council Regulation (EU) 2025/2033 bans transactions in the A7A5 ruble stablecoin from 2025-11-25 and lists the A7A5 developer, the Kyrgyz issuer and a trading-platform operator (reported as A7 LLC, Old Vector and Grinex), plus Payeer. [Source: [Council](https://www.consilium.europa.eu/en/press/press-releases/2025/10/23/19th-package-of-sanctions-against-russia-eu-targets-russian-energy-third-country-banks-and-crypto-providers/) (A)]

**2025-10-14** | **Sanctions + LE Operation** | **Prince Group TCO; Chen Zhi Indicted; FinCEN Final Rule on Huione**
> OFAC designated 146 individuals and entities of the Prince Group transnational criminal organisation, including chairman Chen Zhi, jointly with UK action. DOJ (E.D.N.Y.) unsealed an indictment of Chen Zhi and filed a forfeiture action for 127,271 BTC (~$15B), and FinCEN issued its final Section 311 rule naming Huione Group a primary money-laundering concern. The foundation for the Huione -> Tudou -> H-Pay / Xinbi successor chain. [Source: OFAC-PRINCE-2025]

**2025-10-10** | **LE Operation** | **FBI + French BL2C Seize breachforums.hn (SLSH Extortion Portal)**
> Seized hours before Scattered LAPSUS$ Hunters published Salesforce-customer data; law enforcement also obtained BreachForums database backups going back to 2023. [Source: [CyberInsider](https://cyberinsider.com/fbi-seized-shinyhunters-breachforums-salesforce-leak-portal/) (C)]

**2025-10-10** | **LE Operation** | **Operation SIMCARTEL -- SIM-Box Crime-as-a-Service Network**
> Action day in Latvia with Austria, Estonia and Finland plus Europol and Eurojust: 1,200 SIM-box devices, 40,000 SIM cards and 5 servers seized; about 49M fraudulent accounts; 3,200+ fraud cases and ~EUR 5M in losses. Latvian State Police reported five Latvian nationals arrested (press counted seven arrests in total). [Source: [Latvian State Police](https://www.vp.gov.lv/en/article/international-operation-simcartel-state-police-dismantles-it-infrastructure-used-online-fraud-five-latvian-nationals-arrested) (A)]

**2025-10-03** | **Intelligence** | **Scattered LAPSUS$ Hunters Salesforce Extortion Site**
> The group's leak site went up claiming ~1B records from 39 companies -- the extortionists' own claim (grade E) -- with a 10 October deadline; data was published hours after the breachforums.hn seizure. [Source: [Help Net Security](https://www.helpnetsecurity.com/2025/10/06/data-leak-site-extortion-salesforce/) (C)]

**2025-09-16** | **Provider Event** | **Stark Industries Solutions Ltd Dissolved**
> Companies House records the dissolution of Stark Industries Solutions Ltd (13906017); the network continued as WorkTitans/THE.Hosting and UFO Hosting. [Source: UK-COMPANIES-HOUSE]

**2025-09** | **Provider Event** | **LockBit 5.0 Launched on RAMP**
> In early September LockBit announced 5.0 on RAMP (its sixth anniversary), asking new affiliates for a Bitcoin deposit of roughly $500 to access the panel and encryptor; builds target Windows, Linux and VMware ESXi. [Source: [Check Point](https://blog.checkpoint.com/research/lockbit-returns-and-it-already-has-victims/) (B)]

**2025-09** | **Provider Event** | **DragonForce / LockBit / Qilin "Coalition"**
> DragonForce proposed a partnership with LockBit and Qilin; ReliaQuest's Q3 report publicised it. No shared leak site or infrastructure has been observed and SuspectFile disputes that it is a real alliance. [Source: [ReliaQuest](https://reliaquest.com/blog/threat-spotlight-ransomware-and-cyber-extortion-in-q3-2025/) (B)]

**2025-08-20** | **Sanctions** | **UK -- Grinex, Old Vector and Kyrgyz Rails**
> The UK designated Grinex LLC, CJSC Tengricoin (Meer), Old Vector LLC, OJSC Capital Bank of Central Asia and Altair Holding SA plus three individuals under the Russia regime, saying A7A5 had moved $9.3B in four months. [Source: FCDO-UK-SANCTIONS-LIST]

**2025-08-14** | **Sanctions** | **OFAC -- Garantex Re-Designation, Grinex and the A7 Network**
> OFAC (sb0225) re-designated Garantex Europe OU and designated its successor Grinex, three executives (Sergey Mendeleev, Aleksandr Mira Serda, Pavel Karavatsky) and six companies: InDeFi Bank and Exved (Mendeleev-linked payment firms), Old Vector LLC (the A7A5 issuer), A7 LLC, A71 LLC and A7 Agent LLC (owned by Ilan Shor and Promsvyazbank). The State Department offered rewards totalling up to $6M: up to $5M for Mira Serda and up to $1M for other Garantex leaders. [Source: OFAC-GARANTEX]

**2025-08-08** | **Provider Event** | **"Scattered LAPSUS$ Hunters" Telegram Channel Appears**
> A self-declared merger brand of Scattered Spider, LAPSUS$ and ShinyHunters; the first channel was banned on 11 August and moved to backups. [Sources: [S-RM](https://www.s-rminform.com/cyber-intelligence-briefing/shineyhunters-cyber-intelligence-briefing-15-august-2025) (C); KREBS-SLSH]
>
> *Corrected from "2025-08-25 SLSH alliance announced".*

**2025-07-22** | **LE Operation** | **XSS.is Administrator Arrested in Kyiv; Forum Seized**
> A French-led investigation with Ukraine's SBU and Europol arrested the 38-year-old alleged administrator and seized xss.is (50,000+ users). [Source: [Europol](https://www.europol.europa.eu/media-press/newsroom/news/key-figure-behind-major-russian-speaking-cybercrime-forum-targeted-in-ukraine) (A, snippet)]

**2025-07-20** | **Evasion** | **Aeza Moves 2,100+ IPs to Hypercore (AS211522)**
> Ten days after AS211522 was allocated to the UK front Hypercore Ltd (~2025-07-10), Aeza began migrating more than 2,100 IPs from AS210644 to it -- nineteen days after the OFAC designation. [Source: SILENTPUSH-AEZA-2025]

**2025-07-16** | **LE Operation** | **Operation Eastwood -- NoName057(16)**
> Action 14-17 July across 12 acting countries: 2 arrests, 7 arrest warrants, 24 house searches, 13 people questioned, 1,000+ supporters warned and more than 100 systems disrupted, taking most of the central server infrastructure offline. The group was degraded rather than stopped. [Sources: [BleepingComputer](https://www.bleepingcomputer.com/news/security/europol-disrupts-pro-russian-noname05716-ddos-hacktivist-group/) (C); [Imperva](https://www.imperva.com/blog/operation-eastwood-measuring-the-real-impact-on-noname05716/) (B)]
>
> *Corrected: "19 countries and 200 police officers" could not be sourced.*

**2025-07-01** | **Sanctions** | **OFAC (with UK NCA) -- Aeza Group LLC and UK Front Aeza International Ltd**
> OFAC (sb0185) designated **Aeza Group LLC** as the primary target, together with its UK front Aeza International Ltd, its subsidiaries Aeza Logistic LLC and Cloud Solutions LLC, and four executives: CEO Arsenii Penzev, general director Yurii Bozoyan, technical director Vladimir Gast and 33% owner Igor Knyazev. The SDN entry for Aeza Group LLC carries a TRON address (TU4tDFRvcKhAZ1jdihojmBWZqvJhQCnJ4F). Aeza hosted Meduza and Lumma infostealer operators, BianLian and the BlackSprut market. [Source: OFAC-AEZA]
>
> *Corrections: Aeza International Ltd is a UK company, not the main designee; the TRON address was not "one of the first" BPH wallet designations -- OFAC's Zservers action (2025-02-11) already listed BTC addresses.*

**2025-06-25** | **LE Operation** | **French BL2C Arrests Four BreachForums / ShinyHunters Members**
> Those arrested used the handles ShinyHunters, Hollow, Noct and Depressed; Kai West ("IntelBroker") had been arrested in France in February 2025. [Source: [SiliconANGLE](https://siliconangle.com/2025/06/25/breachforums-leaders-including-shinyhunters-intelbroker-arrested-france/) (C)]

**2025-06-24** | **Intelligence** | **NATO Summit DDoS -- NoName057(16)**
> During the 24-25 June NATO summit in The Hague, NoName057(16) claimed DDoS attacks on Dutch municipalities, public-transport company Connexxion and summit side-event sites. [Source: [NL Times](https://nltimes.nl/2025/06/24/sabotage-may-behind-schiphol-rail-problems-cyberattack-hits-nato-summit-websites) (C)]
>
> *Recategorised from "LE Operation" (it was a threat-actor event); the claim that the traffic came from BPH-hosted botnets is unsourced.*

**2025-06-24** | **Evasion** | **WorkTitans B.V. AS209847 Created**
> AS209847 is created for WorkTitans B.V., the Dutch post-sanctions successor to Stark Industries (its RIPE org ORG-WB96-RIPE the day before). Chain: Stark -> PQ Hosting Plus (AS44477) and the THE.Hosting brand (ORG-THE3-RIPE, 2025-05-28) -> WorkTitans B.V.; created 35 days after the EU listing. [Sources: RF-STARK; GREYNOISE-STARK]

**2025-06-16** | **LE Operation** | **Archetyp Market**
> Archetyp Market, Europol's "longest-standing" dark-web drug market, was dismantled (action 11-13 June): 600,000+ users and at least EUR 250M in transactions; the administrator, a 30-year-old German, was arrested in Barcelona, with a moderator and six top vendors also arrested and EUR 7.8M seized. [Source: [Europol](https://www.europol.europa.eu/media-press/newsroom/news/europe-wide-takedown-hits-longest-standing-dark-web-drug-market) (A, snippet)]

**2025-05-29** | **Sanctions** | **OFAC -- FUNNULL Technology Inc.**
> OFAC (sb0149) designated Philippines-based Funnull Technology Inc. and its administrator Liu Lizhi for infrastructure behind cryptocurrency investment scams causing more than $200M in US victim-reported losses; the FBI FLASH the same day counted 548 FUNNULL CNAMEs linked to 332,000+ domains. CTG Server Limited and StarCloud were **not** designated. [Sources: OFAC-FUNNULL; FBI-IC3-FUNNULL]

**2025-05-29** | **Evasion** | **Stark Network Rebranded as THE.Hosting**
> Recorded Future dates the THE.Hosting rebrand to 2025-05-29 -- nine days *after* the EU listing -- following creation of RIPE org ORG-THE3-RIPE on 2025-05-28. [Source: RF-STARK]
>
> *Corrected from "2025-05-19, one day before sanctions".*

**2025-05-23** | **LE Operation** | **Operation Endgame 2.0**
> Action 19-22 May against Bumblebee, Latrodectus, Qakbot, HijackLoader, DanaBot, Trickbot and Warmcookie: ~300 servers taken down, 650 domains neutralised, international arrest warrants against 20 targets, EUR 3.5M in crypto seized (EUR 21.2M cumulative). [Source: [Europol](https://www.europol.europa.eu/media-press/newsroom/news/operation-endgame-strikes-again-ransomware-kill-chain-broken-its-source) (A, snippet)]
>
> *Corrected: Smokeloader was not a May 2025 target (see 2025-04-09 and 2024-05-30).*

**2025-05-21** | **LE Operation** | **Lumma Stealer Disruption**
> A US court order let Microsoft seize, suspend or block about 2,300 Lumma domains; DOJ seized the control-panel domains, with Europol and Japan's JC3 participating. The Lumma developers were later sanctioned by the EU and UK (2026-07-13). [Source: [BleepingComputer](https://www.bleepingcomputer.com/news/security/lumma-infostealer-malware-operation-disrupted-2-300-domains-seized/) (C)]

**2025-05-20** | **Sanctions** | **EU -- Stark Industries + Neculiti Brothers (Hybrid-Threats Regime)**
> Council Implementing Regulation (EU) 2025/965 lists Stark Industries Solutions Ltd (UK reg. 13906017; websites stark-industries.solutions and pq.hosting), owner Ivan Neculiti ("owner of Stark Industries and PQ Hosting") and CEO Iurie Neculiti under the hybrid-threats regime, Regulation (EU) 2024/2642. The first EU sanctions directly targeting a BPH provider and its operators. [Source: EU-STARK]
>
> *Legal basis: not the 17th Russia package, which was adopted the same day under a different legal basis. **PQ Hosting Plus S.R.L. is not in the annex** -- any restriction on it arises only indirectly through the listed Neculitis.*

**2025-05-16** | **Evasion** | **AS44477 Transferred to PQ Hosting Plus S.R.L.**
> RIPE records the transfer of AS44477 from Stark Industries to PQ Hosting Plus S.R.L. -- **four days** before the EU listing. [Source: RF-STARK]
>
> *Corrected from "~12 days"; twelve days is the lead time from the 2025-05-08 leak.*

**2025-05-13** | **Evasion** | **PQ Hosting Plus S.R.L. Created in the RIPE Database**
> RIPE org ORG-PHPS1-RIPE (Chisinau) created to receive Stark Industries resources ahead of the anticipated EU listing. [Source: RF-STARK]

**2025-05-09** | **LE Operation** | **Operation Moonlander -- Anyproxy / 5socks Router-Proxy Botnet**
> Dutch and US authorities, with Lumen Black Lotus Labs, dismantled a proxy service running since 2004 that advertised 7,000+ daily proxies and earned more than $46M; four people were charged in N.D. Okla. [Source: [The Hacker News](https://thehackernews.com/2025/05/breaking-7000-device-proxy-botnet-using.html) (C)]

**2025-05-09** | **LE Operation** | **eXch No-KYC Swap Service Seized**
> German BKA/ZIT with the Dutch FIOD seized eXch (action 30 April): EUR 34M in crypto and 8TB of data; about $1.9B laundered. [Source: [The Record](https://therecord.media/exch-cryptocurrency-mixer-germany-takedown) (C)]

**2025-05** | **Sanctions** | **FinCEN Section 311 Finding and Proposed Rule -- Huione Group**
> FinCEN found Huione Group (Haowang Guarantee, Huione Pay, Huione Crypto) a primary money-laundering concern and proposed a special measure, citing at least $4B laundered. [Source: [Federal Register 2025-07837](https://www.federalregister.gov/public-inspection/2025-07837/special-measure-regarding-huione-group-as-a-foreign-financial-institution-of-primary-money) (A)]

**2025-05-09** | **Intelligence** | **RIPE/ARIN Stark Sanctions Preparations**
> RIPE and ARIN records show resource-transfer activity and corporate restructuring by the Stark network ahead of the EU listing. *No specific source was identified for this entry in the 2026-09 audit.*

**2025-05-08** | **Intelligence** | **RFE/RL Moldova Report on Upcoming Stark Sanctions**
> Moldovan reporting on the upcoming sanctions gave about 12 days of public notice before the 20 May listing -- the "heads-up" GreyNoise identifies. [Sources: RF-STARK; GREYNOISE-STARK]

**2025-05-07** | **Intelligence** | **LockBit Panel Breach**
> LockBit's panels were defaced ("Don't do crime CRIME is BAD xoxo from Prague") and an SQL dump leaked: ~60,000 BTC addresses, 4,442 negotiation messages (Dec 2024-Apr 2025) and 75 admin/affiliate accounts. The leak contained build records, not builder binaries. [Source: [Help Net Security](https://www.helpnetsecurity.com/2025/05/09/lockbit-hacked-data-leaked/) (C)]

**2025-04-25** | **Evasion** | **Virtualine Shifts IPv4 to the metaspinner-Named AS209800**
> Virtualine Technologies shifted IPv4 resources to AS209800, a new AS registered in the name of the legitimate Hamburg company metaspinner net GmbH, which Recorded Future says Virtualine-affiliated actors impersonated. The ranges later moved to OMEGATECH (AS202412), and AS209800 has been re-issued to an unrelated holder. [Source: RF-AUROLOGIC]

**2025-04-10** | **Evasion** | **Stark Industries -> UFO Hosting Prefix Migration**
> Stark Industries began transferring Russian-origin prefixes to UFO Hosting LLC (most transfers on 2025-04-13), about 40 days before the EU listing. [Source: RF-STARK]

**2025-04-09** | **LE Operation** | **Operation Endgame Follow-Up -- Smokeloader Customers**
> Customers identified from the Smokeloader database seized in 2024 faced five detentions, searches, warrants and "knock-and-talk" interviews. [Source: [Europol](https://europol.europa.eu/media-press/newsroom/news/operation-endgame-follow-leads-to-five-detentions-and-interrogations-well-server-takedowns) (A, snippet)]

**2025-04-03** | **LE Operation** | **Aeza Founders Detained in Russia**
> Russian authorities detained Aeza co-owners Arsenii Penzev (CEO) and Yurii Bozoyan (general director) and employees Maxim Orel and Tatyana Zubova over hosting the BlackSprut darknet drug market. A Russian domestic prosecution, not a Western action. [Sources: [Qurium](https://www.qurium.org/alerts/aeza-blacksprut-and-disinformation/) (C); OFAC-AEZA]
>
> *The exact day is disputed across sources (1, 3 or 11 April).*

**2025-04-02** | **LE Operation** | **Operation Stream -- Kidflix**
> Europol announced the takedown of Kidflix, a CSAM platform launched in 2021 (91,000 unique videos; 1.8M users logged in between April 2022 and March 2025). German and Dutch authorities seized the server on 2025-03-11; ~1,400 suspects were identified and 79 arrested. [Source: [Europol](https://www.europol.europa.eu/media-press/newsroom/news/global-crackdown-kidflix-major-child-sexual-exploitation-platform-almost-two-million-users) (A, quoted)]
>
> *Corrected from an undated "2021-2025" entry (80,000 videos); the claim that it relied on BPH infrastructure is unsourced.*

**2025-03-13** | **Evasion** | **UFO Hosting LLC (AS33993)**
> UFO Hosting LLC's RIPE org is registered (company registered 2025-02-18; director Savushkin). Purpose-built as a sanctions-resilient vehicle for Stark Industries' Russian prefixes; about 68 days before the EU listing. Spamhaus now lists AS33993 under stark-industries.solutions. [Source: RF-STARK]

**2025-03-06** | **LE Operation** | **Garantex Domains Seized; Operators Charged**
> The US Secret Service, with Dutch, German, Estonian and Finnish partners, seized garantex.org, .io and .academy and froze more than $26M; DOJ unsealed an E.D. Va. indictment of technical administrator Aleksej Besciokov and co-founder Aleksandr Mira Serda the next day. Besciokov was arrested in Kerala, India around 2025-03-11. [Source: DOJ-GARANTEX-2025]
>
> *Corrected from "2025-03-25".*

**2025-02-24** | **Sanctions** | **EU 16th Russia Sanctions Package -- Garantex**
> The EU's 16th package lists Garantex, linked to sanctioned Russian banks, with six attributed wallet addresses -- the first cryptocurrency exchange the EU sanctioned. [Source: EU-16TH-PACKAGE]

**2025-02-12** | **LE Operation** | **Dutch Police Take 127 Zservers/XHOST Servers Offline**
> The day after the sanctions, Dutch police took down 127 servers in Amsterdam identified as Zservers/XHOST infrastructure. [Source: THERECORD-ZSERVERS-SEIZURE]

**2025-02-11** | **Intelligence** | **Black Basta Chat Leak**
> "ExploitWhispers" leaked a 47MB JSON file of about 200,000 Black Basta Matrix messages (Sept 2023-Sept 2024); it became widely known on 20 February via PRODAFT. [Source: [The Record](https://therecord.media/black-basta-ransomware-group-chat-logs-leaked) (C)]

**2025-02-11** | **LE Operation** | **Operation Phobos Aetor -- Phobos/8Base**
> Four suspects were arrested in Phuket on 10 February, 27 servers taken down, the 8Base leak site seized and 400+ companies warned, across 14 countries; DOJ charged two Russian nationals. [Source: [Infosecurity](https://www.infosecurity-magazine.com/news/8base-ransomware-phobos-arrested/) (C)]
>
> *Corrected: not "four Russian nationals arrested".*

**2025-02-11** | **Sanctions** | **US / UK / AU -- Zservers/XHOST**
> Designations differ by authority. **OFAC** (sb0018): Zservers and administrators Alexander Mishin and Aleksandr Bolshakov, with three BTC addresses on Zservers and one on Mishin. **UK**: ZSERVERS, the UK front XHOST Internet Solutions LP and six individuals (Bolshakov, Mishin, Ilya Sidorov, Dmitry Bolshakov, Igor Odintsov, Vladimir Ananev). **Australia** (announced 12 February, its first cyber sanction on an entity): Zservers and five individuals. UK and Australian texts tie Zservers infrastructure to the 2022 Medibank data leak. [Sources: OFAC-ZSERVERS; FCDO-UK-SANCTIONS-LIST; AU-DFAT-ZSERVERS]

**2025-01-30** | **LE Operation** | **Operation Talent -- Cracked, Nulled, Sellix and StarkRDP**
> A German-led action (28-30 January) seized 17 servers, 12 domains and about EUR 300,000 and arrested two people in Spain. The seized domains included **starkrdp.io**, an RDP/VPS host abused by criminals. [Sources: [Infosecurity](https://www.infosecurity-magazine.com/news/operation-dismantles-cracked/) (C); [Cybernews](https://cybernews.com/cybercrime/hacker-forums-cracked-nulled-mysellix-starkrdp-siezed-fbi-operation-talent/) (C)]
>
> *Replaces an erroneous "2025-01-20 BreachForums + XSS takedown": no joint takedown happened. See 2025-06-25, 2025-07-22 and 2025-10-10 for the actual BreachForums and XSS actions.*

**2025-01-10** | **LE Operation** | **Blender.io / Sinbad.io Operators Indicted**
> DOJ (N.D. Ga.) and the Netherlands charged the operators of mixers used by ransomware actors and the DPRK (two arrested in December 2024). [Source: [Help Net Security](https://www.helpnetsecurity.com/2025/01/13/alleged-blender-sinbad-cryptomixer-operators-arrested-indicted/) (C)]

**2025-01** | **Provider Event** | **Silent Connection Ltd + Dolphon 1337 Ltd Dissolved (Reported)**
> Silent Connection Ltd and Dolphon 1337 Ltd were reportedly compulsorily dissolved at UK Companies House. Their ASNs have since been re-issued -- AS215240 to a German UG (no routes) and AS215208 to an Indonesian ISP -- so neither network persists under the original operators. [Sources: EXCEDO-ASN; REGISTRY-SNAPSHOT-2026-09]

---

## 2024

**2024-12-09** | **Intelligence** | **Huntress -- Cleo Exploitation (Cl0p)**
> Huntress reported exploitation of Cleo Harmony/VLTrader/LexiCom from 3 December (Cl0p claimed it on 15 December); one callback address, 5[.]149[.]249[.]226, sat in HZ Hosting's AS59711. [Source: HUNTRESS-CLEO-2024]

**2024-12** | **Evasion** | **Grinex Registered in Kyrgyzstan**
> Grinex, later Garantex's successor, was registered in Kyrgyzstan about three months before the Garantex takedown (TRM). [Source: TRM-A7A5-2026]

**2024-11-11** | **Provider Event** | **QWINS LTD Incorporated**
> QWINS LTD incorporated in the United Kingdom (reported). Spamhaus now lists three QWINS ASNs. [Source: INTEL-INSIGHTS-QWINS]

**2024-11-08** | **Provider Event** | **WAIcore AS213887**
> WAIcore AS213887 reported registered via RIPE (date unverified). Earlier WAIcore ASNs (AS202973, AS206425, AS210281) were already on Spamhaus ASN-DROP by February 2024 and have since been re-issued. [Source: SPAMHAUS-ASNDROP-2026]

**2024-10-28** | **LE Operation** | **Operation Magnus -- RedLine and META Infostealers**
> Dutch-led with the FBI, DOJ and Eurojust: three servers taken down in the Netherlands and domains and Telegram channels seized; DOJ charged the alleged RedLine developer, Maxim Rudometov. [Source: [BleepingComputer](https://www.bleepingcomputer.com/news/legal/redline-meta-infostealer-malware-operations-seized-by-police/) (C)]

**2024-10-01** | **Sanctions** | **US / UK / AU -- Evil Corp Designations Expanded**
> Further Evil Corp members designated, including Aleksandr Ryzhenkov, also charged as a LockBit affiliate. [Source: [Treasury jy2623](https://home.treasury.gov/news/press-releases/jy2623) (A)]

**2024-10** | **Provider Event** | **Angel Drainer Acquires Inferno Drainer**
> Angel Drainer acquires the Inferno Drainer cryptocurrency-theft toolkit, consolidating wallet-draining capabilities. *Not re-verified in the 2026-09 audit.*

**2024-09-26** | **Sanctions + LE Operation** | **Cryptex, PM2BTC and UAPS**
> OFAC designated Cryptex and Sergey Ivanov; FinCEN imposed a special measure against PM2BTC; DOJ (E.D. Va.) indicted Ivanov and Timur Shakhmametov, and domains were seized with the FIOD; rewards up to $10M. [Source: [Treasury jy2616](https://home.treasury.gov/news/press-releases/jy2616) (A)]

**2024-08-15** | **Provider Event** | **Femo IT/Defhost AS214351**
> AS214351 allocated seven days after Femo IT Solutions Ltd was incorporated in the UK (2024-08-08); RF assesses it is under Defhost control. [Source: RF-AUROLOGIC]

**2024-05-30** | **LE Operation** | **Operation Endgame (Original Phase)**
> Europol's "largest ever operation against botnets" (27-29 May) hit IcedID, SystemBC, Pikabot, Smokeloader, Bumblebee and Trickbot: 4 arrests, 100+ servers seized and 2,000+ domains taken down. [Source: [Europol](https://www.europol.europa.eu/media-press/newsroom/news/largest-ever-operation-against-botnets-hits-dropper-malware-ecosystem) (A, snippet)]

**2024-05-28** | **Sanctions + LE Operation** | **911 S5 Residential-Proxy Botnet Dismantled**
> OFAC designated administrator Yunhe Wang, Jingping Liu and Yanni Zheng and three Thai companies owned by Wang (E.O. 13694 as amended); Wang was arrested in Singapore. The botnet spread through free VPN apps and compromised machines behind more than 19M IPs. The best precedent for the database's anonymization/proxy-enabler type. [Source: [Treasury jy2375](https://home.treasury.gov/news/press-releases/jy2375) (A)]

**2024-05-10** | **Provider Event** | **KPROHOST LLC**
> KPROHOST LLC (Frankfort, Kentucky) registered via RIPE; Intrinsec later attributed its AS214940 to Virtualine. [Sources: RIPE-DB; INTRINSEC-FDN3-2025]

**2024-05-07** | **Sanctions** | **LockBit Administrator Khoroshev Designated and Indicted**
> OFAC, the UK and Australia designated Dmitry Khoroshev; DOJ (D.N.J.) unsealed an indictment. [Source: [NCA](https://www.nationalcrimeagency.gov.uk/news/lockbit-leader-unmasked-and-sanctioned) (A)]

**2024-03-28** | **Provider Event** | **Dolphon 1337 Ltd AS215208**
> Dolphon 1337 Ltd AS215208 reported registered via RIPE. *The earlier "ELITETEAM/1337TEAM" association rested only on the "1337" naming and has been removed; the ASN now belongs to an Indonesian ISP.* [Source: EXCEDO-ASN]

**2024-03-25** | **Sanctions** | **OFAC -- Bitpapa, Netex24 and Russian Crypto Venues**
> Designated under E.O. 14024; Bitpapa had been described in this repository as an active Garantex successor. [Source: [Treasury jy2204](https://home.treasury.gov/news/press-releases/jy2204) (A)]

**2024-02-19** | **LE Operation** | **Operation Cronos -- LockBit**
> NCA-led action with ten countries: 34 servers and more than 11,000 domains seized, 200+ crypto accounts frozen, about 1,000 decryption keys recovered, two arrests (Poland, Ukraine) and charges against five affiliates. LockBit later rebuilt and launched 5.0 in September 2025. [Source: [Akamai (archived)](https://github.com/mthcht/ThreatIntel-Reports/blob/main/Intel%20Reports/www_akamai_com/blog_security_2024_feb_learning-from-the-lockbit-takedown/content.txt) (B)]

**2024** | **Provider Event** | **Karina Rashkovska Entity**
> A RIPE registration in the name of an individual, Karina Rashkovska, is made (the 2024-01-03 date is unverified); HYAS later flagged it for RisePro C2. The ASN (AS215789) has since been re-issued to BLIK. [Sources: HYAS-RISEPRO; REGISTRY-SNAPSHOT-2026-09]

---

## 2023

**2023-11** | **Provider Event** | **aurologic GmbH Takes Over combahton's fastpipe**
> combahton announced the full transition of its fastpipe network to aurologic GmbH in November 2023; Recorded Future later identified aurologic as a central hub for malicious hosting. [Source: RF-AUROLOGIC]

**2023-09-29** | **Intelligence** | **Unit 42 -- Cl0p Distributes Stolen Data via Torrents**
> Unit 42 tracked Cl0p torrent seeders, including 95[.]215[.]0[.]76 on Petersburg Internet Network's PIN DC AS34665. [Source: UNIT42-CL0P-TORRENTS]

**2023-08** | **Intelligence** | **Halcyon / Cloudzy Exposure**
> Halcyon exposes Cloudzy as a front for the Iranian company abrNOC, run by Hassan Nozari, estimating that 40-60% of its overall activity could be malicious. [Source: HALCYON-CLOUDZY]

**2023-06-07** | **Intelligence** | **CISA/FBI AA23-158A -- Cl0p MOVEit (and GoAnywhere) IOCs**
> The joint advisory's IP lists (revised 16 June) include 19 addresses in HZ Hosting space: 10 from the January-February 2023 GoAnywhere campaign and 9 from MOVEit, with 79[.]141[.]160[.]78 in both. [Source: CISA-AA23-158A]

**2023-02-09** | **Sanctions** | **US / UK -- Trickbot/Conti Members Designated**
> Seven members designated in February (including Vitaly Kovalev, "Stern") and eleven more on 2023-09-07. [Source: [Treasury jy1256](https://home.treasury.gov/news/press-releases/jy1256) (A)]

**2023-01-18** | **Sanctions + LE Operation** | **FinCEN -- Bitzlato**
> FinCEN identified Bitzlato as a primary money-laundering concern (§9714) and DOJ arrested founder Anatoly Legkodymov. [Source: [Federal Register 2023-01189](https://www.federalregister.gov/documents/2023/01/23/2023-01189/imposition-of-special-measure-prohibiting-the-transmittal-of-funds-involving-bitzlato) (A)]

---

## 2022

**2022-04-05** | **Sanctions** | **OFAC -- Garantex (First Designation)**
> OFAC designated the Garantex cryptocurrency **exchange** alongside the Hydra darknet market (coordinated with Germany's BKA seizure of Hydra), citing more than $100M in illicit-actor transactions including about $6M from Conti. [Source: OFAC-GARANTEX]

**2022-02-10** | **Provider Event** | **Stark Industries Solutions Ltd Incorporated**
> Stark Industries Solutions Ltd incorporated in the United Kingdom (13906017) -- two weeks before Russia's full-scale invasion of Ukraine on 24 February 2022. The timing suggests pre-positioning of corporate infrastructure. [Source: UK-COMPANIES-HOUSE]

---

## 2021

**2021-02-22** | **Intelligence** | **Accellion FTA Exploitation Disclosed (Cl0p / UNC2546)**
> Mandiant and CISA (AA21-055A / MAR-10325064) published the Accellion FTA exploitation behind Cl0p's first data-theft extortion campaign (December 2020-January 2021); a DEWMODE webshell C2, 79[.]141[.]162[.]82, carried the netname HZ-NA23 in HZ Hosting space. [Sources: MANDIANT-ACCELLION-2021; CISA-AR21-055A; BLACKLOTUS-ACCELLION]

---

## 2020

**2020-11** | **Provider Event** | **ELITETEAM/1337TEAM ASNs Allocated**
> The 1337TEAM LIMITED ASNs were allocated in late 2020 (exact date unverified) to a Seychelles company at an address that appears in the Panama Papers/Offshore Leaks. The network is now dark, though Spamhaus still lists AS51381 and AS56873. [Source: TEAMCYMRU-ELITETEAM-2022]

---

## 2019

**2019** | **Provider Event** | **Garantex Founded**
> Garantex, a cryptocurrency exchange first registered in Estonia (licence revoked February 2022) and run from Moscow and St. Petersburg, begins operating; DOJ says it processed at least $96B from 2019 until its 2025 takedown. [Source: DOJ-GARANTEX-2025]
>
> *Corrected: an earlier "2016 -- Garantex mixing service created ... EUR 1.3B" entry conflated Garantex with Cryptomixer (see 2025-12-01).*

---

## Summary Statistics

### Sanctions Designations by Authority (BPH/TAE-relevant actions recorded above)

| Authority | Actions | Key Targets |
|-----------|---------|-------------|
| **OFAC (US)** | 19 | Garantex (2022; 2025 re-designation with Grinex and the A7 network), Trickbot/Conti (2023), Bitpapa (2024), Khoroshev (2024), 911 S5 (2024), Cryptex (2024), Evil Corp (2024), Zservers (2025), FUNNULL (2025), Aeza Group (2025), Prince Group (2025), Media Land and the Aeza follow-on (2025), Iranian exchanges (June and Aug 2026, plus the Economic Outcast action), Prince Group/Huione follow-on (2026), 1VPNS (2026), Xinbi (2026) |
| **EU** | 6 | Garantex (16th package, 2025-02-24), Stark Industries + Neculitis (Impl. Reg. 2025/965, 2025-05-20), A7A5 ban (19th package, 2025-10-23), CASP category ban (20th package, 2026-04-23), Media Land + ML.Cloud + Volosovik (Impl. Reg. 2026/1714, 2026-07-13), third-country crypto tool (21st package, 2026-07-23) |
| **UK** | 10 | Trickbot/Conti (2023), Khoroshev (2024), Evil Corp (2024), Zservers + XHOST LP (2025-02), Grinex + Old Vector (2025-08), Prince Group (2025-10), Media Land and Aeza Group LLC (2025-11), Xinbi (2026-03), crypto exchanges (2026-05), Lumma/GRU/CARR/Rybar (2026-07) |
| **Australia** | 4 | Khoroshev (2024), Evil Corp (2024), Zservers (2025-02), Media Land (2025-11) |
| **New Zealand** | 1 | Volosovik and 32 others (2026-08) |
| **FinCEN (311 / §9714)** | 4 | Bitzlato (2023), PM2BTC (2024), Huione Group (proposed May 2025; final Oct 2025), H-Pay successor rule (proposed June 2026) |

### Provider Enforcement Summary

| Metric | Count | Notes |
|--------|-------|-------|
| **Tracked entities under designation** | 15 | 13 with `status=sanctioned` in `BPH_Master.csv` (Aeza, Zservers, Media Land, FUNNULL, Hypercore, Datavice, Grinex, A7A5/Old Vector, Nobitex, Wallex, Bitpin, Ramzinex, 1VPNS) plus Stark Industries (`dissolved`) and Garantex (`evading`), whose designations stand. PQ Hosting Plus, CTG Server and StarCloud are **not** designated |
| **Providers seized/disrupted by LE** | 20+ | Garantex; LockBit (Cronos); Operation Talent incl. StarkRDP; XSS; breachforums.hn; Phobos/8Base; Zservers (127 servers); the press-attributed CrazyRDP seizure; Cryptomixer.io; eXch; Archetyp; NoName057(16); Endgame (2024; Apr, May, Nov 2025; June 2026); Huione backend infrastructure; the Asocks-attributed botnet; THE.Hosting/WorkTitans (FIOD); 1VPNS (Saffron); NetNut domains; QScan/QTRouter; Sality; NightmareStresser; Xinbi |
| **Providers that evaded via rebranding** | 6+ | Stark -> PQ Hosting Plus / THE.Hosting / WorkTitans B.V. / UFO Hosting; Garantex -> Grinex; Aeza -> Hypercore / Smart Digital Ideas / Datavice; Virtualine -> metaspinner-named AS209800 -> OMEGATECH; Huione -> Tudou -> H-Pay Service PLC / Xinbi; Proton66 -> Chang Way shell ASNs (likely) |
| **Individuals sanctioned (tracked providers)** | 25+ | Mishin, A. Bolshakov, Sidorov, D. Bolshakov, Odintsov, Ananev (Zservers); Neculiti x2 (Stark); Penzev, Bozoyan, Gast, Knyazev, Makarov, Zakirov (Aeza); Volosovik, Zatolokin, Pankova, Kozlov (Media Land); Liu Lizhi (FUNNULL); Mira Serda, Mendeleev, Karavatsky (Garantex/Grinex); four Nobitex executives; Hu Xiaowei (Prince Group/Huione); Rashevskyi, Silayev (1VPNS) |

### Evasion Velocity: Time from Sanctions/LE Action to Successor Entity

| Original Entity | Action Date | Successor Entity | Successor Date | Lag (Days) |
|----------------|-------------|-------------------|----------------|------------|
| Stark Industries | 2025-05-20 (EU sanctions) | UFO Hosting LLC (RIPE org) | 2025-03-13 | **-68** (pre-positioned) |
| Stark Industries | 2025-05-20 (EU sanctions) | PQ Hosting Plus S.R.L. (RIPE org) | 2025-05-13 | **-7** (pre-positioned) |
| Stark Industries | 2025-05-20 (EU sanctions) | AS44477 transfer to PQ Hosting Plus | 2025-05-16 | **-4** (pre-positioned) |
| Stark Industries | 2025-05-20 (EU sanctions) | THE.Hosting rebrand | 2025-05-29 | **+9** |
| Stark Industries | 2025-05-20 (EU sanctions) | WorkTitans B.V. AS209847 | 2025-06-24 | **+35** |
| Garantex | 2025-03-06 (seized) | Grinex (registered) | 2024-12 | **~-90** (pre-positioned) |
| Aeza Group | 2025-07-01 (OFAC) | Datavice MCHJ (established) | 2025-07-03 | **+2** |
| Aeza Group | 2025-07-01 (OFAC) | Hypercore AS211522 (allocated) / IP migration | ~2025-07-10 / 2025-07-20 | **+9 / +19** |
| Huione Guarantee | 2025-05 (FinCEN proposed rule; Telegram bans) | Tudou Guarantee (stake announced) -> H-Pay Service PLC | 2024-12 | **~-150** (pre-positioned; 30+ successor marketplaces emerged) |

### Key Analytical Pattern

> **Evasion lead time: usually negative, never long.** In the Stark case successors were pre-positioned: UFO Hosting 68 days before the EU listing, PQ Hosting Plus 7 days before, and the AS44477 transfer 4 days before; the THE.Hosting rebrand followed nine days after. Garantex's successor Grinex was registered about three months before the takedown. Aeza's fronts came *after* the designation but within days (Datavice +2, Hypercore +9 to +19). Either way, sanctioned entities re-emerge faster than designations follow -- effective enforcement targets successors in the same action, as OFAC's August 2025 Garantex re-designation did with Grinex and the A7 network.

> **Takedowns redistribute demand.** Intel 471 found about 80% of Media Land's customer domains still online months after sanctions and indictment, with demand shifting to mainstream clouds and new fast-flux services; routing data shows the same pattern at ASN level -- dark or re-issued ASNs and fresh sibling ASNs appearing on Spamhaus ASN-DROP. See taxonomy §3.9.

> **2026 regime shift -- from named entities to categories and corridors.** The EU's 20th package (2026-04-23) banned a whole category -- Russia- and Belarus-based crypto-asset service providers -- which a new successor cannot escape by being new, and the 21st package (2026-07-23) added a tool to ban third-country corridors. On the US side, E.O. 14390 (2026-03-06) set a coordination mandate but created **no new sanctions authority** (2026 designations still rest on orders such as E.O. 13694; Prince Group was designated as a transnational criminal organisation), while the 2026-08-12 Presidential Memorandum opened a channel for private-sector "cyber effects" operations against foreign cyber-enabled crime groups. Category bans reduce the leverage of successor tracking for *compliance blocking*; successor tracking remains essential for *attribution and infrastructure mapping*.

---

*This timeline is maintained as a living document. Entries will be updated as new sanctions, enforcement actions, and evasion events are identified.*

*CrimsonVector Research -- BPH & TAE Intelligence Program*
