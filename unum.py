#!/usr/bin/env python3
import unicodedata
import sys


def long_cat(category):
    cats = {"Cc": "Other, Control",
            "Cf": "Other, Format",
            "Cn": "Other, Not Assigned",
            "Co": "Other, Private Use",
            "Cs": "Other, Surrogate",
            "LC": "Letter, Cased",
            "Ll": "Letter, Lowercase",
            "Lm": "Letter, Modifier",
            "Lo": "Letter, Other",
            "Lt": "Letter, Titlecase",
            "Lu": "Letter, Uppercase",
            "Mc": "Mark, Spacing Combining",
            "Me": "Mark, Enclosing",
            "Mn": "Mark, Nonspacing",
            "Nd": "Number, Decimal Digit",
            "Nl": "Number, Letter",
            "No": "Number, Other",
            "Pc": "Punctuation, Connector",
            "Pd": "Punctuation, Dash",
            "Pe": "Punctuation, Close",
            "Pf": "Punctuation, Final quote",
            "Pi": "Punctuation, Initial quote",
            "Po": "Punctuation, Other",
            "Ps": "Punctuation, Open",
            "Sc": "Symbol, Currency",
            "Sk": "Symbol, Modifier",
            "Sm": "Symbol, Math",
            "So": "Symbol, Other",
            "Zl": "Separator, Line",
            "Zp": "Separator, Paragraph",
            "Zs": "Separator, Space"}
    if category in cats:
        return cats[category]
    else:
        return category

def print_info(char):
    spacing = " " if unicodedata.category(char) in ['Mn'] else ''
    try:
        unicodename = unicodedata.name(char)
    except ValueError as e:
        unicodename = "UNKNOWN"
    if ord(char) == 10:
        unicodename = "UNKNOWN"
        print(f"{ord(char):>8}    0x{ord(char):>06x}   {spacing}{' ':^5} {long_cat(unicodedata.category(char)):<26} {unicodename:<30}")
    else:
        print(f"{ord(char):>8}    0x{ord(char):>06x}   {spacing}{char:^5} {long_cat(unicodedata.category(char)):<26} {unicodename:<30}")


print(f"  Decimal      Hex     Char  {'Category':^26}   Name")
if len(sys.argv) == 1:
    for char in sys.stdin.read():
        print_info(char)
else:
    for argument in sys.argv[1:]:
        for char in argument:
            print_info(char)
    