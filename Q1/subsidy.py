"""Q1 - Electricity subsidy: separate ifs (buggy) vs if-elif-else, nested vs combined conditions.
Household = (units, has_ration_card, has_member_above_80)."""

def decide_separate_ifs(units, ration, elder):
    """Developer's version: separate if statements. Returns a LIST of every subsidy given."""
    given = []
    if units <= 100:
        given.append("subsidy")
    if units <= 200 and ration:                 # does not exclude units <= 100
        given.append("partial subsidy")
    if elder:                                   # forgot 'units > 200'
        given.append("subsidy")
    return given

def decide_elif(units, ration, elder):
    """Correct version: if-elif-else, exactly ONE decision. Chained comparison for the middle slab."""
    if units <= 100:
        return "subsidy"
    elif 101 <= units <= 200:
        return "partial subsidy" if ration else "none"
    else:                                       # above 200
        return "subsidy" if elder else "none"

def decide_nested(units, ration, elder):
    """Nested ifs."""
    if units <= 100:
        return "subsidy"
    else:
        if units <= 200:
            if ration:
                return "partial subsidy"
            else:
                return "none"
        else:
            if elder:
                return "subsidy"
            else:
                return "none"

def decide_combined(units, ration, elder):
    """Combined Boolean conditions in one flat elif chain."""
    if units <= 100:
        return "subsidy"
    elif 101 <= units <= 200 and ration:
        return "partial subsidy"
    elif units > 200 and elder:
        return "subsidy"
    else:
        return "none"
