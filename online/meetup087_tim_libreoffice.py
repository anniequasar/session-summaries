# -*- coding: utf-8 -*-
r"""MeetUp 087 - Beginners' Python and Machine Learning - 24 Nov 2020 - Python macros in LibreOffice

Youtube: https://youtu.be/841Fgt1sQsY
Source:  https://github.com/anniequasar/session-summaries/raw/master/online/meetup087_tim_libreoffice.py
Sample:  https://github.com/anniequasar/session-summaries/raw/master/online/meetup087_tim_libreoffice.ods

Learning objectives
 - how to write and run Python macros in LibreOffice 7 using pyuno

@author D Tim Cummings

References

https://help.libreoffice.org/latest/sq/text/sbasic/python/python_programming.html
Explains XSCRIPTCONTEXT

https://www.pitonyak.org/oo.php
675 page manual on openoffice macros (BASIC)

https://wiki.documentfoundation.org/Macros/Python_Guide/Calc
How to manipulate sheets, cells and ranges using Python

http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html
Nice tutorial. Shows named ranges

http://document-foundation-mail-archive.969070.n3.nabble.com/PyUNO-usability-improvements-td4151556.html
Explains cell references sheet["A1"], sheet[r, c]

https://wiki.openoffice.org/wiki/Documentation/BASIC_Guide/Cells_and_Ranges
How to manipulate sheets, cells and ranges using BASIC

Extensions (bad links in LibreOffice website)

https://github.com/hanya/MRI/releases . MRI helps you find commands properties and methods.
https://gitlab.com/jmzambon/apso . Alternative Python Script Organizer


Task 1: Install LibreOffice https://www.libreoffice.org/download/
LibreOffice 7.0.3 comes with Python 3.7.7 so you shouldn't need anything else installed.
(SDK is optional and not used in this session)

# Mac: Put scripts in
~/Library/Application Support/LibreOffice/4/user/Scripts/python/
# Windows: Put scripts in
%APPDATA%\LibreOffice\4\user\Scripts\python
echo %APPDATA%
# Linux: Put scripts in
~/.config/libreoffice/4/user/Scripts/python

# Start LibreOffice from command line so you see logging messages. Not necessary if you don't need to see logging
# Windows PowerShell
& 'C:\Program Files\LibreOffice\program\soffice.com'
# Mac Terminal
/Applications/LibreOffice.app/Contents/MacOS/soffice

Task 2: Create a script meetup087_tim_libreoffice.py and put in python scripts directory.
Script to define a function 'py_brokerage' which takes parameters 'quantity' and
'unit_price' and optional parameter 'quantity_split' and returns 20
You can download solution and example files from https://github.com/anniequasar/session-summaries/online/
meetup087_tim_libreoffice.py
meetup087_tim_libreoffice.ods

Task 3: Create a LibreOffice calc document in your Documents directory with a worksheet called 'Trades' and
column headings in row 1, col C of
Trade Date, Buy Sell, Stock Code, Quantity, Unit Price, Brokerage, Revenue
Create Basic macro: Tools > Macros > Organise Macros > Basic...
In workbook > Standard, click [New] and call it PythonBridge
In LibreOffice Tools > Options  (Mac: Preferences)
    LibreOffice > Security > Macro Security > Select Medium

Function bas_brokerage(quantity, unit_price, Optional quantity_split)
    Dim myScript as Object
    myScript = ThisComponent.getScriptProvider().getScript("vnd.sun.star.script:meetup087_tim_libreoffice.py$py_brokerage?language=Python&location=user")
    bas_brokerage = myScript.invoke(Array(quantity, unit_price, quantity_split), Array(), Array() )
End Function

In a cell in worksheet, enter "=bas_brokerage(100, 15)" without the quotes and you should get 20

Task 4: import logging and sys and in py_brokerage log the python version to the console. Use F9 to recalc cell with brokerage

Task 5: Change py_brokerage to match commsec brokerage rates and test in worksheet
    $10.00 (Up to and including $1,000)
    $19.95 (Over $1,000 up to $10,000 (inclusive))
    $29.95 (Over $10,000 up to $25,000 (inclusive))
    0.12% (Over $25,000)

Task 6: Create py_revenue which returns a positive value for sale of shares (Buy Sell = S) and negative for purchase (Buy Sell = B)
You will need to create a BASIC function revenue to call it.

Solution 6:
Function bas_revenue(buy_sell, quantity, unit_price, Optional quantity_split)
    Dim myScript as Object
    myScript = ThisComponent.getScriptProvider().getScript("vnd.sun.star.script:meetup087_tim_libreoffice.py$py_revenue?language=Python&location=user")
    bas_revenue = myScript.invoke(Array(buy_sell, quantity, unit_price, quantity_split), Array(), Array() )
End Function

Task 7: Install extension MRI from https://github.com/hanya/MRI/releases . MRI helps you find commands properties and methods.
Install extension APSO from https://gitlab.com/jmzambon/apso . Alternative Python Script Organizer

Task 8: Define a python function cells_and_ranges with one optional argument which sets contents of one cell with "Cells and Ranges"
Run the script in a worksheet from Tools > Macros > Run Macro... > My Macros > meetup087_tim_libreoffice.py > cells_and_ranges
    XSCRIPTCONTEXT.getDocument().CurrentController.ActiveSheet["A6"].setString("Cells and Ranges")

CurrentController works with user interface elements such as active worksheet or selection.

Task 9: Create a push button making it easier to run macro.
Form design mode > Right click button > Control properties > Events > Execute Action >
    ... > My Macros > meetup087_tim_libreoffice.py > cells_and_ranges

Task 10: With some data in Trades table (especially Buy Sell, Quantity, Unit Price) write and run a python macro calc_revenue_simple
which puts in formula for calculating brokerage and revenue on every row.

Task 11: Repeat Task 10 with named ranges.
(Solution uses two functions update_named_range and calc_revenue)

Task 12: Create a macro which analyses your trades matches sells to buys and calculates the capital gains
(Solution uses two functions link_buy_sell and calc_gains)

Task 13: Usg msgbox from https://wiki.documentfoundation.org/Macros/Python_Guide/Useful_functions to display a message

"""
import logging
import sys
from collections import defaultdict


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# $10.00 (Up to and including $1,000)
# $19.95 (Over $1,000 up to $10,000 (inclusive))
# $29.95 (Over $10,000 up to $25,000 (inclusive))
# 0.12% (Over $25,000)
def py_brokerage(quantity, unit_price, quantity_split=None):
    """Calculate Commsec brokerage. If purchase is split over sales then apportion brokerage"""
    logger.debug(f"brokerage: sys.version = {sys.version}")
    if quantity_split is None:
        quantity_split = quantity
    amount = quantity * unit_price
    if amount <= 1000:
        return 10 * quantity_split / quantity
    elif amount <= 10000:
        return 19.95 * quantity_split / quantity
    elif amount <= 25000:
        return 29.95 * quantity_split / quantity
    else:
        return amount * 0.0012 * quantity_split / quantity


