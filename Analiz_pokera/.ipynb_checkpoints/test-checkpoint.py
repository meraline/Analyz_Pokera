import re
import pandas as pd
from datetime import datetime
import numpy as np
import logging


#import eval7, pprint
from poker.room.pokerstars import PokerStarsHandHistory
#from phevaluator import evaluate_cards
from poker.hand import Hand, Combo
from poker.constants import Action, Position
import poker


import sentry_sdk
sentry_sdk.init(
    dsn="https://440378f295354f0fadbd14a96a9614d6@o4504649572941824.ingest.sentry.io/4504649575694336",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)


# logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
#                     format="%(asctime)s %(levelname)s %(message)s")
# logging.debug("A DEBUG Message")
# logging.info("An INFO")
# logging.warning("A WARNING")
# logging.error("An ERROR")
# logging.critical("A message of CRITICAL severity")


with open('Poker_/45.txt', 'r', encoding="utf8") as f:  # Poker_\SNG dimetruk 1-54133.txt
    data4 = f.read()

seats = []
pref_calls = []
pref_raisess = []
pref_allins = []
flop_calls = []
flop_checks = []

length_calls = 0
length_raisess = 0
length_allins = 0
length_f_calls = 0
length_f_checks = 0

for i in range(len(data4.split("\n\n\n"))):  # -1 для предупреждения ошибки, выход из цикда без последнего элемента
    try:
        # raise NotImplementedError("No error")
        distribut = data4.split("\n\n\n")[i]
        hhh = PokerStarsHandHistory(distribut)
        hhh.parse()
        pfa = str(hhh.preflop_actions)
        fa = str(hhh.flop.actions)

        seat = len(hhh.preflop_actions)
        seats.append(seat)

        pr_call = re.findall("calls", pfa)
        pr_rais = re.findall("raises", pfa)
        pr_allin = re.findall("all-in", pfa)

        f_check = re.findall("check", fa)
        f_call = re.findall("call", fa)
        f_rais = re.findall("raise", fa)
        f_allin = re.findall("bet", fa)
        # print(pr_allin)

        if pr_call == []:
            length_calls = 0
        else:
            for c in range(len(pr_call)):
                if c == 0:
                    length_calls = 1
                else:
                    length_calls += 1
        pref_calls.append(length_calls)

        if pr_rais == []:
            length_raisess = 0
        else:
            for r in range(len(pr_rais)):
                if r == 0:
                    length_raisess = 1
                else:
                    length_raisess += 1
        pref_raisess.append(length_raisess)

        if pr_allin == []:
            length_allins = 0
        else:
            for a in range(len(pr_allin)):
                # print(a)
                if a == 0:
                    length_allins = 1
                else:
                    length_allins += 1
        pref_allins.append(length_allins)

        if f_check == []:
            length_f_checks = 0
        else:
            for ch in range(len(f_check)):
                if ch == 0:
                    length_f_checks = 1
                else:
                    length_f_checks += 1
        flop_checks.append(length_f_checks)

        if f_call == []:
            length_f_calls = 0
        else:
            for k in range(len(f_call)):
                if k == 0:
                    length_f_calls = 1
                else:
                    length_f_calls += 1
        flop_calls.append(length_f_calls)

    except AttributeError:
        data4.split("\n\n\n")

    except TypeError as ru:
        print(ru)

    # except Exception as e:
    #     print(e)

