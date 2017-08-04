
import enum
import random
import logging
logging.basicConfig(level=logging.INFO, format="%(message)s")


class dice(enum.IntEnum):
    def __str__(self):
        return str(self.name) # don't need to print the number
    def __repr__(self):
        return str(self.name)
    Sword_1 = 1
    Sword_2 = 2
    Sword_3 = 3
    Sword_4 = 4
    Sword_5 = 5
    Sword_6 = 6
    Sword_7 = 7
    Sword_8 = 8
    Sword_9 = 9
    Sword_10 = 10
    Sword_11 = 11
    Sword_12 = 12
    Sword_13 = 13
    # numeric values are for matching Swords
    Political = 0
    Castle = 0
    Wizard = 0
    @classmethod
    def rollable(cls):
        "Returns a tuple of the six possible rolls"
        return (cls.Sword_1, cls.Sword_2, cls.Sword_3, cls.Political, cls.Castle, cls.Wizard)

def roll():
    return random.choice(dice.rollable())

class card():
    def __init__(self, name, *requirements):
        self.name = name
        self.reqs = requirements

def buy(card, number_of_rolls=7):
    rolls = [roll() for _ in range(number_of_rolls)]
    requirements = list(card.reqs) # create a copy
    requirements.sort(reverse=True)  # sort the requirements to ensure largest sword is first.
    penalty = 0
    all_matches = []
    while requirements and rolls: # Each iteration of this loop is one round.
        matches = []  # need to track the matches in a round for penalty determination
        logging.debug("Reqs: {}".format(requirements))
        logging.debug("Rolls: {}".format(rolls))
        if all_matches:
            logging.debug("Current Matches: {}".format(all_matches))
        for easy in (dice.Political, dice.Castle, dice.Wizard):
            while easy in requirements and easy in rolls:
                # remove all instances.
                logging.debug("Matched: {}".format(easy))
                requirements.remove(easy)
                rolls.remove(easy)
                matches.append(easy)
        #for big_sword in [dice.Sword_13]:
        for big_sword in [dice.Sword_13, dice.Sword_12, dice.Sword_11, dice.Sword_10, dice.Sword_9, dice.Sword_8, dice.Sword_7, dice.Sword_6, dice.Sword_5, dice.Sword_4]:
        # for big_sword in [dice.Sword_12, dice.Sword_11, dice.Sword_10, dice.Sword_9, dice.Sword_8, dice.Sword_7, dice.Sword_6, dice.Sword_5]:
            while big_sword in requirements:
                if sum(rolls) >= big_sword:  # we can match a big_sword.
                    rolls.sort(reverse=True)
                    
                    requirements.remove(big_sword)
                    # the first approach removes the largest swords first -- this may be suboptimal if there are other requirements.
                    # 30 % versus 40% for 3xSword_4 new versus old. Now up to 36.5% and that's probably where I'll leave it.
                    # so Sword_3, Sword_3, Sword_1, Sword_1 should match 2xSword_4, but with the first approach it doesn't.
                    # also don't want to match 1,1,1,1 with Sword_4 if there is another Sword remaining. 
                    # -- although we'd need 5 dice to allow for the mismatch penalty
                    swords = 0
                    new_matches = []
                    if False:
                        for d in rolls:
                            if swords < big_sword:
                                if d > 0:  # shouldn't get here are the rolls are now sorted.
                                    new_matches.append(d)
                                    # can't remove from rolls here as we're iterating through rolls.
                                    swords += d
                        #logging.debug("Matched {} with : {}".format(big_sword, new_matches))
                        for d in new_matches:
                            rolls.remove(d)
                            matches.append(d)
                    else:
                        # This approach tries to minimise the Swords used, but will match 1,1,1,1 regardless of remaining requirements
                        matched = False
                        while sum(rolls) > 0 and not matched: # still swords available.
                            logging.debug("A match is available for {} with {} in {}".format(big_sword, swords, rolls))
                            swords += rolls[0]
                            new_matches.append(rolls[0])                
                            rolls.remove(rolls[0])
                            if swords + rolls[0] >= big_sword:  
                            # we can match with one dice, so iterate from the smallest to optimise use
                                for d in reversed(rolls):  # creates an iterator, NOT a copy            
                                    if swords + d >= big_sword:
                                        new_matches.append(d)
                                        matched = True
                                        break  # break out of the for loop
                            else:
                                # we need at least two more dice, so loop again
                                pass
                        logging.debug("Matched {} with : {}".format(big_sword, new_matches))
                        # only need to remove the last of the new_matches from rolls as they're removed to iterate
                        rolls.remove(new_matches[-1])
                        matches.extend(new_matches)
                        
                        
                else:  # check if we have enough dice to match on a re-roll.
                    if 3 * (len(rolls) - 1) < requirements.count(big_sword) * big_sword: # handle multiple big swords
                        logging.debug("Next round can't match {} with {} dice".format(big_sword, len(rolls) - 1))
                        # just set rolls to an empty list to trigger failure case
                        rolls = []
                    break
        # swords requiMancer OR re-roll for easys
        while dice.Sword_4 in requirements:
            # worst case, but if we have a Sword_4 and a Sword_2 and rolled Sword_3 and Sword_1 would we match the 4 or the 2? Maybe depends on how many other die there are and what round we're in.
            # just match this first then handle the rest of the Swords.
            if dice.Sword_3 in rolls and dice.Sword_1 in rolls:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_3, dice.Sword_1))
                logging.debug("4 matched by 3, 1")
                rolls.remove(dice.Sword_3)
                rolls.remove(dice.Sword_1)
            elif rolls.count(dice.Sword_2) >= 2:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_2, dice.Sword_2))
                logging.debug("4 matched by 2, 2")
                rolls.remove(dice.Sword_2)
                rolls.remove(dice.Sword_2)
            elif rolls.count(dice.Sword_3) >= 2:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_3, dice.Sword_3))
                logging.debug("4 matched by 3, 3")
                rolls.remove(dice.Sword_3)
                rolls.remove(dice.Sword_3)
            elif dice.Sword_3 in rolls and dice.Sword_2 in rolls:
                requirements.remove(dice.Sword_4)
                matches.extend((dice.Sword_3, dice.Sword_2))
                logging.debug("4 matched by 3, 2")
                rolls.remove(dice.Sword_3)
                rolls.remove(dice.Sword_2)
            else: # no possible matches for Sword_4
                break
        for d in (dice.Sword_3, dice.Sword_2, dice.Sword_1):
            while d in requirements:
                if d in rolls:
                    logging.debug("{} Matched exactly".format(d))
                    rolls.remove(d)
                    requirements.remove(d)
                    matches.append(d)
                else:
                    break
        # check to match Sword 2 with Sword 3
        if dice.Sword_2 in requirements and dice.Sword_3 in rolls:
            requirements.remove(dice.Sword_2)
            matches.append(dice.Sword_3)
            logging.debug("2 matched by 3")
            rolls.remove(dice.Sword_3)
        if dice.Sword_1 in requirements and dice.Sword_3 in rolls:
            requirements.remove(dice.Sword_1)
            matches.append(dice.Sword_3)
            logging.debug("1 matched by 3")
            rolls.remove(dice.Sword_3)
        if dice.Sword_1 in requirements and dice.Sword_2 in rolls:
            requirements.remove(dice.Sword_1)
            matches.append(dice.Sword_2)
            logging.debug("1 matched by 2")
            rolls.remove(dice.Sword_2)
        if requirements:
            logging.debug("No more matches with: {}, still need {}".format(rolls, requirements))
            if matches:
                all_matches.extend(matches)
                penalty = 0
            else:
                penalty = 1
            rerolls = len(rolls) - penalty
            logging.debug("Rerolling {}".format(rerolls))
            rolls = [roll() for _ in range(rerolls)]
        else:
            logging.debug("Unneeded: {}".format(rolls))
        penalty += 1
    if requirements:
        logging.debug("Failed to acquire {} remaining:".format(card.name, requirements))
        return False
    else:
        logging.debug("Successfully acquiMancer {}".format(card.name))
        return True