def py_revenue(buy_sell, quantity, unit_price, quantity_split=None):
    if quantity_split is None:
        quantity_split = quantity
    if buy_sell.lower().startswith("s"):
        return quantity_split * unit_price - py_brokerage(quantity=quantity, unit_price=unit_price, quantity_split=quantity_split)
    else:
        return - quantity_split * unit_price - py_brokerage(quantity=quantity, unit_price=unit_price, quantity_split=quantity_split)


def cells_and_ranges(event=None):
    doc = XSCRIPTCONTEXT.getDocument()
    sheet = doc.CurrentController.ActiveSheet
    logger.info("cells_and_ranges")

    sheet[5, 0].setString("Cells and Ranges")  # assign to String property or call setString method
    sheet.getCellRangeByName("A7").String = 'sheet.getCellRangeByName("A7")'
    # getCellByPosition(column, row)  # zero-indexed
    sheet.getCellRangeByName("A7:C16").getCellByPosition(0, 1).String = 'sheet.getCellRangeByName("A7:C16").getCellByPosition(0, 1)'
    sheet.getCellByPosition(0, 8).String = 'sheet.getCellByPosition(0, 8)'
    # [row, column]  # zero-indexed
    sheet.getCellRangeByName("A7:C16")[3, 0].String = 'sheet.getCellRangeByName("A7:C16")[3, 0]'
    sheet.getCellRangeByPosition(0, 6, 2, 15)[4, 0].String = 'sheet.getCellRangeByPosition(0, 6, 2, 15)[4, 0]'
    sheet[11, 0].String = 'sheet[11, 0]'
    sheet["A13"].String = 'sheet["A13"]'
    sheet[6:16, 0:3][7, 0].String = 'sheet[6:16, 0:3][7, 0]'
    try:
        sheet[6:16, 0:3]["A4"].String = 'sheet[6:16, 0:3]["A4"]'
    except Exception as e:
        logger.error(f'sheet[6:16, 0:3]["A4"] {str(e)}')
    sheet[6:16, 0:3]["A15"].String = 'sheet[6:16, 0:3]["A15"]'
    sheet[15, 0].String = sheet[15, 0].AbsoluteName
    ca = sheet["A17"].CellAddress
    sheet["A17"].String = f'CellAddress=(Sheet={ca.Sheet} Row={ca.Row} Column={ca.Column})'
    sheet["A18"].String = f'sheet[6:16, 0:3].AbsoluteName={sheet[6:16, 0:3].AbsoluteName}'
    cr = sheet['A7:C16'].RangeAddress
    sheet["A19"].String = f"sheet['A7:C16'].RangeAddress=(Sheet={cr.Sheet} StartRow={cr.StartRow} EndRow={cr.EndRow} StartColumn={cr.StartColumn} EndColumn={cr.EndColumn})"
    cursor = sheet.createCursorByRange(sheet['A10'])
    cursor.gotoEnd()
    cr = cursor.RangeAddress
    sheet["A20"].String = f"gotoEnd RangeAddress=(Sheet={cr.Sheet} StartRow={cr.StartRow} EndRow={cr.EndRow} StartColumn={cr.StartColumn} EndColumn={cr.EndColumn})"
    cursor = sheet.createCursorByRange(sheet['A10'])
    cursor.collapseToCurrentRegion()
    cr = cursor.RangeAddress
    sheet["A21"].String = f"collapseToCurrentRegion RangeAddress=(Sheet={cr.Sheet} StartRow={cr.StartRow} EndRow={cr.EndRow} StartColumn={cr.StartColumn} EndColumn={cr.EndColumn})"
    doc.CurrentController.select(sheet.getCellRangeByPosition(cr.StartColumn, cr.StartRow, cr.EndColumn, cr.EndRow))


