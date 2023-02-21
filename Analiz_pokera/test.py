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



# Создали словарь
data_pd = {'HandId': [], 'Level': [], 'ante': [], 'BB': [], 'flop_chip_bets': [], 'flop_chip_raises': [],
           'flop_chip_calls': [], 'turn_chip_bets': [], 'turn_chip_raises': [],
           'turn_chip_calls': [], 'river_chip_bets': [], 'river_chip_raises': [], 'river_chip_calls': [],
           'pflop_rais_sum': [], 'pflop_calls_sum': [], 'Players': [],
           'Board': [], 'SHOW_DOWN': [], 'pflop_rais': [], 'pflop_calls': [], 'pflop_allin': [], 'flop_bets': [],
           'flop_raises': [], 'flop_calls': [],
           'flop_allin': [], 'turn_bets': [], 'turn_raises': [], 'turn_calls': [], 'turn_allin': [], 'river_bets': [],
           'river_raises': [], 'river_calls': [], 'river_allin': []}

# Открываем файл
with open('dim100.txt', 'r', encoding="utf8") as f:  # Poker_/613k.txt   14437.txt
    data_r = f.read()

iterr = re.findall("\n\n\n", data_r).count('\n\n\n')  # задаём колличесвто итераций
print(iterr)

data = ""
iter_SHOW = 0

for i in range(iterr + 1):  # фильтруем раздачи с ШД и без
    if data_r.split("\n\n\n")[i].count('SHOW DOWN'):
        data = data + data_r.split("\n\n\n")[i] + "\n\n\n"
        iter_SHOW += 1
    else:
        continue
print(iter_SHOW)

# данные
result = re.findall(
    '(\w+) Hand #(\d*): Tournament #(\d*),(.*) Level (.*) \(.*\/(.*)\) - (\d{4}/\d+/\d+) (\d+\D\d+\D\d+) (\w*)', data)
Tables = re.findall('Table \'.*\' (.*)-max Seat', data)
# bains = re.findall('(\D\d+\.\d+\+\D\d+\.\d+)', data)
# HandHiros = re.findall("Dealt to .* \D(.. ..)\D", data)
Boards = re.findall("Board \[(.*)\]", data)
# preflop_raises_ = re.findall("raises", data) # "raises"g
SHOW_DOWNs = re.findall("Seat \d+: .+? showed \[(.*)\] and won", data)


# SHOW_DOWN.group(1)

def preflop_acti(self):
    preflop_ = re.search("HOLE CARDS \*{3}\\n(.*)\*{3} FLOP", self, re.DOTALL)
    x = 0
    i = 0
    max_rais = 0  # максимальный рейз
    y = 0
    sum_rais = 0  # сумма всех рейзов
    while i != preflop_.group(1).count('raises'):
        s = preflop_.group(1)
        if s.find('Dealt') == 0 and i == 0:
            y = 10
        if i != 0:
            y = x
        strart = s.find('to ', y)
        x = s.find('\n', strart)
        max_rais = s[strart + 3:x]
        if max_rais.find(' ') > 0:
            max_rais = s[strart + 3:x - 14]
        i += 1
        x = x + 1
        sum_rais += int(max_rais)

    z1 = 0
    i1 = 0
    x1 = 0
    sum_call = 0

    while i1 != preflop_.group(1).count('calls'):
        s = preflop_.group(1)
        strart = s.find('calls ', x1)
        x1 = s.find('\n', strart)
        z1 = s[strart + 6:x1]
        if z1.find(' ') > 0:
            z1 = s[strart + 6:x1 - 14]
        i1 += 1
        x1 = x1 + 1
        sum_call += int(z1)

    action_preflop_raises = preflop_.group(1).count('raises')
    action_preflop_calls = preflop_.group(1).count('calls')
    action_preflop_allin = preflop_.group(1).count('all-in')
    return action_preflop_raises, action_preflop_calls, action_preflop_allin, sum_rais, sum_call


