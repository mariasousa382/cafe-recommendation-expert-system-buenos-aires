try:
    import pyswip
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyswip"])
    import pyswip

import tempfile, os
from pyswip import Prolog, Functor, Atom
from pyswip.prolog import Variable

KB = r'''
% cafes_fixed.pl -- simplified KB for Python-driven menus
:- dynamic known/3.

% Cafe facts (name, distance, budget, outlets, noise_level, crowdedness, goods, closing_time, wifi_quality, size)
cafe('Amayta Patisserie', between_1_and_2km, between_10k_20k, yes, mid, sometimes_crowded, full_menu, closes_after_9, high, large).
cafe('Casa Dingo', over_3km, under_10k, yes, mid, sometimes_crowded, full_menu, closes_between_7_and_9, high, large).
cafe('Casa Telma', between_2_and_3km, between_10k_20k, yes, mid, usually_crowded, full_menu, closes_between_7_and_9, high, large).
cafe('Divino Budin', less_than_1km, under_10k, no, low, rarely_crowded, coffee_and_pastries, closes_between_7_and_9, high, small).
cafe('Doxa cafe y vino', between_2_and_3km, between_10k_20k, no, low, rarely_crowded, full_menu, closes_between_7_and_9, high, small).
cafe('Guaduchi Coffee House', over_3km, between_10k_20k, yes, low, rarely_crowded, full_menu, closes_between_7_and_9, high, medium).
cafe('Hobby - Cafe de Especialidad', over_3km, between_10k_20k, yes, mid, sometimes_crowded, coffee_and_pastries, closes_after_9, high, large).
cafe('Kopi Cafe', over_3km, between_10k_20k, yes, mid, sometimes_crowded, full_menu, closes_between_7_and_9, high, large).
cafe('Lharmonie', over_3km, between_10k_20k, yes, mid, rarely_crowded, full_menu, closes_after_9, mid, medium).
cafe('Llama Coffee Roasters', between_1_and_2km, between_10k_20k, yes, low, sometimes_crowded, just_coffee, closes_between_7_and_9, mid, large).
cafe('Lobo Café Puerto Madero', between_2_and_3km, between_10k_20k, no, low, sometimes_crowded, full_menu, closes_after_9, high, large).
cafe('Magnolia''s Cafe', over_3km, under_10k, no, low, rarely_crowded, full_menu, closes_between_7_and_9, high, small).
cafe('Manifiesto (Retiro)', less_than_1km, under_10k, yes, mid, usually_crowded, full_menu, closes_between_7_and_9, high, medium).
cafe('Merci', between_2_and_3km, between_10k_20k, yes, low, rarely_crowded, full_menu, closes_between_7_and_9, mid, medium).
cafe('Moshu Treehouse', over_3km, between_10k_20k, yes, mid, sometimes_crowded, full_menu, closes_between_7_and_9, mid, large).
cafe('Posdata Cafe Postal', less_than_1km, under_10k, no, low, rarely_crowded, coffee_and_pastries, closes_between_7_and_9, mid, small).
cafe('Punto Café', less_than_1km, under_10k, yes, mid, sometimes_crowded, full_menu, closes_between_7_and_9, high, medium).
cafe('Rajatabla cafe', between_1_and_2km, between_10k_20k, yes, mid, usually_crowded, full_menu, closes_between_7_and_9, high, large).
cafe('Sorbo Cafe', between_2_and_3km, between_10k_20k, yes, mid, usually_crowded, full_menu, closes_between_7_and_9, high, medium).
cafe('Tostado - Corrientes y Esmeralda', less_than_1km, under_10k, yes, mid, usually_crowded, full_menu, closes_between_7_and_9, high, large).
cafe('Usina Cafetera Recoleta', between_2_and_3km, between_10k_20k, yes, mid, usually_crowded, full_menu, closes_between_7_and_9, high, large).
cafe('WAT Coffee', between_2_and_3km, under_10k, yes, mid, rarely_crowded, coffee_and_pastries, closes_between_7_and_9, high, medium).
cafe('Yen Cafe', over_3km, under_10k, yes, low, rarely_crowded, full_menu, closes_between_7_and_9, high, medium).

% --------- Matching helper ----------
% If user said no preference on attribute A, succeed.
match_attr(A, _) :-
    known(no_preference, A, none), !.

% If user selected one or more yes values, any matching yes value succeeds.
match_attr(A, CafeValue) :-
    known(yes, A, CafeValue), !.

% If attribute hasn't been asked yet (no known fact), succeed (don't filter on it yet)
match_attr(A, _) :-
    \+known(_, A, _), !.

% Otherwise fail (means this cafe doesn't match user's preferences)
match_attr(_, _) :- fail.

% Top-level matcher: all attributes must match (or be no_preference)
matches_criteria(Name) :-
    cafe(Name, Dist, Budget, Outlets, Noise, Crowd, Goods, Close, Wifi, Size),
    match_attr(distance, Dist),
    match_attr(budget, Budget),
    match_attr(outlets, Outlets),
    match_attr(noise_level, Noise),
    match_attr(crowdedness, Crowd),
    match_attr(goods, Goods),
    match_attr(closing_time, Close),
    match_attr(wifi_quality, Wifi),
    match_attr(size, Size).
'''

# Write KB to temp file
fd, kb_path = tempfile.mkstemp(suffix='.pl', text=True)
with os.fdopen(fd, 'w') as f:
    f.write(KB)

# Start Prolog and consult KB
prolog = Prolog()
prolog.consult(kb_path)

