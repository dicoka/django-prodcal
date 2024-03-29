"""Production calendar for Russian Federation"""

from .prod_dict import ProdDict

# нерабочие дни (среди будних)
NON_WORK_DAY_DICT = ProdDict({
    2016: { 1: [1, 4, 5, 6, 7, 8],
            2: [22, 23],
            3: [7, 8],
            4: [],
            5: [1, 2, 3, 9],
            6: [13],
            7: [],
            8: [],
            9: [],
           10: [],
           11: [4],
           12: []},
    2017: { 1: [2, 3, 4, 5, 6],
            2: [23, 24],
            3: [8],
            4: [],
            5: [1, 8, 9],
            6: [5, 12, 19],
            7: [],
            8: [],
            9: [],
           10: [],
           11: [6],
           12: []},
    2018: { 1: [1, 2, 3, 4, 5, 8],
            2: [23],
            3: [8, 9],
            4: [9,30],
            5: [1, 2, 9],
            6: [11, 12],
            7: [],
            8: [],
            9: [],
           10: [],
           11: [5],
           12: [31]},

})

# рабочие дни (среди выходных)
WORK_DAY_DICT = ProdDict({
    2016: { 1: [],
            2: [20],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
           10: [],
           11: [],
           12: []},
    2018: { 1: [],
            2: [22],
            3: [7],
            4: [28],
            5: [],
            6: [9],
            7: [],
            8: [],
            9: [],
           10: [],
           11: [],
           12: [29]},

})
