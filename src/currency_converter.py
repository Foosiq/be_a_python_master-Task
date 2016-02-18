#!/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import urllib2


def load_json_data(currency_from, currency_or_currencies_to):
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
    output_dict = {
                    "input": {
                        "amount": amount,
                        "currency": input_currency
                    },
                    "output": {}
                   }
    return output_dict


def add_currency(dictionary, new_currency, amount):
    dictionary["output"].update({new_currency: round(amount, 2)})


def print_output(output):
    print json.dumps(output, indent=4, sort_keys=True)


if len(sys.argv) > 4:
    input_amount = float(sys.argv[2])
    currency_from = sys.argv[4]
    """
    currencies = {'EUR': '€', 'KRW': '₩', 'VND': '₫', 'BOB': '$b', 'VEF': 'Bs', 'ISK': 'kr', 'BYR': 'p.', 'THB': '฿',
                  'JMD': 'J$', 'DKK': 'kr', 'SRD': '$', 'IDR': 'Rp', 'AUD': '$', 'ZAR': 'S', 'CUP': '₱', 'NGN': '₦',
                  'CRC': '₡', 'MZN': 'MT', 'SYP': '£', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€',
                  'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€',
                  'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€',
                  'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€',
                  'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€',
                  'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€', 'EUR': '€',
                  'EUR': '€',}
    """
    result = make_frame(input_amount, currency_from)

    if len(sys.argv) > 6:
        currency_to = sys.argv[6]
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
                                 "BGN", "SGD", "CNY", "EUR", "TTD", "SCR", "BBD", "SBD", "MAD", "GTQ",
                                 "MWK", "PKR", "ITL", "PEN", "AED", "LVL", "UAH", "FRF", "LRD", "LSL",
                                 "SEK", "RON", "XOF", "COP", "CDF", "TZS", "SRD", "GHS", "NPR", "ZWL",
                                 "SOS", "DZD", "FKP", "LKR", "JPY", "CHF", "KYD", "CLP", "IRR", "AFN",
                                 "DJF", "SVC", "PLN", "PYG", "ERN", "ETB", "ILS", "TWD", "KPW", "SIT",
                                 "GIP", "BND", "HNL", "CZK", "HUF", "BZD", "DEM", "JOD", "IDR", "RWF",
                                 "LTL", "RUB", "RSD", "WST", "NAD", "BZD", "PAB", "DOP", "ALL", "HTG",
                                 "AMD", "KMF", "MRO", "HRK", "ECS", "KHR", "PHP", "CYP", "KWD", "XCD",
                                 "CNH", "SDG", "CLF", "KZT", "TRY", "FJD", "NZD", "BAM", "BTN", "STD",
                                 "VUV", "MVR", "AOA", "EGP", "QAR", "OMR", "CVE", "KGS", "MXN", "MYR",
                                 "GYD", "SZL", "YER", "SAR", "UYU", "GBP", "UZS", "GMD", "AWG", "RWF",
                                 "MNT", "HKD", "YER", "ARS"]

        convert_rates_from_json = load_json_data(currency_from, currencies_to_convert)
        current_currency_in_list = 0
        for currency in currencies_to_convert:
            output_amount = convert_currency(input_amount, current_currency_in_list, convert_rates_from_json)
            add_currency(result, currency, output_amount)
            current_currency_in_list += 1

    print_output(result)
else:
    print "Missing program arguments"