# Simple utility to assert known facts
def assert_no_preference(attr):
    # store as known(no_preference, Attr, none).
    prolog.assertz(f"known(no_preference, {attr}, none)")

def assert_yes(attr, value):
    # store as known(yes, Attr, Value).
    prolog.assertz(f"known(yes, {attr}, {value})")

# Menu definitions (display_label, prolog_atom)
MENUS = {
    'distance': [
        ("Less than 1 km", "less_than_1km"),
        ("1-2 km", "between_1_and_2km"),
        ("2-3 km", "between_2_and_3km"),
        ("Over 3 km", "over_3km")
    ],
    'budget': [
        ("Under 10k", "under_10k"),
        ("10k-20k", "between_10k_20k"),
        ("Over 20k", "over_20k")
    ],
    'outlets': [
        ("Yes", "yes"),
        ("No", "no")
    ],
    'noise_level': [
        ("Low", "low"),
        ("Mid", "mid"),
        ("High", "high")
    ],
    'crowdedness': [
        ("Rarely crowded", "rarely_crowded"),
        ("Sometimes crowded", "sometimes_crowded"),
        ("Usually crowded", "usually_crowded")
    ],
    'goods': [
        ("Just coffee", "just_coffee"),
        ("Coffee and pastries", "coffee_and_pastries"),
        ("Full menu", "full_menu")
    ],
    'closing_time': [
        ("Closes before 7 PM", "closes_before_7"),
        ("Closes between 7-9 PM", "closes_between_7_and_9"),
        ("Closes after 9 PM", "closes_after_9")
    ],
    'wifi_quality': [
        ("Low", "low"),
        ("Mid", "mid"),
        ("High", "high")
    ],
    'size': [
        ("Small", "small"),
        ("Medium", "medium"),
        ("Large", "large")
    ]
}

# Natural language questions for each attribute
QUESTIONS = {
    'distance': "How far are you willing to walk to the cafe?",
    'budget': "What's your budget per person?",
    'outlets': "Do you need power outlets?",
    'noise_level': "What noise level do you prefer?",
    'crowdedness': "How busy do you want the cafe to be?",
    'goods': "What kind of food options do you want?",
    'closing_time': "How late do you need the cafe to be open?",
    'wifi_quality': "What WiFi quality do you need?",
    'size': "What size cafe do you prefer?"
}

# Which attributes are multi-select (user can pick more than one)
MULTISELECT = {'goods', 'distance', 'budget', 'crowdedness', 'noise_level', 'closing_time', 'wifi_quality', 'size'}

# Query an attribute from the user, assert known facts into Prolog
def ask_attr(attr):
    options = MENUS[attr]
    question = QUESTIONS.get(attr, attr.replace('_', ' ').title())
    print(f"\n{question}")

    # Showing menu options
    for i, (label, atom) in enumerate(options, start=1):
        print(f"  {i}. {label}")
    print(f"  {len(options)+1}. No preference")

    # prompt
    if attr in MULTISELECT:
        prompt = "Pick option numbers separated by commas (e.g. 1,3) or press Enter for no preference: "
    else:
        prompt = "Pick one option number or press Enter for no preference: "

    resp = input(prompt).strip()
    if not resp:
        assert_no_preference(attr)
        return
    # parse numbers
    nums = []
    for token in resp.split(','):
        token = token.strip()
        if not token:
            continue
        if not token.isdigit():
            print(f"Ignoring invalid token: {token}")
            continue
        nums.append(int(token))
    if not nums:
        assert_no_preference(attr)
        return
    # If user explicitly chose the no-preference number
    if any(n == len(options)+1 for n in nums):
        assert_no_preference(attr)
        return
    # For single-select attributes, take the first valid number
    if attr not in MULTISELECT:
        n = nums[0]
        if 1 <= n <= len(options):
            _, val = options[n-1]
            assert_yes(attr, val)
        else:
            assert_no_preference(attr)
    else:
        # multi-select: assert yes for each chosen value
        chosen_any = False
        for n in nums:
            if 1 <= n <= len(options):
                _, val = options[n-1]
                assert_yes(attr, val)
                chosen_any = True
        if not chosen_any:
            assert_no_preference(attr)

def main():
    """Main function to run the cafe recommendation system."""
    print("=" * 60)
    print("Welcome to the Buenos Aires Cafe Finder!")
    print("=" * 60)
    print("\nLet's find the perfect cafe for you.")
    # clear any previous known facts
    prolog.retractall("known(_,_,_)")
    # Ask attributes in a sensible order (you can change)
    order = ['distance','budget','outlets','noise_level','crowdedness','goods','closing_time','wifi_quality','size']
    for a in order:
        ask_attr(a)
        # Check for matches after each question - stop early if no matches possible
        results = list(prolog.query("matches_criteria(Name).", maxresult=1))
        if not results:
            print(f"\n No cafes match your criteria so far (after selecting {a.replace('_', ' ')}).")
            print("Stopping early to save time. Try adjusting your preferences!")
            return

    # Final query to get all matches
    results = list(prolog.query("matches_criteria(Name).", maxresult=100))
    if results:
        print(f"\nFound {len(results)} matching cafe(s):")
        for i, sol in enumerate(results, start=1):
            name = sol['Name']
            # pyswip may return bytes for atoms on some setups; coerce
            if isinstance(name, bytes):
                name = name.decode('utf-8')
            print(f"{i}. {name}")
    else:
        print("\nNo cafes match your criteria. Try relaxing preferences.")

if __name__ == "__main__":
    try:
        main()
    finally:
        # cleanup kb file
        try:
            os.remove(kb_path)
        except Exception:
            pass