def flop_acti(self):
    flop_ = re.search("FLOP \*{3} \[(.*)\]\\n(.*)\*{3} TU", self, re.DOTALL)
    # hand_flop = flop_.group(1)
    x = 0
    i = 0
    max_rais = 0  # максимальный рейз
    y = 0
    sum_rais = 0  # сумма всех рейзов
    while i != flop_.group(2).count('raises'):
        s = flop_.group(2)
        if s.find('Dealt') == 0 and i == 0:
            y = 10
        if i != 0:
            y = x
        strart = s.find('to ', y)
        x = s.find('\n', strart)
        max_rais = s[strart + 3:x]
        if max_rais.find(' ') > 0:
            max_rais = s[strart + 3:x - 14]
        i += 1
        x = x + 1
        sum_rais += int(max_rais)

    z1 = 0
    i1 = 0
    x1 = 0
    sum_call = 0

    while i1 != flop_.group(2).count('calls'):
        s = flop_.group(2)
        strart = s.find('calls ', x1)
        x1 = s.find('\n', strart)
        z1 = s[strart + 6:x1]
        if z1.find(' ') > 0:
            z1 = s[strart + 6:x1 - 14]
        i1 += 1
        x1 = x1 + 1
        sum_call += int(z1)

    bets = 0
    s = flop_.group(2)
    start = s.find('bets ')
    x1 = s.find('\n', start)
    bets = s[start + 5:x1]

    action_flop_bets = flop_.group(2).count('bets')
    action_flop_raises = flop_.group(2).count('raises')
    action_flop_allin = flop_.group(2).count('all-in')
    action_flop_calls = flop_.group(2).count('calls')
    return action_flop_bets, action_flop_raises, action_flop_calls, action_flop_allin, bets, sum_call, sum_rais


def turn_acti(self):
    turn_ = re.search("TURN \*{3} \[.*\] \[(.*)\](.*)\*{3} RI", self, re.DOTALL)
    # hand_turn = turn_.group(1)

    x = 0
    i = 0
    max_rais = 0  # максимальный рейз
    y = 0
    sum_rais = 0  # сумма всех рейзов
    while i != turn_.group(2).count('raises'):
        s = turn_.group(2)
        if s.find('Dealt') == 0 and i == 0:
            y = 10
        if i != 0:
            y = x
        strart = s.find('to ', y)
        x = s.find('\n', strart)
        max_rais = s[strart + 3:x]
        if max_rais.find(' ') > 0:
            max_rais = s[strart + 3:x - 14]
        i += 1
        x = x + 1
        sum_rais += int(max_rais)

    z1 = 0
    i1 = 0
    x1 = 0
    sum_call = 0
    while i1 != turn_.group(2).count('calls'):
        s = turn_.group(2)
        strart = s.find('calls ', x1)
        x1 = s.find('\n', strart)
        z1 = s[strart + 6:x1]
        if z1.find(' ') > 0:
            z1 = s[strart + 6:x1 - 14]
        i1 += 1
        x1 = x1 + 1
        sum_call += int(z1)

    bets = 0
    s = turn_.group(2)
    strart = s.find('bets ')
    x1 = s.find('\n', strart)
    bets = s[strart + 5:x1]

    action_turn_bets = turn_.group(2).count('bets')
    action_turn_raises = turn_.group(2).count('raises')
    action_turn_allin = turn_.group(2).count('all-in')
    action_turn_calls = turn_.group(2).count('calls')
    return action_turn_bets, action_turn_raises, action_turn_calls, action_turn_allin, bets, sum_call, sum_rais


def river_acti(self):
    river_ = re.search("RIVER \*{3} \[.*\] \[(.*)\](.*)\\n\*{3} SHOW", self, re.DOTALL)
    # hand_river = river_.group(1)

    x = 0
    i = 0
    max_rais = 0  # максимальный рейз
    y = 0
    sum_rais = 0  # сумма всех рейзов
    while i != river_.group(2).count('raises'):
        s = river_.group(2)
        if s.find('Dealt') == 0 and i == 0:
            y = 10
        if i != 0:
            y = x
        strart = s.find('to ', y)
        x = s.find('\n', strart)
        max_rais = s[strart + 3:x]
        if max_rais.find(' ') > 0:
            max_rais = s[strart + 3:x - 14]
        i += 1
        x = x + 1
        sum_rais += int(max_rais)

    z1 = 0
    i1 = 0
    x1 = 0
    sum_call = 0
    while i1 != river_.group(2).count('calls'):
        s = river_.group(2)
        strart = s.find('calls ', x1)
        x1 = s.find('\n', strart)
        z1 = s[strart + 6:x1]
        if z1.find(' ') > 0:
            z1 = s[strart + 6:x1 - 14]
        i1 += 1
        x1 = x1 + 1
        sum_call += int(z1)

    bets = 0
    s = river_.group(2)
    strart = s.find('bets ')
    x1 = s.find('\n', strart)
    bets = s[strart + 5:x1]

    action_river_bets = river_.group(2).count('bets')
    action_river_raises = river_.group(2).count('raises')
    action_river_allin = river_.group(2).count('all-in')
    action_river_calls = river_.group(2).count('calls')
    return action_river_bets, action_river_raises, action_river_calls, action_river_allin, bets, sum_call, sum_rais


