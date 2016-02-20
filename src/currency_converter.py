#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import json


def win32_unicode_argv():
    """Uses shell32.GetCommandLineArgvW to get sys.argv as a list of Unicode
    strings.

    Versions 2.x of Python don't support Unicode in sys.argv on
    Windows, with the underlying Windows API instead replacing multi-byte
    characters with '?'.
    """

    from ctypes import POINTER, byref, cdll, c_int, windll
    from ctypes.wintypes import LPCWSTR, LPWSTR

    GetCommandLineW = cdll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = LPCWSTR

    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [LPCWSTR, POINTER(c_int)]
    CommandLineToArgvW.restype = POINTER(LPWSTR)

    cmd = GetCommandLineW()
    argc = c_int(0)
    argv = CommandLineToArgvW(cmd, byref(argc))
    if argc.value > 0:
        # Remove Python executable and commands if present
        start = argc.value - len(sys.argv)
        return [argv[i] for i in
                xrange(start, argc.value)]


def load_json_data(currency_from, currency_or_currencies_to):

    import urllib2

    string_of_currencies = ""
    if len(currency_or_currencies_to) < 4:
        string_of_currencies = '"'+currency_from+currency_or_currencies_to+'"'
    else:
        for currency in currency_or_currencies_to:
            string_of_currencies += '"'+currency_from+currency+'"'
            string_of_currencies += ","
        string_of_currencies = string_of_currencies[:-1]

    yql_base_url = "https://query.yahooapis.com/v1/public/yql"
    yql_query = 'select%20*%20from%20yahoo.finance.xchange%20where%20pair%20in%20('+string_of_currencies+')'
    yql_query_url = yql_base_url + "?q=" + yql_query + "&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"

    try:
        yql_response = urllib2.urlopen(yql_query_url)
        try:
            yql_json = json.loads(yql_response.read())
            return yql_json
        except (ValueError, KeyError, TypeError):
            return "JSON format error"

    except IOError, e:
        if hasattr(e, 'code'):
            return e.code
        elif hasattr(e, 'reason'):
            return e.reason


def convert_currency(currency_amount, current_rate, json_data):
    if current_rate is None:
        return currency_amount * float(json_data['query']['results']['rate']['Rate'])
    else:
        return currency_amount * float(json_data['query']['results']['rate'][current_rate]['Rate'])


def make_frame(amount, input_currency):
    return {
             "input": {
                "amount": amount,
                "currency": input_currency
             },
                "output": {}
            }


def add_currency(dictionary, new_currency, amount):
    dictionary["output"].update({new_currency: round(amount, 2)})


def print_output(output):
    print json.dumps(output, indent=4, sort_keys=True)