def test_buy(target, number_of_tests=10000, print_last=False):
    count = 0
    logger = logging.getLogger()
    log_level = logger.level
    for i in range(number_of_tests):
        # only print the last round
        if i == number_of_tests - 1 and print_last:
            logger.setLevel(logging.DEBUG)  # note this will permanently
        if buy(target):
            count += 1
    logger.info("Chance to buy card {} is about {:.2%} after {:,} iterations".format(target.name, count/number_of_tests, number_of_tests))
    logger.setLevel(log_level)

Priest = card("P1", dice.Sword_3, dice.Sword_1, dice.Political, dice.Political, dice.Castle, dice.Castle)
Priest2 = card("P2", dice.Sword_13)
Priest3 = card("P3", dice.Sword_8, dice.Sword_2, dice.Political, dice.Wizard)
Priest4 = card("P4", dice.Sword_6, dice.Political, dice.Political, dice.Castle)
# Warrior3
Warrior = card("B1", dice.Sword_12)
Warrior2 = card("B2", dice.Political, dice.Political, dice.Political, dice.Castle, dice.Wizard)
Warrior3 = card("B3", dice.Castle, dice.Castle, dice.Political, dice.Political)
#Wizard3
Wizard = card("G1", dice.Sword_4, dice.Sword_4, dice.Political)
Wizard2 = card("G2", dice.Sword_10)
Wizard3 = card("G3", dice.Sword_4, dice.Castle, dice.Castle, dice.Political, dice.Political, dice.Wizard)
#Kingmakersmith3
Kingmakersmith = card("Y1", dice.Castle, dice.Castle, dice.Castle)
Kingmakersmith2 = card("Y2", dice.Political, dice.Political, dice.Political)
Kingmakersmith3 = card("Y3", dice.Sword_3, dice.Castle, dice.Castle, dice.Castle)
#Builder2
Builder = card("O1", dice.Political, dice.Political, dice.Political, dice.Wizard)
Builder2 = card("O2", dice.Sword_10)
#Mancer2
Mancer = card("R1", dice.Sword_2, dice.Political, dice.Political, dice.Castle)
Mancer2 = card("R2", dice.Sword_4, dice.Sword_3, dice.Political, dice.Political)
#Docks2
Docks = card("W1", dice.Sword_3)
Docks2 = card("W2",  dice.Political, dice.Castle, dice.Castle, dice.Castle)
#undertaker1
Undertaker = card("GR2", dice.Sword_4)
#Kingmaker1
Kingmaker = card("BK2", dice.Sword_6, dice.Political, dice.Castle, dice.Castle, dice.Castle)
#Player 1 Upgrade
P1_UpGrade = card("P1_UpGrade", dice.Sword_4, dice.Castle, dice.Castle, dice.Political, dice.Political, dice.Wizard)
#Player 2 Upgrade
P2_UpGrade = card("P2_UpGrade", dice.Sword_4, dice.Castle, dice.Castle, dice.Political, dice.Political, dice.Wizard)
#Player 3 Upgrade
P3_UpGrade = card("P3_UpGrade", dice.Sword_4, dice.Castle, dice.Castle, dice.Political, dice.Political, dice.Wizard)
#Player 4 Upgrade
P4_UpGrade = card("P4_UpGrade", dice.Sword_4, dice.Castle, dice.Castle, dice.Political, dice.Political, dice.Wizard)
#Player 5 Upgrade
P5_UpGrade = card("P5_UpGrade", dice.Sword_4, dice.Castle, dice.Castle, dice.Political, dice.Political, dice.Wizard)
#Player 6 Upgrade
P6_UpGrade = card("P6_UpGrade", dice.Sword_4, dice.Castle, dice.Castle, dice.Political, dice.Political, dice.Wizard)
#Generic Upgrade
G1_UpGrade = card("G1_UpGrade", dice.Sword_3, dice.Castle, dice.Castle, dice.Wizard, dice.Political, dice.Sword_2)
#Generic 2 Upgrade
G2_UpGrade = card("G2_UpGrade", dice.Sword_3, dice.Castle, dice.Castle, dice.Wizard, dice.Political, dice.Sword_3)

for target in [Priest, Priest2, Priest3, Priest4, Warrior, Warrior2, Warrior3, Wizard, Wizard2, Wizard3, Kingmakersmith, Kingmakersmith2, Kingmakersmith3, Builder, Builder2, Mancer, Mancer2, Docks, Docks2, Undertaker, Kingmaker, P1_UpGrade, P2_UpGrade, P3_UpGrade, P4_UpGrade, P5_UpGrade, P6_UpGrade, G1_UpGrade, G2_UpGrade]:

    # test_buy(target)
    test_buy(target, number_of_tests=10_000)