preflop_raisess = []
preflop_callss = []
preflop_allins = []
preflop_raisess_sums = []
preflop_calls_sums = []
antes = []

flop_betss = []
flop_raisess = []
flop_callss = []
flop_allins = []
flop_chip_betss = []
flop_chip_callss = []
flop_chip_raisess = []

turn_betss = []
turn_raisess = []
turn_callss = []
turn_allins = []
turn_chip_betss = []
turn_chip_raisess = []
turn_chip_callss = []

river_betss = []
river_raisess = []
river_callss = []
river_allins = []
river_chip_betss = []
river_chip_raisess = []
river_chip_callss = []

for y in range(iter_SHOW):
    data_n = data.split("\n\n\n")[y]  # разбивает сплошной текст на раздачи

    # ПРЕФЛОП
    strart = data_n.find('ante')
    x1 = data_n.find('\n', strart)
    ante = data_n[strart + 5:x1]
    antes.append(ante)

    if data_n.count('raises'):
        preflop_raisess.append(preflop_acti(data_n)[0])
    else:
        preflop_raisess.append(0)

    if data_n.count('calls'):
        preflop_callss.append(preflop_acti(data_n)[1])
    else:
        preflop_callss.append(0)
    if data_n.count('all-in'):
        preflop_allins.append(preflop_acti(data_n)[2])
    else:
        preflop_allins.append(0)

    if preflop_acti(data_n)[3] != 0:
        preflop_raisess_sums.append(preflop_acti(data_n)[3])
    else:
        preflop_raisess_sums.append(0)

    if preflop_acti(data_n)[4] != 0:
        preflop_calls_sums.append(preflop_acti(data_n)[4])
    else:
        preflop_calls_sums.append(0)

    #     if preflop_acti(data_n)[5] != 0:
    #         flop_chip_betss.append(preflop_acti(data_n)[5])
    #     else:
    #         flop_chip_betss.append(0)

    #     if preflop_acti(data_n)[6] != 0:
    #         flop_chip_callss.append(preflop_acti(data_n)[6])
    #     else:
    #         flop_chip_callss.append(0)

    #     if preflop_acti(data_n)[7] != 0:
    #         flop_chip_raisess.append(preflop_acti(data_n)[7])
    #     else:
    #         flop_chip_raisess.append(0)

    # ФЛОП
    if data_n.count('bets'):
        flop_betss.append(flop_acti(data_n)[0])
    else:
        flop_betss.append(0)
    if data_n.count('raises'):
        flop_raisess.append(flop_acti(data_n)[1])
    else:
        flop_raisess.append(0)
    if data_n.count('calls'):
        flop_callss.append(flop_acti(data_n)[2])
    else:
        flop_callss.append(0)
    if data_n.count('all-in'):
        flop_allins.append(flop_acti(data_n)[3])
    else:
        flop_allins.append(0)
    # ТЁРН
    if data_n.count('bets'):
        turn_betss.append(turn_acti(data_n)[0])
    else:
        turn_betss.append(0)
    if data_n.count('raises'):
        turn_raisess.append(turn_acti(data_n)[1])
    else:
        turn_raisess.append(0)
    if data_n.count('calls'):
        turn_callss.append(turn_acti(data_n)[2])
    else:
        turn_callss.append(0)
    if data_n.count('all-in'):
        turn_allins.append(turn_acti(data_n)[3])
    else:
        turn_allins.append(0)

    if turn_acti(data_n)[4] != 0:
        turn_chip_betss.append(turn_acti(data_n)[4])
    else:
        turn_chip_betss.append(0)

    if turn_acti(data_n)[5] != 0:
        turn_chip_callss.append(turn_acti(data_n)[5])
    else:
        turn_chip_callss.append(0)

    if turn_acti(data_n)[6] != 0:
        turn_chip_raisess.append(turn_acti(data_n)[6])
    else:
        turn_chip_raisess.append(0)

    # РИВЕР
    if data_n.count('bets'):
        river_betss.append(river_acti(data_n)[0])
    else:
        river_betss.append(0)
    if data_n.count('raises'):
        river_raisess.append(river_acti(data_n)[1])
    else:
        river_raisess.append(0)
    if data_n.count('calls'):
        river_callss.append(river_acti(data_n)[2])
    else:
        river_callss.append(0)
    if data_n.count('all-in'):
        river_allins.append(river_acti(data_n)[3])
    else:
        river_allins.append(0)

    if river_acti(data_n)[4] != 0:
        river_chip_betss.append(river_acti(data_n)[4])
    else:
        river_chip_betss.append(0)

    if river_acti(data_n)[5] != 0:
        river_chip_callss.append(river_acti(data_n)[5])
    else:
        river_chip_callss.append(0)

    if river_acti(data_n)[6] != 0:
        river_chip_raisess.append(river_acti(data_n)[6])
    else:
        river_chip_raisess.append(0)