def calc_revenue_simple(event=None):  # need optional argument so function can be run from button or menu
    logger.info("calc_revenue_simple")
    doc = XSCRIPTCONTEXT.getDocument()
    sheet = doc.Sheets["Trades"]
    cursor = sheet.createCursorByRange(sheet["C1"])
    cursor.gotoEnd()

    row_boundary = cursor.RangeAddress.EndRow + 1
    for row in range(1, row_boundary):
        sheet[row, 7].Formula = f"=BAS_BROKERAGE(F{row};G{row})"
        sheet[row, 8].Formula = f"=BAS_REVENUE(D{row};F{row};G{row})"
    # Setting formula
    # Use semicolons rather than commas or get Err:508


def update_named_range(sheet, name, column, row_boundary, number_format=None):
    sheet[f"{column}1"].String = name.replace("_", " ")
    if row_boundary > 1:
        if sheet.NamedRanges.hasByName(name):
            sheet.NamedRanges.removeByName(name)
        # addNewByName(name:str, content:str, position:CellAddress, type:int)
        # name = name of named range
        # content = a cell range address is one possible content of a named range - absolute works, can be a formula.
        # position = base address for relative cell positions
        # type = normally 0 except for named ranges used as filter criteria or print range or repeating rows or columns
        sheet.NamedRanges.addNewByName(name, sheet[f"{column}2:{column}{row_boundary}"].AbsoluteName, sheet[0, 0].CellAddress, 0)
        if number_format is not None:
            sheet[name].NumberFormat = number_format


