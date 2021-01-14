from money.currency import Currency

switcher = {
    'ALL': Currency.ALL, 'AMD': Currency.AMD, 'ANG': Currency.ANG, 'AOA': Currency.AOA, 'ARS': Currency.ARS,
    'AUD': Currency.AUD, 'AWG': Currency.AWG, 'AZN': Currency.AZN, 'BAM': Currency.BAM, 'BBD': Currency.BBD,
    'BDT': Currency.BDT, 'BGN': Currency.BGN, 'BHD': Currency.BHD, 'BIF': Currency.BIF, 'BMD': Currency.BMD,
    'BND': Currency.BND, 'BOB': Currency.BOB, 'BOV': Currency.BOV, 'BRL': Currency.BRL, 'BSD': Currency.BSD,
    'BTN': Currency.BTN, 'BWP': Currency.BWP, 'BYN': Currency.BYN, 'BYR': Currency.BYR, 'BZD': Currency.BZD,
    'CDF': Currency.CDF, 'CHE': Currency.CHE, 'CHF': Currency.CHF, 'CHW': Currency.CHW, 'CLF': Currency.CLF,
    'CLP': Currency.CLP, 'CNY': Currency.CNY, 'COP': Currency.COP, 'COU': Currency.COU, 'CAD': Currency.CAD,
    'CRC': Currency.CRC, 'CUC': Currency.CUC, 'CUP': Currency.CUP, 'CVE': Currency.CVE, 'CZK': Currency.CZK,
    'DJF': Currency.DJF, 'DKK': Currency.DKK, 'DOP': Currency.DOP, 'DZD': Currency.DZD, 'EGP': Currency.EGP,
    'ERN': Currency.ERN, 'ETB': Currency.ETB, 'EUR': Currency.EUR, 'FJD': Currency.FJD, 'FKP': Currency.FKP,
    'GBP': Currency.GBP, 'GEL': Currency.GEL, 'GHS': Currency.GHS, 'GIP': Currency.GIP, 'GMD': Currency.GMD,
    'GNF': Currency.GNF, 'GTQ': Currency.GTQ, 'GYD': Currency.GYD, 'HKD': Currency.HKD, 'HNL': Currency.HNL,
    'HRK': Currency.HRK, 'HTG': Currency.HTG, 'HUF': Currency.HUF, 'IDR': Currency.IDR, 'ILS': Currency.ILS,
    'INR': Currency.INR, 'IQD': Currency.IQD, 'IRR': Currency.IRR, 'ISK': Currency.ISK, 'JMD': Currency.JMD,
    'JOD': Currency.JOD, 'JPY': Currency.JPY, 'KES': Currency.KES, 'KGS': Currency.KGS, 'KHR': Currency.KHR,
    'KMF': Currency.KMF, 'KPW': Currency.KPW, 'KRW': Currency.KRW, 'KWD': Currency.KWD, 'KYD': Currency.KYD,
    'KZT': Currency.KZT, 'LAK': Currency.LAK, 'LBP': Currency.LBP, 'LKR': Currency.LKR, 'LRD': Currency.LRD,
    'LTL': Currency.LTL, 'LVL': Currency.LVL, 'LYD': Currency.LYD, 'MAD': Currency.MAD, 'MDL': Currency.MDL,
    'MGA': Currency.MGA, 'MKD': Currency.MKD, 'MMK': Currency.MMK, 'MNT': Currency.MNT, 'LSL': Currency.LSL,
    'MOP': Currency.MOP, 'MRO': Currency.MRO, 'MUR': Currency.MUR, 'MVR': Currency.MVR, 'MWK': Currency.MWK,
    'MXN': Currency.MXN, 'MXV': Currency.MXV, 'MYR': Currency.MYR, 'MZN': Currency.MZN, 'NAD': Currency.NAD,
    'NGN': Currency.NGN, 'NIO': Currency.NIO, 'NOK': Currency.NOK, 'NPR': Currency.NPR, 'NZD': Currency.NZD,
    'OMR': Currency.OMR, 'PAB': Currency.PAB, 'PEN': Currency.PEN, 'PGK': Currency.PGK, 'PHP': Currency.PHP,
    'PKR': Currency.PKR, 'PLN': Currency.PLN, 'PYG': Currency.PYG, 'QAR': Currency.QAR, 'RON': Currency.RON,
    'RSD': Currency.RSD, 'RUB': Currency.RUB, 'RWF': Currency.RWF, 'SAR': Currency.SAR, 'SBD': Currency.SBD,
    'SCR': Currency.SCR, 'SDG': Currency.SDG, 'SEK': Currency.SEK, 'SGD': Currency.SGD, 'SHP': Currency.SHP,
    'SLL': Currency.SLL, 'SOS': Currency.SOS, 'SRD': Currency.SRD, 'SSP': Currency.SSP, 'STD': Currency.STD,
    'SVC': Currency.SVC, 'SYP': Currency.SYP, 'SZL': Currency.SZL, 'THB': Currency.THB, 'TJS': Currency.TJS,
    'TMT': Currency.TMT, 'TND': Currency.TND, 'TOP': Currency.TOP, 'TRY': Currency.TRY, 'TTD': Currency.TTD,
    'TWD': Currency.TWD, 'TZS': Currency.TZS, 'UAH': Currency.UAH, 'UGX': Currency.UGX, 'USD': Currency.USD,
    'USN': Currency.USN, 'USS': Currency.USS, 'UYI': Currency.UYI, 'UYU': Currency.UYU, 'UZS': Currency.UZS,
    'VEF': Currency.VEF, 'VND': Currency.VND, 'VUV': Currency.VUV, 'WST': Currency.WST, 'XAF': Currency.XAF,
    'XAG': Currency.XAG, 'XAU': Currency.XAU, 'XBA': Currency.XBA, 'XBB': Currency.XBB, 'XBC': Currency.XBC,
    'XBD': Currency.XBD, 'XCD': Currency.XCD, 'XDR': Currency.XDR, 'XFU': Currency.XFU, 'XOF': Currency.XOF,
    'XPD': Currency.XPD, 'XPF': Currency.XPF, 'XPT': Currency.XPT, 'XSU': Currency.XSU, 'XTS': Currency.XTS,
    'XUA': Currency.XUA, 'YER': Currency.YER, 'ZAR': Currency.ZAR, 'ZMW': Currency.ZMW, 'ZWL': Currency.ZWL,
    'AED': Currency.AED, 'AFN': Currency.AFN
}