# Считаем сколко фишек
s = re.findall('Seat (\d).*chips', data)
s = [int(x) for x in s]
seats = []
length = 1
for i in range(len(s) - 1):
    if s[i + 1] < s[i]:
        seats.append(length)
        length = 1
    else:
        length += 1
seats.append(length)

# ЗАполнЯем словарь данными
for r, table, seat, Board, preflop_raises, preflop_calls, preflop_allin, flop_bets, flop_raises, flop_calls, flop_allin, \
    turn_bets, turn_raises, turn_calls, turn_allin, river_bets, river_raises, river_calls, river_allin, SHOW_DOWN, preflop_raisess_sum, \
    preflop_calls_sum, ante, flop_chip_bets, flop_chip_calls, flop_chip_raises, turn_chip_bets, turn_chip_raises, turn_chip_calls, river_chip_bets, \
    river_chip_raises, river_chip_calls \
        in zip(result, Tables, seats, Boards, preflop_raisess, preflop_callss, preflop_allins, flop_betss, flop_raisess,
               flop_callss,
               flop_allins, turn_betss, turn_raisess, turn_callss, turn_allins, river_betss, river_raisess,
               river_callss, river_allins, SHOW_DOWNs,
               preflop_raisess_sums, preflop_calls_sums, antes, flop_chip_betss, flop_chip_callss, flop_chip_raisess,
               turn_chip_betss, turn_chip_raisess,
               turn_chip_callss, river_chip_betss, river_chip_raisess, river_chip_callss):
    # data_pd['TypeOfRoom'].append(r[0])
    data_pd['HandId'].append(r[1])
    # data_pd['Tournament'].append(r[2])
    # data_pd['info'].append(r[3])
    data_pd['Level'].append(r[4])
    data_pd['BB'].append(r[5])
    # data_pd['Date'].append(r[6])
    # data_pd['Hour'].append(r[7])
    # data_pd['TimeZone'].append(r[8])
    data_pd['ante'].append(ante)
    # data_pd['Table'].append(table) #table
    data_pd['Players'].append(seat)
    # data_pd['bain'].append(bain)
    # data_pd['HandHiro'].append(handHiro)
    data_pd['Board'].append(Board)
    data_pd['pflop_rais'].append(preflop_raises)
    # data_pd['pflop_rais_max'].append(preflop_raisess_to)
    data_pd['pflop_rais_sum'].append(preflop_raisess_sum)
    data_pd['pflop_calls_sum'].append(preflop_calls_sum)
    # data_pd['showed_won'].append(showed_won)
    data_pd['pflop_calls'].append(preflop_calls)
    data_pd['pflop_allin'].append(preflop_allin)
    data_pd['flop_bets'].append(flop_bets)
    data_pd['flop_raises'].append(flop_raises)
    data_pd['flop_calls'].append(flop_calls)
    data_pd['flop_allin'].append(flop_allin)
    data_pd['turn_bets'].append(turn_bets)
    data_pd['turn_raises'].append(turn_raises)
    data_pd['turn_calls'].append(turn_calls)
    data_pd['turn_allin'].append(turn_allin)
    data_pd['river_bets'].append(river_bets)
    data_pd['river_raises'].append(river_raises)
    data_pd['river_calls'].append(river_calls)
    data_pd['river_allin'].append(river_allin)
    data_pd['flop_chip_bets'].append(flop_chip_bets)
    data_pd['flop_chip_raises'].append(flop_chip_raises)
    data_pd['flop_chip_calls'].append(flop_chip_calls)
    data_pd['turn_chip_bets'].append(turn_chip_bets)
    data_pd['turn_chip_raises'].append(turn_chip_raises)
    data_pd['turn_chip_calls'].append(turn_chip_calls)
    data_pd['river_chip_bets'].append(river_chip_bets)
    data_pd['river_chip_raises'].append(river_chip_raises)
    data_pd['river_chip_calls'].append(river_chip_calls)
    data_pd['SHOW_DOWN'].append(SHOW_DOWN)

# Создаём ДатаФрейм
df = pd.DataFrame(data_pd)
df.head()
print(df)