CURRENCY = 104  # LibreOffice code for currency format
DATE = 75  # LibreOffice code for date format


def calc_revenue(event=None):  # need optional argument so function can be run from button or menu
    logger.info("calc_revenue")
    doc = XSCRIPTCONTEXT.getDocument()
    sheet = doc.Sheets["Trades"]
    cursor = sheet.createCursorByRange(sheet["C1"])
    cursor.gotoEnd()

    row_boundary = cursor.RangeAddress.EndRow + 1
    update_named_range(sheet, "Trade_Date", "C", row_boundary, DATE)  # 75 : D MMM YYYY
    update_named_range(sheet, "Buy_Sell", "D", row_boundary)
    update_named_range(sheet, "Stock_Code", "E", row_boundary)
    update_named_range(sheet, "Quantity", "F", row_boundary)
    update_named_range(sheet, "Unit_Price", "G", row_boundary, CURRENCY)  # 104 : [$$-C09]#,##0.00;[RED]-[$$-C09]#,##0.00

    for row in range(1, row_boundary):
        sheet[row, 7].Formula = '=BAS_BROKERAGE(1*Quantity;1*Unit_Price)'
        sheet[row, 8].Formula = '=BAS_REVENUE(""&Buy_Sell;1*Quantity;1*Unit_Price)'
    update_named_range(sheet, "Brokerage", "H", row_boundary, CURRENCY)  # 104 : Currency format
    update_named_range(sheet, "Revenue", "I", row_boundary, CURRENCY)  # 104 : Currency format
    # Setting formula
    # Use semicolons rather than commas or get Err:508
    # Can't use named ranges with user defined functions in BASIC except if use 1* (or 0+ or ""&) trick to convert ranges to scalars


def link_buy_sell(buy, sell):
    quantity_split = min(buy['quantity_balance'], sell['quantity_balance'])
    if quantity_split == 0:
        # Don't create a link with zero value
        return None
    buy['quantity_balance'] -= quantity_split
    sell['quantity_balance'] -= quantity_split
    gain = {'date_buy': buy['date'], 'quantity_buy': buy['quantity'], 'unit_price_buy': buy['unit_price'],
            'date_sell': sell['date'], 'quantity_sell': sell['quantity'], 'unit_price_sell': sell['unit_price'],
            'stock_code': buy['stock_code'], 'quantity_split': quantity_split}
    return gain


