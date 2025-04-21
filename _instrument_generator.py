# https://freeserv.dukascopy.com/2.0/index.php?path=common%2Finstruments&jsonp=_callbacks_._1m9mtpe0f

groups={
  "FX": {
    "id": "FX",
    "title": "Forex"
  },
  "CMD": {
    "id": "CMD",
    "title": "Commodities (CFD)"
  },
  "IDX": {
    "id": "IDX",
    "title": "Indices (CFD)",
    "instruments": ["PRT.IDX/EUR"]
  },
  "BND_CFD": {
    "id": "BND_CFD",
    "title": "Bonds (CFD)",
    "instruments": ["BUND.TR/EUR", "UKGILT.TR/GBP", "USTBOND.TR/USD"]
  },
  "STCK_CFD": {
    "id": "STCK_CFD",
    "title": "Stocks (CFD)"
  },
  "ETF_CFD": {
    "id": "ETF_CFD",
    "title": "ETF (CFD)",
    "instruments": ["ARKI.US/USD", "BUGG.GB/GBP", "CSH2.FR/EUR", "CSH2.GB/GBX", "CYSE.GB/GBX", "ESIH.GB/GBP", "IGLN.US/USD", "IUFS.US/USD", "SEMI.GB/GBP", "SGLD.US/USD", "SMH.US/USD", "SMTC.US/USD", "WTAI.US/USD", "XDER.GB/GBX", "XDWH.US/USD", "XDWT.US/USD"]
  },
  "VCCY": {
    "id": "VCCY",
    "title": "Crypto (CFD)",
    "instruments": ["ADA/USD", "AVE/USD", "BAT/USD", "BCH/CHF", "BCH/EUR", "BCH/GBP", "BCH/USD", "BTC/CHF", "BTC/EUR", "BTC/GBP", "BTC/USD", "CMP/USD", "DSH/USD", "ENJ/USD", "EOS/USD", "ETH/CHF", "ETH/EUR", "ETH/GBP", "ETH/USD", "LNK/USD", "LTC/CHF", "LTC/EUR", "LTC/GBP", "LTC/USD", "MAT/USD", "MKR/USD", "TRX/USD", "UNI/USD", "UST/USD", "XLM/CHF", "XLM/EUR", "XLM/GBP", "XLM/USD", "XMR/USD", "XRP/USD", "YFI/USD"]
  },
  "CMD_AGRICULTURAL": {
    "id": "CMD_AGRICULTURAL",
    "title": "Agricultural",
    "parent": "CMD",
    "instruments": ["COCOA.CMD/USD", "COFFEE.CMD/USX", "COTTON.CMD/USX", "OJUICE.CMD/USX", "SOYBEAN.CMD/USX", "SUGAR.CMD/USD"]
  },
  "CMD_ENERGY": {
    "id": "CMD_ENERGY",
    "title": "Energy",
    "parent": "CMD",
    "instruments": ["DIESEL.CMD/USD", "E_Brent", "E_Light", "GAS.CMD/USD"]
  },
  "CMD_METALS": {
    "id": "CMD_METALS",
    "title": "Metals",
    "parent": "CMD",
    "instruments": ["COPPER.CMD/USD", "XPD.CMD/USD", "XPT.CMD/USD"]
  },
  "ETF_CFD_DE": {
    "id": "ETF_CFD_DE",
    "title": "Germany",
    "parent": "ETF_CFD",
    "instruments": ["TECDAXE.DE/EUR"]
  },
  "ETF_CFD_FR": {
    "id": "ETF_CFD_FR",
    "title": "France",
    "parent": "ETF_CFD",
    "instruments": ["DSB.FR/EUR", "LVC.FR/EUR", "LYXBNK.FR/EUR"]
  },
  "ETF_CFD_HK": {
    "id": "ETF_CFD_HK",
    "title": "Hong Kong",
    "parent": "ETF_CFD",
    "instruments": ["2822.HK/HKD", "2828.HK/HKD", "2833.HK/HKD", "2836.HK/HKD", "3188.HK/HKD"]
  },
  "ETF_CFD_US": {
    "id": "ETF_CFD_US",
    "title": "US",
    "parent": "ETF_CFD",
    "instruments": ["ARKQ.US/USD", "ARKX.US/USD", "AWAY.US/USD", "BITO.US/USD", "BTF.US/USD", "DIA.US/USD", "DVY.US/USD", "EEM.US/USD", "EFA.US/USD", "EMB.US/USD", "ESPO.US/USD", "EWH.US/USD", "EWJ.US/USD", "EWW.US/USD", "EWZ.US/USD", "EZU.US/USD", "FINX.US/USD", "FTXG.US/USD", "FXI.US/USD", "GDX.US/USD", "GDXJ.US/USD", "GLD.US/USD", "IAK.US/USD", "IBB.US/USD", "IEF.US/USD", "IJH.US/USD", "IJR.US/USD", "ITA.US/USD", "IVE.US/USD", "IVW.US/USD", "IWD.US/USD", "IWF.US/USD", "IWM.US/USD", "IYR.US/USD", "JETS.US/USD", "JNK.US/USD", "KIE.US/USD", "KRE.US/USD", "PBJ.US/USD", "PEJ.US/USD", "PPA.US/USD", "QQQ.US/USD", "ROBO.US/USD", "SLV.US/USD", "SPY.US/USD", "TLT.US/USD", "USO.US/USD", "VDE.US/USD", "VEA.US/USD", "VGK.US/USD", "VNQ.US/USD", "VXX.US/USD", "XLE.US/USD", "XLF.US/USD", "XLI.US/USD", "XLK.US/USD", "XLP.US/USD", "XLU.US/USD", "XLV.US/USD", "XLY.US/USD", "XOP.US/USD", "XRES.US/USD"]
  },
  "FX_CROSSES": {
    "id": "FX_CROSSES",
    "title": "Crosses",
    "parent": "FX",
    "instruments": ["AUD/CAD", "AUD/CHF", "AUD/JPY", "AUD/NZD", "AUD/SGD", "CAD/CHF", "CAD/HKD", "CAD/JPY", "CHF/JPY", "CHF/PLN", "CHF/SGD", "EUR/AUD", "EUR/CAD", "EUR/CHF", "EUR/CZK", "EUR/DKK", "EUR/GBP", "EUR/HKD", "EUR/HUF", "EUR/JPY", "EUR/MXN", "EUR/NOK", "EUR/NZD", "EUR/PLN", "EUR/RUB", "EUR/SEK", "EUR/SGD", "EUR/TRY", "EUR/ZAR", "GBP/AUD", "GBP/CAD", "GBP/CHF", "GBP/JPY", "GBP/NZD", "HKD/JPY", "MXN/JPY", "NZD/CAD", "NZD/CHF", "NZD/JPY", "NZD/SGD", "SGD/JPY", "TRY/JPY", "USD/BRL", "USD/CNH", "USD/CZK", "USD/DKK", "USD/HKD", "USD/HUF", "USD/ILS", "USD/MXN", "USD/NOK", "USD/NZD", "USD/PLN", "USD/RON", "USD/RUB", "USD/SEK", "USD/SGD", "USD/THB", "USD/TRY", "USD/ZAR", "ZAR/JPY"]
  },
  "FX_MAJORS": {
    "id": "FX_MAJORS",
    "title": "Majors",
    "parent": "FX",
    "instruments": ["AUD/USD", "EUR/USD", "GBP/USD", "NZD/USD", "USD/CAD", "USD/CHF", "USD/JPY"]
  },
  "FX_METALS": {
    "id": "FX_METALS",
    "title": "Metals",
    "parent": "FX",
    "instruments": ["XAG/USD", "XAU/USD"]
  },
  "IDX_AMERICA": {
    "id": "IDX_AMERICA",
    "title": "America",
    "parent": "IDX",
    "instruments": ["DOLLAR.IDX/USD", "E_D&J-Ind", "E_NQ-100", "E_SandP-500", "RUSSELL.IDX/USD", "USSC2000.IDX/USD", "VOL.IDX/USD"]
  },
  "IDX_ASIA": {
    "id": "IDX_ASIA",
    "title": "Asia / Pacific",
    "parent": "IDX",
    "instruments": ["CHI.IDX/USD", "E_H-Kong", "E_N225Jap", "E_XJO-ASX", "IND.IDX/USD", "SGD.IDX/SGD"]
  },
  "IDX_EUROPE": {
    "id": "IDX_EUROPE",
    "title": "Europe",
    "parent": "IDX",
    "instruments": ["E_CAAC-40", "E_DAAX", "E_DJE50XX", "E_Futsee-100", "E_IBC-MAC", "E_SWMI", "ITA.IDX/EUR", "NLD.IDX/EUR", "PLN.IDX/PLN"]
  },
  "IDX_AFRICA": {
    "id": "IDX_AFRICA",
    "title": "Africa",
    "parent": "IDX",
    "instruments": ["SOA.IDX/ZAR"]
  },
  "Australia": {
    "id": "Australia",
    "title": "Australia",
    "parent": "STCK_CFD"
  },
  "Austria": {
    "id": "Austria",
    "title": "Austria",
    "parent": "STCK_CFD",
    "instruments": ["ANDR.AT/EUR", "EBS.AT/EUR", "POST.AT/EUR", "RBI.AT/EUR", "TKA.AT/EUR", "VER.AT/EUR", "VIG.AT/EUR", "VOE.AT/EUR", "WIE.AT/EUR"]
  },
  "Belgium": {
    "id": "Belgium",
    "title": "Belgium",
    "parent": "STCK_CFD",
    "instruments": ["ABI.BE/EUR", "AGS.BE/EUR", "BELG.BE/EUR", "KBC.BE/EUR", "SOLB.BE/EUR", "UCB.BE/EUR", "UMI.BE/EUR"]
  },
  "Denmark": {
    "id": "Denmark",
    "title": "Denmark",
    "parent": "STCK_CFD",
    "instruments": ["CARLB.DK/DKK", "COLOB.DK/DKK", "DANSKE.DK/DKK", "MAERSKB.DK/DKK", "NOVOB.DK/DKK", "NZYMB.DK/DKK", "PNDORA.DK/DKK", "VWS.DK/DKK"]
  },
  "Finland": {
    "id": "Finland",
    "title": "Finland",
    "parent": "STCK_CFD",
    "instruments": ["CGCBV.FI/EUR", "ELI1V.FI/EUR", "NES1V.FI/EUR", "NRE1V.FI/EUR", "OTE1V.FI/EUR", "OUT1V.FI/EUR", "STERV.FI/EUR", "TLS1V.FI/EUR"]
  },
  "France": {
    "id": "France",
    "title": "France",
    "parent": "STCK_CFD",
    "instruments": ["AC.FR/EUR", "ACA.FR/EUR", "AF.FR/EUR", "AI.FR/EUR", "AIR.FR/EUR", "ALO.FR/EUR", "ATO.FR/EUR", "BN.FR/EUR", "BNP.FR/EUR", "CA.FR/EUR", "CAP.FR/EUR", "CS.FR/EUR", "DG.FR/EUR", "DSY.FR/EUR", "EDF.FR/EUR", "EI.FR/EUR", "EN.FR/EUR", "ENGI.FR/EUR", "FP.FR/EUR", "FR.FR/EUR", "GLE.FR/EUR", "HO.FR/EUR", "KER.FR/EUR", "LI.FR/EUR", "LR.FR/EUR", "MC.FR/EUR", "ML.FR/EUR", "OR.FR/EUR", "ORA.FR/EUR", "PUB.FR/EUR", "RI.FR/EUR", "RMS.FR/EUR", "RNO.FR/EUR", "SAF.FR/EUR", "SAN.FR/EUR", "SGO.FR/EUR", "SU.FR/EUR", "SW.FR/EUR", "TEC.FR/EUR", "UG.FR/EUR", "VIE.FR/EUR", "VIV.FR/EUR", "VK.FR/EUR"]
  },
  "Germany": {
    "id": "Germany",
    "title": "Germany",
    "parent": "STCK_CFD",
    "instruments": ["ADS.DE/EUR", "ALV.DE/EUR", "BAS.DE/EUR", "BAYN.DE/EUR", "BEI.DE/EUR", "BMW.DE/EUR", "BNR.DE/EUR", "BOSS.DE/EUR", "CBK.DE/EUR", "CON.DE/EUR", "COV.DE/EUR", "DAI.DE/EUR", "DB1.DE/EUR", "DBK.DE/EUR", "DHR.DE/EUR", "DPW.DE/EUR", "DTE.DE/EUR", "EOAN.DE/EUR", "FME.DE/EUR", "FRE.DE/EUR", "HEI.DE/EUR", "HEN3.DE/EUR", "HFG.DE/EUR", "HNR.DE/EUR", "IFX.DE/EUR", "LHA.DE/EUR", "LIN.DE/EUR", "LXS.DE/EUR", "MRK.DE/EUR", "MTX.DE/EUR", "MUV2.DE/EUR", "PAH3.DE/EUR", "PSM.DE/EUR", "PUM.DE/EUR", "RWE.DE/EUR", "SAP.DE/EUR", "SDF.DE/EUR", "SIE.DE/EUR", "SRT.DE/EUR", "SY1.DE/EUR", "TKA.DE/EUR", "TUI1.DE/EUR", "VNA.DE/EUR", "VOW3.DE/EUR"]
  },
  "Hong Kong": {
    "id": "Hong Kong",
    "title": "Hong Kong",
    "parent": "STCK_CFD",
    "instruments": ["0005.HK/HKD", "0027.HK/HKD", "0175.HK/HKD", "0291.HK/HKD", "0386.HK/HKD", "0388.HK/HKD", "0700.HK/HKD", "0857.HK/HKD", "0883.HK/HKD", "0939.HK/HKD", "0941.HK/HKD", "0998.HK/HKD", "1093.HK/HKD", "1177.HK/HKD", "1288.HK/HKD", "1299.HK/HKD", "1398.HK/HKD", "1810.HK/HKD", "1918.HK/HKD", "2007.HK/HKD", "2018.HK/HKD", "2318.HK/HKD", "2388.HK/HKD", "2628.HK/HKD", "3333.HK/HKD", "3968.HK/HKD", "3988.HK/HKD"]
  },
  "Hungary": {
    "id": "Hungary",
    "title": "Hungary",
    "parent": "STCK_CFD"
  },
  "Ireland": {
    "id": "Ireland",
    "title": "Ireland",
    "parent": "STCK_CFD",
    "instruments": ["BIRG.IE/EUR", "CRG.IE/EUR", "KRX.IE/EUR", "KRZ.IE/EUR", "RY4C.IE/EUR"]
  },
  "Italy": {
    "id": "Italy",
    "title": "Italy",
    "parent": "STCK_CFD",
    "instruments": ["A2A.IT/EUR", "AGL.IT/EUR", "AMP.IT/EUR", "ATL.IT/EUR", "AZM.IT/EUR", "BAMI.IT/EUR", "BC.IT/EUR", "BMPS.IT/EUR", "BPE.IT/EUR", "BRE.IT/EUR", "BZU.IT/EUR", "CASS.IT/EUR", "CERV.IT/EUR", "CPR.IT/EUR", "CVAL.IT/EUR", "DAN.IT/EUR", "DEA.IT/EUR", "DIA.IT/EUR", "ENEL.IT/EUR", "ENI.IT/EUR", "ERG.IT/EUR", "FBK.IT/EUR", "FCA.IT/EUR", "G.IT/EUR", "IG.IT/EUR", "INW.IT/EUR", "ISP.IT/EUR", "JUVE.IT/EUR", "LDO.IT/EUR", "MB.IT/EUR", "MONC.IT/EUR", "MS.IT/EUR", "PIA.IT/EUR", "PRY.IT/EUR", "RACE.IT/EUR", "REC.IT/EUR", "SFER.IT/EUR", "SPM.IT/EUR", "SRG.IT/EUR", "SRS.IT/EUR", "STM.IT/EUR", "TEN.IT/EUR", "TIS.IT/EUR", "TIT.IT/EUR", "TOD.IT/EUR", "TRN.IT/EUR", "UCG.IT/EUR", "US.IT/EUR", "WBD.IT/EUR"]
  },
  "Japan": {
    "id": "Japan",
    "title": "Japan",
    "parent": "STCK_CFD",
    "instruments": ["2502.JP/JPY", "2503.JP/JPY", "2914.JP/JPY", "3382.JP/JPY", "3436.JP/JPY", "4004.JP/JPY", "4005.JP/JPY", "4063.JP/JPY", "4452.JP/JPY", "4502.JP/JPY", "4503.JP/JPY", "4507.JP/JPY", "4523.JP/JPY", "4543.JP/JPY", "4689.JP/JPY", "4911.JP/JPY", "5108.JP/JPY", "5301.JP/JPY", "5401.JP/JPY", "6098.JP/JPY", "6301.JP/JPY", "6367.JP/JPY", "6501.JP/JPY", "6502.JP/JPY", "6503.JP/JPY", "6506.JP/JPY", "6702.JP/JPY", "6752.JP/JPY", "6758.JP/JPY", "6762.JP/JPY", "6902.JP/JPY", "6954.JP/JPY", "6971.JP/JPY", "7201.JP/JPY", "7203.JP/JPY", "7261.JP/JPY", "7267.JP/JPY", "7269.JP/JPY", "7270.JP/JPY", "7751.JP/JPY", "7974.JP/JPY", "8031.JP/JPY", "8035.JP/JPY", "8306.JP/JPY", "8316.JP/JPY", "8411.JP/JPY", "8766.JP/JPY", "8801.JP/JPY", "8802.JP/JPY", "9020.JP/JPY", "9432.JP/JPY", "9433.JP/JPY", "9437.JP/JPY", "9501.JP/JPY", "9983.JP/JPY", "9984.JP/JPY"]
  },
  "Mexico": {
    "id": "Mexico",
    "title": "Mexico",
    "parent": "STCK_CFD",
    "instruments": ["ALFAA.MX/MXN", "ALSEA.MX/MXN", "AMXL.MX/MXN", "ARCA.MX/MXN", "ASURB.MX/MXN", "BBAJIOO.MX/MXN", "BOLSAA.MX/MXN", "CEMEXCPO.MX/MXN", "ELEKTRA.MX/MXN", "FEMSAUBD.MX/MXN", "GAPB.MX/MXN", "GCARSOA1.MX/MXN", "GCC.MX/MXN", "GFNORTEO.MX/MXN", "GMEXICOB.MX/MXN", "GRUMAB.MX/MXN", "KIMBERA.MX/MXN", "KOFUBL.MX/MXN", "LABB.MX/MXN", "LIVEPOLC1.MX/MXN", "MEGACPO.MX/MXN", "OMAB.MX/MXN", "ORBIA.MX/MXN", "PEOLES.MX/MXN", "PINFRA.MX/MXN", "Q.MX/MXN", "RA.MX/MXN", "VOLARA.MX/MXN", "WALMEX.MX/MXN"]
  },
  "Netherlands": {
    "id": "Netherlands",
    "title": "Netherlands",
    "parent": "STCK_CFD",
    "instruments": ["AGN.NL/EUR", "AH.NL/EUR", "AKZA.NL/EUR", "ASML.NL/EUR", "DSM.NL/EUR", "GTO.NL/EUR", "HEIA.NL/EUR", "INGA.NL/EUR", "KPN.NL/EUR", "MT.NL/EUR", "PHIA.NL/EUR", "QIA.NL/EUR", "RAND.NL/EUR", "RDSA.NL/EUR", "REN.NL/EUR", "UL.NL/EUR", "UNA.NL/EUR", "VPK.NL/EUR", "WKL.NL/EUR"]
  },
  "Norway": {
    "id": "Norway",
    "title": "Norway",
    "parent": "STCK_CFD",
    "instruments": ["DNB.NO/NOK", "DNO.NO/NOK", "FOE.NO/NOK", "MHG.NO/NOK", "NAS.NO/NOK", "NHY.NO/NOK", "ORK.NO/NOK", "PGS.NO/NOK", "SCH.NO/NOK", "STB.NO/NOK", "STL.NO/NOK", "SUBC.NO/NOK", "TEL.NO/NOK", "YAR.NO/NOK"]
  },
  "Poland": {
    "id": "Poland",
    "title": "Poland",
    "parent": "STCK_CFD"
  },
  "Portugal": {
    "id": "Portugal",
    "title": "Portugal",
    "parent": "STCK_CFD",
    "instruments": ["EDP.PT/EUR", "GALP.PT/EUR"]
  },
  "Singapore": {
    "id": "Singapore",
    "title": "Singapore",
    "parent": "STCK_CFD"
  },
  "South Africa": {
    "id": "South Africa",
    "title": "South Africa",
    "parent": "STCK_CFD"
  },
  "Spain": {
    "id": "Spain",
    "title": "Spain",
    "parent": "STCK_CFD",
    "instruments": ["ABE.ES/EUR", "ACS.ES/EUR", "ACX.ES/EUR", "AENA.ES/EUR", "AMS.ES/EUR", "APP.ES/EUR", "BBVA.ES/EUR", "CABK.ES/EUR", "DIA.ES/EUR", "EBR.ES/EUR", "ELE.ES/EUR", "ENG.ES/EUR", "FCC.ES/EUR", "FER.ES/EUR", "GAM.ES/EUR", "GAS.ES/EUR", "GRF.ES/EUR", "IBE.ES/EUR", "ITX.ES/EUR", "MAP.ES/EUR", "POP.ES/EUR", "REE.ES/EUR", "REP.ES/EUR", "SAB.ES/EUR", "SAN.ES/EUR", "TEF.ES/EUR", "VIS.ES/EUR"]
  },
  "Sweden": {
    "id": "Sweden",
    "title": "Sweden",
    "parent": "STCK_CFD",
    "instruments": ["ABB.SE/SEK", "ALFA.SE/SEK", "ATCOA.SE/SEK", "AZN.SE/SEK", "ELUXB.SE/SEK", "ERICB.SE/SEK", "GETIB.SE/SEK", "HMB.SE/SEK", "INVEB.SE/SEK", "NDA.SE/SEK", "SAND.SE/SEK", "SCAB.SE/SEK", "SEBA.SE/SEK", "SECUB.SE/SEK", "SKAB.SE/SEK", "SKFB.SE/SEK", "SWEDA.SE/SEK", "SWMA.SE/SEK", "TEL2B.SE/SEK", "TLSN.SE/SEK", "VOLVB.SE/SEK"]
  },
  "Switzerland": {
    "id": "Switzerland",
    "title": "Switzerland",
    "parent": "STCK_CFD",
    "instruments": ["ABBN.CH/CHF", "ADEN.CH/CHF", "ATLN.CH/CHF", "BAER.CH/CHF", "CFR.CH/CHF", "CLN.CH/CHF", "CSGN.CH/CHF", "GALN.CH/CHF", "GIVN.CH/CHF", "KNIN.CH/CHF", "LHN.CH/CHF", "LISP.CH/CHF", "LOGN.CH/CHF", "LONN.CH/CHF", "MBTN.CH/CHF", "NESN.CH/CHF", "NOVN.CH/CHF", "OERL.CH/CHF", "ROG.CH/CHF", "SCMN.CH/CHF", "SGSN.CH/CHF", "SIK.CH/CHF", "SLHN.CH/CHF", "SOON.CH/CHF", "SREN.CH/CHF", "SYNN.CH/CHF", "TEMN.CH/CHF", "UBSG.CH/CHF", "UHR.CH/CHF", "UHRN.CH/CHF", "VIFN.CH/CHF", "ZURN.CH/CHF"]
  },
  "UK": {
    "id": "UK",
    "title": "UK",
    "parent": "STCK_CFD",
    "instruments": ["AAL.GB/GBX", "ABF.GB/GBX", "ADM.GB/GBX", "ADN.GB/GBX", "AGK.GB/GBX", "AHT.GB/GBX", "AMFW.GB/GBX", "ANTO.GB/GBX", "AV.GB/GBX", "AVST.GB/GBX", "AVV.GB/GBX", "AZN.GB/GBX", "BA.GB/GBX", "BAB.GB/GBX", "BARC.GB/GBX", "BATS.GB/GBX", "BDEV.GB/GBX", "BLND.GB/GBX", "BLT.GB/GBX", "BNZL.GB/GBX", "BP.GB/GBX", "BRBY.GB/GBX", "BT.GB/GBX", "CCL.GB/GBX", "CNA.GB/GBX", "CPG.GB/GBX", "CPI.GB/GBX", "CRDA.GB/GBX", "CRH.GB/GBX", "DCC.GB/GBX", "DGE.GB/GBX", "DPH.GB/GBX", "ECM.GB/GBX", "EXPN.GB/GBX", "EZJ.GB/GBX", "FRES.GB/GBX", "GFS.GB/GBX", "GKN.GB/GBX", "GLEN.GB/GBX", "GSK.GB/GBX", "HIK.GB/GBX", "HL.GB/GBX", "HLMA.GB/GBX", "HMSO.GB/GBX", "HSBA.GB/GBX", "IAG.GB/GBX", "ICP.GB/GBX", "IHG.GB/GBX", "III.GB/GBX", "IMI.GB/GBX", "IMT.GB/GBX", "INTU.GB/GBX", "ISAT.GB/GBX", "ITRK.GB/GBX", "ITV.GB/GBX", "KGF.GB/GBX", "LAND.GB/GBX", "LGEN.GB/GBX", "LLOY.GB/GBX", "LSE.GB/GBX", "MGGT.GB/GBX", "MKS.GB/GBX", "MNDI.GB/GBX", "MNG.GB/GBX", "MRW.GB/GBX", "NG.GB/GBX", "NXT.GB/GBX", "OCDO.GB/GBX", "OML.GB/GBX", "PFC.GB/GBX", "PHNX.GB/GBX", "PRU.GB/GBX", "PSN.GB/GBX", "PSON.GB/GBX", "RB.GB/GBX", "RBS.GB/GBX", "RDSB.GB/GBX", "REL.GB/GBX", "RIO.GB/GBX", "RMG.GB/GBX", "RMV.GB/GBX", "RR.GB/GBX", "RRS.GB/GBX", "RSA.GB/GBX", "RTO.GB/GBX", "SBRY.GB/GBX", "SDR.GB/GBX", "SGE.GB/GBX", "SGRO.GB/GBX", "SHP.GB/GBX", "SKY.GB/GBX", "SL.GB/GBX", "SLA.GB/GBX", "SMDS.GB/GBX", "SMIN.GB/GBX", "SMT.GB/GBX", "SN.GB/GBX", "SPD.GB/GBX", "SPX.GB/GBX", "SSE.GB/GBX", "STAN.GB/GBX", "STJ.GB/GBX", "SVT.GB/GBX", "TATE.GB/GBX", "TLW.GB/GBX", "TPK.GB/GBX", "TSCO.GB/GBX", "TUI.GB/GBX", "TW.GB/GBX", "ULVR.GB/GBX", "UU.GB/GBX", "VED.GB/GBX", "VOD.GB/GBX", "WEIR.GB/GBX", "WOS.GB/GBX", "WPP.GB/GBX", "WTB.GB/GBX"]
  },
  "US": {
    "id": "US",
    "title": "US",
    "parent": "STCK_CFD",
    "instruments": ["A.US/USD", "AA.US/USD", "AABA.US/USD", "AABV.US/USD", "AAL.US/USD", "AAP.US/USD", "AAPL.US/USD", "ABC.US/USD", "ABEV.US/USD", "ABMD.US/USD", "ABT.US/USD", "ACGL.US/USD", "ACM.US/USD", "ACN.US/USD", "ADBE.US/USD", "ADI.US/USD", "ADP.US/USD", "ADSK.US/USD", "AEP.US/USD", "AET.US/USD", "AFG.US/USD", "AGNC.US/USD", "AIG.US/USD", "AJG.US/USD", "ALB.US/USD", "ALGN.US/USD", "ALK.US/USD", "ALKS.US/USD", "ALL.US/USD", "ALLE.US/USD", "ALLY.US/USD", "ALNY.US/USD", "ALXN.US/USD", "AMAT.US/USD", "AMCR.US/USD", "AMD.US/USD", "AMGN.US/USD", "AMH.US/USD", "AMP.US/USD", "AMT.US/USD", "AMWL.US/USD", "AMZN.US/USD", "ANET.US/USD", "ANSS.US/USD", "ANTM.US/USD", "AON.US/USD", "AOS.US/USD", "APA.US/USD", "APC.US/USD", "APD.US/USD", "APTV.US/USD", "AR.US/USD", "ARE.US/USD", "ARMK.US/USD", "ARW.US/USD", "ATO.US/USD", "ATVI.US/USD", "AVB.US/USD", "AVGO.US/USD", "AVLR.US/USD", "AVTR.US/USD", "AWK.US/USD", "AXP.US/USD", "AXTA.US/USD", "AYX.US/USD", "AZN.US/USD", "AZO.US/USD", "AZPN.US/USD", "BA.US/USD", "BABA.US/USD", "BAC.US/USD", "BAH.US/USD", "BBD.US/USD", "BBT.US/USD", "BBWI.US/USD", "BBY.US/USD", "BDX.US/USD", "BERY.US/USD", "BG.US/USD", "BIDU.US/USD", "BIIB.US/USD", "BIO.US/USD", "BK.US/USD", "BKI.US/USD", "BKR.US/USD", "BLK.US/USD", "BMRN.US/USD", "BMY.US/USD", "BP.US/USD", "BPOP.US/USD", "BR.US/USD", "BRKB.US/USD", "BRKR.US/USD", "BRO.US/USD", "BRX.US/USD", "BSX.US/USD", "BURL.US/USD", "BWA.US/USD", "BYND.US/USD", "C.US/USD", "CACC.US/USD", "CACI.US/USD", "CAG.US/USD", "CAH.US/USD", "CARR.US/USD", "CASY.US/USD", "CAT.US/USD", "CB.US/USD", "CBOE.US/USD", "CBS.US/USD", "CCI.US/USD", "CCK.US/USD", "CCL.US/USD", "CDAY.US/USD", "CDEV.US/USD", "CDK.US/USD", "CDNS.US/USD", "CDW.US/USD", "CE.US/USD", "CELG.US/USD", "CERN.US/USD", "CF.US/USD", "CFG.US/USD", "CFR.US/USD", "CGNX.US/USD", "CHD.US/USD", "CHNG.US/USD", "CI.US/USD", "CL.US/USD", "CLR.US/USD", "CMCSA.US/USD", "CME.US/USD", "CMG.US/USD", "CMI.US/USD", "CNC.US/USD", "COF.US/USD", "COHR.US/USD", "COL.US/USD", "COLD.US/USD", "COO.US/USD", "COP.US/USD", "COST.US/USD", "COUP.US/USD", "CPRI.US/USD", "CPRT.US/USD", "CPT.US/USD", "CRL.US/USD", "CRM.US/USD", "CS.US/USD", "CSCO.US/USD", "CSGP.US/USD", "CSL.US/USD", "CSX.US/USD", "CTL.US/USD", "CTLT.US/USD", "CTSH.US/USD", "CTVA.US/USD", "CTXS.US/USD", "CUBE.US/USD", "CVNA.US/USD", "CVS.US/USD", "CVX.US/USD", "CZR.US/USD", "D.US/USD", "DAL.US/USD", "DBX.US/USD", "DE.US/USD", "DELL.US/USD", "DFS.US/USD", "DG.US/USD", "DHI.US/USD", "DHR.US/USD", "DIS.US/USD", "DKS.US/USD", "DLR.US/USD", "DLTR.US/USD", "DOCU.US/USD", "DOX.US/USD", "DPZ.US/USD", "DRE.US/USD", "DT.US/USD", "DUK.US/USD", "DVA.US/USD", "DVN.US/USD", "DXC.US/USD", "DXCM.US/USD", "EA.US/USD", "EBAY.US/USD", "EEFT.US/USD", "EFX.US/USD", "EHC.US/USD", "EIX.US/USD", "EL.US/USD", "ELAN.US/USD", "ELS.US/USD", "EMR.US/USD", "ENPH.US/USD", "ENTG.US/USD", "EOG.US/USD", "EPAM.US/USD", "EQH.US/USD", "EQT.US/USD", "ES.US/USD", "ESRX.US/USD", "ESS.US/USD", "ESTC.US/USD", "ETN.US/USD", "ETSY.US/USD", "EVRG.US/USD", "EW.US/USD", "EWBC.US/USD", "EXC.US/USD", "EXEL.US/USD", "EXPE.US/USD", "EXR.US/USD", "F.US/USD", "FANG.US/USD", "FB.US/USD", "FBHS.US/USD", "FCNCA.US/USD", "FCX.US/USD", "FDS.US/USD", "FDX.US/USD", "FE.US/USD", "FICO.US/USD", "FITB.US/USD", "FIVE.US/USD", "FL.US/USD", "FLT.US/USD", "FND.US/USD", "FNF.US/USD", "FOXA.US/USD", "FRC.US/USD", "FTI.US/USD", "FTNT.US/USD", "FTV.US/USD", "G.US/USD", "GD.US/USD", "GDDY.US/USD", "GE.US/USD", "GGG.US/USD", "GH.US/USD", "GILD.US/USD", "GIS.US/USD", "GL.US/USD", "GLPI.US/USD", "GLW.US/USD", "GM.US/USD", "GNRC.US/USD", "GOOG.US/USD", "GOOGL.US/USD", "GPN.US/USD", "GPS.US/USD", "GS.US/USD", "GWW.US/USD", "H.US/USD", "HAL.US/USD", "HBI.US/USD", "HCA.US/USD", "HCN.US/USD", "HCP.US/USD", "HD.US/USD", "HEI.US/USD", "HES.US/USD", "HII.US/USD", "HLT.US/USD", "HOG.US/USD", "HON.US/USD", "HPE.US/USD", "HPQ.US/USD", "HTA.US/USD", "HUBB.US/USD", "HUBS.US/USD", "HUM.US/USD", "HWM.US/USD", "HZNP.US/USD", "IBKR.US/USD", "IBM.US/USD", "ICE.US/USD", "IDXX.US/USD", "IEX.US/USD", "ILMN.US/USD", "INCY.US/USD", "INTC.US/USD", "INTU.US/USD", "INVH.US/USD", "IONS.US/USD", "IPG.US/USD", "IPGP.US/USD", "IQV.US/USD", "IR.US/USD", "ISRG.US/USD", "IT.US/USD", "ITUB.US/USD", "ITW.US/USD", "IVZ.US/USD", "JAZZ.US/USD", "JBLU.US/USD", "JCI.US/USD", "JEF.US/USD", "JKHY.US/USD", "JLL.US/USD", "JNJ.US/USD", "JPM.US/USD", "JWN.US/USD", "K.US/USD", "KEY.US/USD", "KEYS.US/USD", "KHC.US/USD", "KMB.US/USD", "KMI.US/USD", "KMX.US/USD", "KNX.US/USD", "KO.US/USD", "KR.US/USD", "KRC.US/USD", "KSS.US/USD", "L.US/USD", "LAMR.US/USD", "LDOS.US/USD", "LEA.US/USD", "LEN.US/USD", "LHX.US/USD", "LKQ.US/USD", "LLY.US/USD", "LMT.US/USD", "LNC.US/USD", "LNG.US/USD", "LNT.US/USD", "LOW.US/USD", "LPLA.US/USD", "LRCX.US/USD", "LSI.US/USD", "LSTR.US/USD", "LULU.US/USD", "LUV.US/USD", "LVS.US/USD", "LW.US/USD", "LYB.US/USD", "LYFT.US/USD", "LYV.US/USD", "M.US/USD", "MA.US/USD", "MAA.US/USD", "MANH.US/USD", "MAR.US/USD", "MASI.US/USD", "MAT.US/USD", "MCD.US/USD", "MCHP.US/USD", "MCK.US/USD", "MDB.US/USD", "MDLZ.US/USD", "MDT.US/USD", "MET.US/USD", "MGM.US/USD", "MHK.US/USD", "MIDD.US/USD", "MKL.US/USD", "MKSI.US/USD", "MKTX.US/USD", "MLM.US/USD", "MMM.US/USD", "MNDT.US/USD", "MO.US/USD", "MOH.US/USD", "MON.US/USD", "MPC.US/USD", "MPW.US/USD", "MPWR.US/USD", "MRK.US/USD", "MRNA.US/USD", "MRO.US/USD", "MRVL.US/USD", "MS.US/USD", "MSCI.US/USD", "MSFT.US/USD", "MTCH.US/USD", "MTD.US/USD", "MTN.US/USD", "MU.US/USD", "NBIX.US/USD", "NBL.US/USD", "NCLH.US/USD", "NDSN.US/USD", "NEE.US/USD", "NEM.US/USD", "NFLX.US/USD", "NIO.US/USD", "NKE.US/USD", "NLOK.US/USD", "NLSN.US/USD", "NLY.US/USD", "NOC.US/USD", "NOW.US/USD", "NRG.US/USD", "NSC.US/USD", "NTNX.US/USD", "NVDA.US/USD", "NVR.US/USD", "NWL.US/USD", "NWS.US/USD", "NXST.US/USD", "NYT.US/USD", "O.US/USD", "OC.US/USD", "ODFL.US/USD", "OGE.US/USD", "OGN.US/USD", "OHI.US/USD", "OKE.US/USD", "OKTA.US/USD", "OLED.US/USD", "OLLI.US/USD", "OLN.US/USD", "OMC.US/USD", "OMF.US/USD", "ON.US/USD", "ORCL.US/USD", "ORLY.US/USD", "OTIS.US/USD", "OXY.US/USD", "PANW.US/USD", "PARA.US/USD", "PAYC.US/USD", "PAYX.US/USD", "PBF.US/USD", "PBR.US/USD", "PCAR.US/USD", "PCG.US/USD", "PCLN.US/USD", "PCTY.US/USD", "PEAK.US/USD", "PENN.US/USD", "PEP.US/USD", "PFE.US/USD", "PG.US/USD", "PGR.US/USD", "PH.US/USD", "PII.US/USD", "PKG.US/USD", "PLAN.US/USD", "PLNT.US/USD", "PLTR.US/USD", "PLUG.US/USD", "PM.US/USD", "PNC.US/USD", "PNR.US/USD", "PODD.US/USD", "POOL.US/USD", "PPG.US/USD", "PRGO.US/USD", "PRU.US/USD", "PSA.US/USD", "PSTG.US/USD", "PSX.US/USD", "PTC.US/USD", "PTEN.US/USD", "PTON.US/USD", "PVH.US/USD", "PX.US/USD", "PXD.US/USD", "PYPL.US/USD", "QCOM.US/USD", "QRVO.US/USD", "RCL.US/USD", "RE.US/USD", "REG.US/USD", "REGN.US/USD", "RF.US/USD", "RGA.US/USD", "RGLD.US/USD", "RHT.US/USD", "RJF.US/USD", "RMD.US/USD", "RNG.US/USD", "RNR.US/USD", "ROKU.US/USD", "ROL.US/USD", "ROST.US/USD", "RPM.US/USD", "RRC.US/USD", "RRX.US/USD", "RS.US/USD", "RTN.US/USD", "RTX.US/USD", "SABR.US/USD", "SBNY.US/USD", "SBUX.US/USD", "SCCO.US/USD", "SCHW.US/USD", "SCI.US/USD", "SEDG.US/USD", "SEIC.US/USD", "SFM.US/USD", "SGEN.US/USD", "SHW.US/USD", "SIVB.US/USD", "SJM.US/USD", "SLB.US/USD", "SLM.US/USD", "SNAP.US/USD", "SNI.US/USD", "SNOW.US/USD", "SNPS.US/USD", "SO.US/USD", "SPG.US/USD", "SPGI.US/USD", "SPLK.US/USD", "SPOT.US/USD", "SPR.US/USD", "SQ.US/USD", "SRPT.US/USD", "SSNC.US/USD", "STE.US/USD", "STI.US/USD", "STT.US/USD", "STZ.US/USD", "SUI.US/USD", "SWK.US/USD", "SWKS.US/USD", "SYF.US/USD", "SYK.US/USD", "SYMC.US/USD", "SYY.US/USD", "T.US/USD", "TAP.US/USD", "TDG.US/USD", "TDY.US/USD", "TEAM.US/USD", "TECH.US/USD", "TEL.US/USD", "TEVA.US/USD", "TFC.US/USD", "TFX.US/USD", "TGT.US/USD", "TIF.US/USD", "TJX.US/USD", "TMO.US/USD", "TMUS.US/USD", "TOL.US/USD", "TPR.US/USD", "TPX.US/USD", "TRGP.US/USD", "TRMB.US/USD", "TROW.US/USD", "TRU.US/USD", "TRV.US/USD", "TSLA.US/USD", "TSM.US/USD", "TSN.US/USD", "TT.US/USD", "TTD.US/USD", "TTWO.US/USD", "TWLO.US/USD", "TWTR.US/USD", "TWX.US/USD", "TXN.US/USD", "TYL.US/USD", "UA.US/USD", "UAA.US/USD", "UBER.US/USD", "UDR.US/USD", "UGI.US/USD", "UHS.US/USD", "ULTA.US/USD", "UNH.US/USD", "UNP.US/USD", "UPS.US/USD", "URI.US/USD", "USB.US/USD", "USFD.US/USD", "UTHR.US/USD", "UTX.US/USD", "V.US/USD", "VALE.US/USD", "VEEV.US/USD", "VFC.US/USD", "VIAB.US/USD", "VICI.US/USD", "VIRT.US/USD", "VLO.US/USD", "VMC.US/USD", "VMW.US/USD", "VOYA.US/USD", "VRTX.US/USD", "VST.US/USD", "VTRS.US/USD", "VZ.US/USD", "W.US/USD", "WAB.US/USD", "WAL.US/USD", "WBA.US/USD", "WBS.US/USD", "WDAY.US/USD", "WDC.US/USD", "WEN.US/USD", "WEX.US/USD", "WFC.US/USD", "WH.US/USD", "WHR.US/USD", "WLK.US/USD", "WMT.US/USD", "WPC.US/USD", "WRB.US/USD", "WRK.US/USD", "WSM.US/USD", "WSO.US/USD", "WST.US/USD", "WTRG.US/USD", "WTW.US/USD", "WWD.US/USD", "WYNN.US/USD", "X.US/USD", "XIV.US/USD", "XLNX.US/USD", "XOM.US/USD", "XPEV.US/USD", "XPO.US/USD", "XYL.US/USD", "Y.US/USD", "YUM.US/USD", "YUMC.US/USD", "Z.US/USD", "ZBH.US/USD", "ZBRA.US/USD", "ZEN.US/USD", "ZM.US/USD", "ZS.US/USD", "ZTS.US/USD"]
  }
}

if __name__ == "__main__":

  transformID = lambda x:x.replace("/","_").replace(".","_").replace("&","_").replace(" ","_").replace("-","_")

  py_output=""
  go_output=""

  for group in groups.values():
    instruments=group.get("instruments")
    if instruments is None:
      continue
    id=transformID(group["id"])
    for instrument in instruments:
      variableName= transformID(instrument)
      "".upper()
      py_output+=f'''INSTRUMENT_{id.upper()}_{variableName.upper()} = "{instrument}"\n'''
      go_output+=f'''const INSTRUMENT_{id.upper()}_{variableName.upper()} = "{instrument}"\n'''

  with open("python/dukascript/instruments.py","w") as fd:
      fd.write(py_output)
  with open("go/instruments.go","w") as fd:
      fd.write("package dukascript\n\n")
      fd.write(go_output)
