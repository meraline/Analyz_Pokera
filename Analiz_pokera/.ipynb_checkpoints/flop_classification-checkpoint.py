from range import Range
import numpy as np

deck = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
deck2 = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
suit = ['c', 'd', 'h', 's']

A = ['A']
HIGH = ['T', 'J', 'Q', 'K']
MED = ['6', '7', '8', '9']
LOW = ['2', '3', '4', '5']
group = [[A, 'A'], [HIGH, "H"], [MED, "M"], [LOW, "L"]]

paired = ["TRIPS", "PAIRED", "UNPAIRED"]  # Paired types
flush = ["RAINBOW", "TWO-TONE", "MONOTONE"]  # Flushes Type
STR = ["OESD", "GUTSHOT", "STRAIGHT", "NONE"]  # Straights Type


class Flop:
    # create list of flop, card in flop, and suit in flop
    flop = []
    flop_card = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    flop_suit = [0, 0, 0, 0]
    group = None
    paired = None
    flush = None
    strit = None

    # init flop with input flop
    def __init__(self, text):
        self.set_flop(text)
        self.card_and_suit_count()
        self.set_group()
        self.set_fullhouse()
        self.set_flush()
        self.set_strit()

    # set flop
    def set_flop(cls, text):
        if ' ' in text:
            temp = text.split(' ')
        else:
            temp = [text[0:2], text[2:4], text[4:6]]
        cls.flop = temp.copy()

    # count card and suit
    def card_and_suit_count(cls):
        for card in cls.flop:
            temp_card = card[0]
            temp_suit = card[1]
            cls.flop_card[deck.index(temp_card)] += 1
            cls.flop_suit[suit.index(temp_suit)] += 1


    # set cls.group ex. AHM AMM MML
    def set_group(cls):
        cards = cls.flop
        group_cards = ""
        for card in cards:
            for group_type in group:
                if card[0] in group_type[0]:
                    group_cards += group_type[1]
                    continue
        cls.group = group_cards

    # set cls.paired ex. PAIRED UNPAIRED TRIPS
    def set_fullhouse(cls):
        if 3 in cls.flop_card: # TRIPS
            cls.paired = paired[0]
        elif 2 in cls.flop_card: #PAIRED
            cls.paired = paired[1]
        else: #UNPAIRED
            cls.paired = paired[2]

    # set cls.flush ex. MONOTONE TWO-TONE RAINBOW
    def set_flush(cls):
        if 3 in cls.flop_suit: # MONOTONE
            cls.flush = flush[2]
        elif 2 in cls.flop_suit: # TWO-TONE
            cls.flush = flush[1]
        else: # RAINBOW
            cls.flush = flush[0]
            
     # выводит двухсторонку, гатшот и стрит       
    def set_strit(cls):
        index = []
        for n in cls.flop:
            for i in deck2:
                i = str(deck2.index(n[:1])).zfill(2)
            index.append(i)
        index.sort()
        index_int = [int(x) for x in index]
        if (index_int[0] == 0 and index_int[1] == 1  and index_int[2] == 12) or \
            (index_int[0] == 10 and index_int[1] == 11  and index_int[2] == 12):
            cls.strit = STR[2]
        elif (index_int[2] - index_int[1]) == 1 and \
             (index_int[1] - index_int[0]) == 1:
            cls.strit = STR[0]
        elif ((index_int[2] - index_int[1]) == 2 and \
             (index_int[1] - index_int[0]) == 1) or \
             ((index_int[2] - index_int[1]) == 1 and \
             (index_int[1] - index_int[0]) == 2) or \
             (index_int[0] == 0 and index_int[1] == 2  and index_int[2] == 12) or \
             (index_int[0] == 1 and index_int[1] == 2  and index_int[2] == 12):
            cls.strit = STR[1]
        else:
            cls.strit = STR[3]       

    # return flop card only (no suit)
    def get_flop_card(cls):
        return cls.flop[0][0] + cls.flop[1][0] + cls.flop[2][0]

    # print Flop ex. AcTc5d
    def __str__(self):
        return self.flop[0] + self.flop[1] + self.flop[2]


if __name__ == '__main__':
    t = Flop('3c 2c 4c')
    print(t)
    print(t.group)
    print(t.paired)
    print(t.flush) 
    print(t.strit)