def calc_gains(event=None):
    logger.info("calc_revenue")
    doc = XSCRIPTCONTEXT.getDocument()
    # Get trades
    calc_revenue()
    sheet = doc.Sheets["Trades"]
    rng_trade_date = sheet["Trade_Date"]
    rng_buy_sell = sheet["Buy_Sell"]
    rng_stock_code = sheet["Stock_Code"]
    rng_quantity = sheet["Quantity"]
    rng_unit_price = sheet["Unit_Price"]
    buy_by_code = defaultdict(list)
    sell_by_code = defaultdict(list)
    for row in range(rng_trade_date.Rows.Count):
        the_date = rng_trade_date[row, 0].Value
        the_buy_sell = rng_buy_sell[row, 0].String
        the_stock_code = rng_stock_code[row, 0].String
        the_quantity = rng_quantity[row, 0].Value
        the_unit_price = rng_unit_price[row, 0].Value
        d = {'date': the_date, 'stock_code': the_stock_code, 'quantity': the_quantity, 'quantity_balance': the_quantity, 'unit_price': the_unit_price}
        if the_buy_sell.lower().startswith("b"):
            buy_by_code[the_stock_code].append(d)
        else:
            sell_by_code[the_stock_code].append(d)
        # Assume data sorted chronologically
    lst_gains = []
    lst_portfolio = []
    for the_stock_code, lst_buys in buy_by_code.items():
        lst_sells = sell_by_code[the_stock_code]
        i_buy = 0
        i_sell = 0
        while i_sell < len(lst_sells):
            buy = lst_buys[i_buy]
            sell = lst_sells[i_sell]
            gain = link_buy_sell(buy, sell)
            if gain is not None:
                lst_gains.append(gain)
            if buy["quantity_balance"] == 0:
                i_buy += 1
            if sell["quantity_balance"] == 0:
                i_sell += 1
        while i_buy < len(lst_buys):
            buy = lst_buys[i_buy]
            lst_portfolio.append(buy)
            i_buy += 1
    # How to create a new sheet
    # https://wiki.documentfoundation.org/Macros/Python_Guide/Calc/Calc_sheets
    if "Gains" not in doc.Sheets:
        doc.Sheets.insertNewByName("Gains", 2)
    sheet = doc.Sheets["Gains"]
    sheet["A1"].String = "Stock Code"
    sheet["B1"].String = "Quantity Split"
    sheet["C1"].String = "Date Buy"
    sheet["D1"].String = "Quantity Buy"
    sheet["E1"].String = "Unit Price Buy"
    sheet["F1"].String = "Brokerage Buy"
    sheet["G1"].String = "Revenue Buy"
    sheet["H1"].String = "Date Sell"
    sheet["I1"].String = "Quantity Sell"
    sheet["J1"].String = "Unit Price Sell"
    sheet["K1"].String = "Brokerage Sell"
    sheet["L1"].String = "Revenue Sell"
    sheet["M1"].String = "Gain"
    row = 2
    for gain in lst_gains:
        sheet[f"A{row}"].String = gain['stock_code']
        sheet[f"B{row}"].Value = gain['quantity_split']
        sheet[f"C{row}"].Value = gain['date_buy']
        sheet[f"D{row}"].Value = gain['quantity_buy']
        sheet[f"E{row}"].Value = gain['unit_price_buy']
        sheet[f"F{row}"].Formula = f"=BAS_BROKERAGE(D{row};E{row};B{row})"
        sheet[f"G{row}"].Formula = f'=BAS_REVENUE("B";D{row};E{row};B{row})'
        sheet[f"H{row}"].Value = gain['date_sell']
        sheet[f"I{row}"].Value = gain['quantity_sell']
        sheet[f"J{row}"].Value = gain['unit_price_sell']
        sheet[f"K{row}"].Formula = f"=BAS_BROKERAGE(I{row};J{row};B{row})"
        sheet[f"L{row}"].Formula = f'=BAS_REVENUE("S";I{row};J{row};B{row})'
        sheet[f"M{row}"].Formula = f"=G{row}+L{row}"
        row += 1
    for share in lst_portfolio:
        sheet[f"A{row}"].String = share['stock_code']
        sheet[f"B{row}"].Value = share['quantity_balance']
        sheet[f"C{row}"].Value = share['date']
        sheet[f"D{row}"].Value = share['quantity']
        sheet[f"E{row}"].Value = share['unit_price']
        sheet[f"F{row}"].Formula = f"=BAS_BROKERAGE(D{row};E{row};B{row})"
        sheet[f"G{row}"].Formula = f'=BAS_REVENUE("B";D{row};E{row};B{row})'
        row += 1
    sheet[1:row, 2].NumberFormat = DATE
    sheet[1:row, 7].NumberFormat = DATE
    sheet[1:row, 4:7].NumberFormat = CURRENCY
    sheet[1:row, 9:13].NumberFormat = CURRENCY


# https://wiki.documentfoundation.org/Macros/Python_Guide/Useful_functions
from com.sun.star.awt import MessageBoxButtons as MSG_BUTTONS
import uno

CTX = uno.getComponentContext()
SM = CTX.getServiceManager()


def create_instance(name, with_context=False):
    if with_context:
        instance = SM.createInstanceWithContext(name, CTX)
    else:
        instance = SM.createInstance(name)
    return instance


def msgbox(message, title='LibreOffice', buttons=MSG_BUTTONS.BUTTONS_OK, type_msg='infobox'):
    """ Create message box
        type_msg: infobox, warningbox, errorbox, querybox, messbox
        https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XMessageBoxFactory.html
        https://wiki.documentfoundation.org/Macros/Python_Guide/Useful_functions
    """
    toolkit = create_instance('com.sun.star.awt.Toolkit')
    parent = toolkit.getDesktopWindow()
    mb = toolkit.createMessageBox(parent, type_msg, buttons, title, str(message))
    return mb.execute()
