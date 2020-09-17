# Knight and Knave puzzle

# each player -> knight / knave

# Knight - tells truth
# Knave - tells lie

# Goal: given a set of sentences (puzzle 0, 1, 2, 3) spoken by each of the players
#       for each player, determine whether that player is a knight or a knave.

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A cannot be both knight and knave AND either A is knight or A is knave
    And(Not(And(AKnight, AKnave)), Or(AKnight, AKnave)),
    # if A was knight, then true for A is both knight and knave
    Implication(AKnight, And(AKnight, AKnave)),
    # if A wan knave, then false for A is both knight and knave
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A cannot be both knight and knave AND either A is knight or A is knave
    And(Not(And(AKnight, AKnave)), Or(AKnight, AKnave)),
    # B cannot be both knight and knave AND either B is knight or B is knave
    And(Not(And(BKnight, BKnave)), Or(BKnight, BKnave)),
    # impossible for either A and B are both knight or A and B are both knave
    Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # if A was knight, then true for A and B are both knave
    Implication(AKnight, And(AKnave, BKnave)),
    # if A was knave, then false for A and B are both knave
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A cannot be both knight and knave AND either A is knight or A is knave
    And(Not(And(AKnight, AKnave)), Or(AKnight, AKnave)),
    # B cannot be both knight and knave AND either B is knight or B is knave
    And(Not(And(BKnight, BKnave)), Or(BKnight, BKnave)),
    # impossible for either A and B are both knight or A and B are both knave
    Not(Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # if A was knight, then true for A and B are either both knight or either both knave
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # if A was knave, then false for A and B are either both knight or either both knave
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    # if B was knight, then true for either A is knight and B is knave or A is knave and B is knight
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # if B was knave, then false for either A is knight and B is knave or A is knave and B is knight
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A cannot be both knight and knave AND either A is knight or A is knave
    And(Not(And(AKnight, AKnave)), Or(AKnight, AKnave)),
    # B cannot be both knight and knave AND either B is knight or B is knave
    And(Not(And(BKnight, BKnave)), Or(BKnight, BKnave)),
    # B cannot be both knight and knave AND either B is knight or B is knave
    And(Not(And(CKnight, CKnave)), Or(CKnight, CKnave)),
    # impossible for either A, B and C are all knight or A, B and C are all knave
    Not(Or(And(AKnight, BKnight, CKnight), And(AKnave, BKnave, CKnave))),
    # if A was knight, then true for either A is knight or knave
    Implication(AKnight, Or(AKnight, AKnave)),
    # if A was knave, then false for either A is knight or knave
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # if B was knight, then true for A is knave and C is knave
    Implication(BKnight, And(AKnave, CKnave)),
    # if B was knave, then false for A is knave and C is knave
    Implication(BKnave, Not(And(AKnave, CKnave))),
    # if C was knight, then true for A is knight
    Implication(CKnight, AKnight),
    # if C was knave, then false for A is knight
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
