# IAI
Itemizing Artificial Intelligence:
A Project exploring learning in an inventory allotment scenario.
Gives an agent the opportunity to learn the best itemization schemes

Authors:
    Michael Chadbourne
    Tim Webber
    Mateo Freye

Last Edited: 12/10/15

Files:
    items.py:
    contains the item classes as well as instantiations of the items which make
    up the item-store's catalog.

    shopping.py:
    contains the processes used in assigning a personal inventory from the stock
    available in the item-store. This is where the learning-agent applies it's
    knowledge.

    gameObjects.py:
    contains the classes which represent the structure of the testing
    environment. This is where the learning-agent gathers new information, and
    Tests the effectiveness of their item build.

    IAI.py:
    The Main-File for the project: Runs the testing suite and displays results.

DESIGN:
    items.py contains item classes used by the shop, and in the hunting phase.
    These classes, while not enforced by python, must be adhered to when
    creating new items, so as to assure consistency of function.

    shopping.py uses the a <FORMAT DECISION> passed to it, to generate an
    inventory based upon the items available in <FORMAT DECISION> and the
    knowledge of items learned from "Journal Entries" received from the hunting
    phase.

    The JOURNAL ENTRIES are in the format:
    (String action, int time, int hp, int hits) or
    ("HIT", int time, int hp, Listof<String> tags)

    Where 'action' is 'MOVE' or the name of an item.
    'time' is the number of turns since the level began
    'hp' is the Hero's hp after the reported action occurred
    'hits' is the number of enemies affected by the action
    and 'tags' in the "HIT" case is a List of iterm-names where each name in the
        list is a weapon which could have helped the hero.
        
