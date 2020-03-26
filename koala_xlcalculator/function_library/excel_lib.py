
from datetime import datetime
from collections.abc import Iterable
import itertools

######################################################################################
# A dictionary that maps excel function names onto python equivalents. You should
# only add an entry to this map if the python name is different to the excel name
# (which it may need to be to  prevent conflicts with existing python functions
# with that name, e.g., max).

# So if excel defines a function foobar(), all you have to do is add a function
# called foobar to this module.  You only need to add it to the function map,
# if you want to use a different name in the python code.

# Note: some functions (if, pi, atan2, and, or, array, ...) are already taken care of
# in the FunctionNode code, so adding them here will have no effect.

SUPPORTED_FUNCTIONS = {
    "AVERAGE":"Average.average",
    "CHOOSE":"Choose.choose",
    "_XLFN.CONCAT":"Concat.concat",
    "COUNT":"Count.count",
    # "COUNTA":"Counta.counta",
    # "COUNTIF":"Countif.countif",
    # "COUNTIFS":"Countifs.countifs",
    # "DATE":"xDate.xdate",
    # "IFERROR":"Iferror.iferror",
    # "INDEX":"Index.index",
    # "IRR":"IRR.irr",
    # "ISBLANK":"Isblank.isblank",
    # "ISNA":"Isna.isna",
    # "ISTEXT":"Istext.istext",
    # "LINEST":"Linest.linest",
    # "LN":"Ln.ln",
    # "LOOKUP":"Lookup.lookup",
    # "MATCH":"Match.match",
    "MAX":"xMax.xmax",
    # "MID":"Mid.mid",
    "MIN":"xMin.xmin",
    # "MOD":"Mod.mod",
    # "NPV":"NPV.npv",
    # "OFFSET":"Offset.offset",
    # "PMT":"PMT.pmt",
    # "POWER":"Power.power",
    # "RIGHT":"Right.right",
    # "ROUND":"Round.round",
    # "ROUNDUP":"Round.roundup",
    # "SLN":"SLN.sln",
    # "SQRT":"Sqrt.sqrt",
    "SUM":"xSum.xsum",
    # "SUMIF":"SumIf.sumif",
    # "SUMPRODUCT":"Sumproduct.sumproduct",
    # "TODAY":"Today.today",
    # "VDB":"VDB.vdb",
    # "VLOOKUP":"Vlookup.vlookup",
    # "XNPV":"XNPV.xnpv",
    # "YEARFRAC":"Yearfrac.yearfrac",
    # # "GAMMALN":"lgamma",
}

IND_FUN = [
    "IF",
    "TAN",
    "ATAN2",
    "PI",
    "ARRAY",
    "ARRAYROW",
    "AND",
    "OR",
    "ALL",
    "VALUE",
    "LOG"
]


class KoalaBaseFunction():

    EXCEL_EPOCH = datetime.strptime("1900-01-01", '%Y-%m-%d').date()
    CELL_CHARACTER_LIMIT = 32767

    ErrorCodes = (
        "#NULL!",
        "#DIV/0!",
        "#VALUE!",
        "#REF!",
        "#NAME?",
        "#NUM!",
        "#N/A"
    )


    @staticmethod
    def value(text):
        """"""

        # make the distinction for naca numbers
        if text.find('.') > 0:
            return float(text)

        elif text.endswith('%'):
            text = text.replace('%', '')
            return float(text) / 100

        else:
            return int(text)


    @staticmethod
    def extract_numeric_values(*args):
        """"""

        values = []

        for arg in args:
            if isinstance(arg, XLRange):
                for x in arg.values:
                    values

        return values


    @staticmethod
    def is_number(s): # http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python
        """"""

        try:

            float(s)
            return True

        except:
            return False


    @staticmethod
    def flatten(l, only_lists=False):
        return list(itertools.chain(l))
    # def flatten(l, only_lists = False):
    #     instance = list if only_lists else collections.Iterable
    #
    #     for el in l:
    #         if isinstance(el, instance) and not isinstance(el, string_types):
    #             for sub in flatten(el, only_lists = only_lists):
    #                 yield sub
    #         else:
    #             yield el


    @staticmethod
    def find_corresponding_index(list, criteria):

        # parse criteria
        check = KoalaBaseFunction.criteria_parser(criteria)

        valid = []

        for index, item in enumerate(list):
            if check(item):
                valid.append(index)

        return valid


    @staticmethod
    def criteria_parser(criteria):

        if KoalaBaseFunction.is_number(criteria):
            def check(x):
                return x == criteria #and type(x) == type(criteria)

        elif type(criteria) == str:
            search = re.search('(\W*)(.*)', criteria.lower()).group
            operator = search(1)
            value = search(2)
            value = float(value) if KoalaBaseFunction.is_number(value) else str(value)

            if operator == '<':
                def check(x):
                    if not KoalaBaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x < value

            elif operator == '>':
                def check(x):
                    if not KoalaBaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x > value

            elif operator == '>=':
                def check(x):
                    if not KoalaBaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x >= value

            elif operator == '<=':
                def check(x):
                    if not KoalaBaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x <= value

            elif operator == '<>':
                def check(x):
                    if not KoalaBaseFunction.is_number(x):
                        raise TypeError('excellib.countif() doesnt\'t work for checking non number items against non equality')
                    return x != value

            else:
                def check(x):
                    return x == criteria

        else:
            raise Exception('Could\'t parse criteria %s' % criteria)

        return check

    @staticmethod
    def check_value(a):
        """"""

        if isinstance(a, ExcelError):
            return a

        elif isinstance(a, str) and a in ErrorCodes:
            return ExcelError(a)

        try:  # This is to avoid None or Exception returned by Range operations
            if float(a) or isinstance(a, (str)):
                return a

            else:
                return 0

        except:
            if a == 'True':
                return True

            elif a == 'False':
                return False

            else:
                return 0
