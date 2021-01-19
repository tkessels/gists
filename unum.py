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


print("{:^11} {:^10} {:^5} {:^26}   {:<30}".format("Decimal", "Hex", "Char", "Category", "Name"))
for argument in sys.argv[1:]:
    for char in argument:
        #if character has now own width add a space ..... u know .... for spacing 
        spacing = " " if unicodedata.category(char) in ['Mn'] else ''
        print("{:>8}    0x{:>06x}   {spacing}{:^5} {:<26} {:<30}".format(ord(char), ord(char), char, long_cat(unicodedata.category(char)), unicodedata.name(char),spacing=spacing))