if len(sys.argv) > 4:
    sys.argv = win32_unicode_argv()
    input_amount = float(sys.argv[2])
    currency_from = sys.argv[4]

    # Currencies with known symbols, some of them are modified due to the same symbols
    currencies = {'EUR': '€', 'KRW': 'KR₩', 'VND': '₫', 'BOB': '$b', 'VEF': 'Bs', 'ISK': 'ikr', 'BYR': 'p.',
                  'JMD': 'J$', 'DKK': 'dkr', 'SRD': 'SR$', 'AUD': 'A$', 'ZAR': 'ZS', 'CUP': '₱', 'NGN': '₦',
                  'CRC': '₡', 'MZN': 'MT', 'SYP': 'SY£', 'ANG': 'ƒ', 'BRL': 'R$', 'BSD': 'BS$', 'MKD': 'ден',
                  'SHP': 'SH£', 'BGN': 'Bлв', 'SGD': 'SG$', 'CNY': 'C¥', 'ARS': 'AR$', 'TTD': 'TT$', 'SCR': 'S₨',
                  'SBD': 'SB$', 'GTQ': 'Q', 'PKR': 'P₨', 'PEN': 'S/.', 'LVL': 'Ls', 'UAH': '₴', 'LRD': 'LR$',
                  'RON': 'rkr', 'COP': 'CO$', 'NPR': 'N₨', 'SOS': 'SS', 'FKP': 'F£', 'LKR': 'L₨', 'JPY': '¥',
                  'KYD': 'KY$', 'TWD': 'NT$', 'IRR': '﷼', 'AFN': '؋', 'SVC': 'SV$', 'PLN': 'zł', 'PYG': 'Gs',
                  'ILS': '₪', 'KPW': 'KP₩', 'GIP': 'G£', 'BND': 'BN$', 'HNL': 'L', 'CZK': 'Kč', 'HUF': 'Ft',
                  'IDR': 'Rp', 'LTL': 'Lt', 'RUB': 'руб', 'RSD': 'Дин.', 'NAD': 'NA$', 'PAB': 'B/.', 'DOP': 'RD$',
                  'ALL': 'Lek', 'HRK': 'kn', 'KHR': '៛', 'PHP': '₱', 'XCD': 'X$', 'KZT': 'Kлв', 'FJD': 'F$',
                  'BAM': 'KM', 'EGP': 'E£', 'QAR': '﷼', 'OMR': '﷼', 'KGS': 'Kлв', 'MXN': 'M$', 'MYR': 'RM',
                  'YER': '﷼', 'SAR': '﷼', 'UYU': '$U', 'GBP': '£', 'UZS': 'Uлв', 'AWG': 'ƒ', 'MNT': '₮',
                  'THB': '฿', 'LAK': '₭', 'BBD': 'BB$', 'SEK': 'skr', 'USD': '$', 'ERN': 'nfk', 'BZD': 'BZ$',
                  'NZD': 'N$', 'GYD': 'GY$', 'HKD': 'HK$'}

    for currency, symbol in currencies.iteritems():
        if currency_from == unicode(symbol, "utf-8"):
            currency_from = currency

    result = make_frame(input_amount, currency_from)

    if len(sys.argv) > 6:
        currency_to = sys.argv[6]
        for currency, symbol in currencies.iteritems():
            if currency_to == unicode(symbol, "utf-8"):
                currency_to = currency
        convert_rate_from_json = load_json_data(currency_from, currency_to)
        output_amount = convert_currency(input_amount, None, convert_rate_from_json)
        add_currency(result, currency_to, output_amount)
    else:
        # All known currencies from http://finance.yahoo.com/
        currencies_to_convert = ["EUR", "KRW", "VND", "BOB", "MOP", "BDT", "MDL", "VEF", "GEL", "ISK",
                                 "BYR", "THB", "MXV", "TND", "JMD", "DKK", "SRD", "BWP", "NOK", "MUR",
                                 "AZN", "INR", "MGA", "CAD", "XAF", "LBP", "SRD", "XDR", "IDR", "IEP",
                                 "AUD", "MMK", "LYD", "ZAR", "IQD", "XPF", "TJS", "CUP", "UGX", "NGN",
                                 "PGK", "TOP", "TMT", "KES", "CRC", "MZN", "SYP", "ANG", "ZMW", "BRL",
                                 "BSD", "NIO", "GNF", "BMD", "SLL", "MKD", "BIF", "LAK", "BHD", "SHP",
                                 "BGN", "SGD", "CNY", "ARS", "TTD", "SCR", "BBD", "SBD", "MAD", "GTQ",
                                 "MWK", "PKR", "ITL", "PEN", "AED", "LVL", "UAH", "FRF", "LRD", "LSL",
                                 "SEK", "RON", "XOF", "COP", "CDF", "TZS", "SRD", "GHS", "NPR", "ZWL",
                                 "SOS", "DZD", "FKP", "LKR", "JPY", "CHF", "KYD", "CLP", "IRR", "AFN",
                                 "DJF", "SVC", "PLN", "PYG", "ERN", "ETB", "ILS", "TWD", "KPW", "SIT",
                                 "GIP", "BND", "HNL", "CZK", "HUF", "BZD", "DEM", "JOD", "IDR", "RWF",
                                 "LTL", "RUB", "RSD", "WST", "NAD", "PAB", "DOP", "ALL", "HTG", "HKD",
                                 "AMD", "KMF", "MRO", "HRK", "ECS", "KHR", "PHP", "CYP", "KWD", "XCD",
                                 "CNH", "SDG", "CLF", "KZT", "TRY", "FJD", "NZD", "BAM", "BTN", "STD",
                                 "VUV", "MVR", "AOA", "EGP", "QAR", "OMR", "CVE", "KGS", "MXN", "MYR",
                                 "GYD", "SZL", "YER", "SAR", "UYU", "GBP", "UZS", "GMD", "AWG", "RWF",
                                 "MNT", "USD"]

        convert_rates_from_json = load_json_data(currency_from, currencies_to_convert)
        current_currency_in_list = 0
        for currency in currencies_to_convert:
            if cmp(currency, currency_from) == 0:
                continue
            output_amount = convert_currency(input_amount, current_currency_in_list, convert_rates_from_json)
            add_currency(result, currency, output_amount)
            current_currency_in_list += 1

    print_output(result)
else:
    print "Missing command line arguments"



