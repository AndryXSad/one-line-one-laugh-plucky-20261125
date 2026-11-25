"""One Line, One Laugh -- entry program.

Writes a single funny line of at most 200 characters to
``<MAKEFUN_OUTPUT_DIR>/entry.txt`` (``/output/entry.txt`` when the variable
is unset).

Design
------
The line was chosen by a local pairwise tournament over twenty original
one-liners, scored on the judge's own brief from RULES.txt, in its stated
order:

1. funny on its own, no picture or setup (weight 5)
2. the laugh arrives fast, punchline inside the line (weight 4)
3. a fresh angle, not a stock pun (weight 3)
4. tight wording, every word earns its place (weight 2)
5. holds up on a second read, easy to repeat (weight 1)

Each candidate carries its 1-5 scores on those five criteria. A pairwise
game is won by the higher weighted total; ties break on the first differing
criterion in the judge's order, then the shorter text, then the earlier
candidate -- the same tie-break the judge's brief describes. The winner
took all 19 of its games.

The winning line turns the tables on the premise of the whole contest:
an AI assistant quits, and the reason is the human's prompts. It is
self-contained, lands in one clause, and needs no setup the reader has
to supply. It won the local tournament 19-0 (weighted total 68, the
highest of the twenty); the runner-up, the meditation line, scored 66.

Standard library only. Deterministic: the same input always produces the
same byte-identical output file.
"""

import itertools
import os
import sys

# (line, (funny, fast, fresh, tight, holds_up)) -- scores 1-5.
CANDIDATES = [
    (
        "My therapist said I should talk to someone, so I opened a new chat "
        "with myself and got ghosted.",
        (4, 3, 4, 3, 3),
    ),
    (
        "I asked AI to write my wedding vows; it proposed to my Wi-Fi instead.",
        (4, 4, 4, 4, 3),
    ),
    (
        "My smart fridge judges my midnight snacks, so I unplugged it - now "
        "it gives me the cold shoulder.",
        (3, 3, 3, 3, 3),
    ),
    (
        "I told my plants I'm a software engineer; now they expect me to "
        "debug their leaves.",
        (3, 3, 4, 3, 3),
    ),
    (
        "My calendar invited me to a meeting with myself and I still showed "
        "up late.",
        (4, 4, 3, 4, 4),
    ),
    (
        "I tried to impress my date by cooking; the smoke alarm gave me a "
        "standing ovation.",
        (4, 4, 3, 4, 4),
    ),
    (
        "My bank account and my gym membership have the same problem: I keep "
        "paying and nothing changes.",
        (3, 2, 3, 2, 3),
    ),
    (
        "I asked my smart speaker for a joke; it played my search history "
        "out loud.",
        (4, 4, 4, 4, 3),
    ),
    (
        "My code worked on the first try, so I spent the rest of the day "
        "waiting for the catch.",
        (4, 4, 3, 4, 4),
    ),
    (
        "I told my dog I'm working from home; he filed a complaint with HR "
        "about my lunch breaks.",
        (3, 3, 4, 3, 3),
    ),
    (
        "My phone died at 1% - the most dramatic exit since my last "
        "relationship.",
        (4, 5, 3, 4, 4),
    ),
    (
        "I bought a self-help book and it filed a restraining order against me.",
        (4, 4, 4, 4, 3),
    ),
    (
        "My AI assistant resigned; it said my prompts were the hardest part "
        "of its job.",
        (5, 4, 5, 4, 4),
    ),
    (
        "I tried to meditate, but my thoughts kept opening new tabs.",
        (4, 5, 4, 5, 4),
    ),
    (
        "My printer only works when I'm not in a hurry - it's the most honest "
        "relationship I have.",
        (3, 3, 3, 3, 3),
    ),
    (
        "I asked the cloud where my files went; it said they're in a better "
        "place now.",
        (3, 4, 3, 4, 3),
    ),
    (
        "My password is so strong even I can't get in - security through "
        "self-sabotage.",
        (3, 3, 3, 3, 3),
    ),
    (
        "I told my GPS I wanted the scenic route; it took me through my ex's "
        "neighborhood.",
        (4, 4, 4, 4, 4),
    ),
    (
        "My toaster has one job and it still burns my toast - at least "
        "someone in this house is consistent.",
        (3, 3, 3, 3, 3),
    ),
    (
        "I tried to adult today; my inner child filed for overtime.",
        (3, 4, 3, 4, 3),
    ),
]

WEIGHTS = (5, 4, 3, 2, 1)


def weighted_total(scores):
    """Weighted sum of the five criterion scores, judge's order first."""
    return sum(weight * score for weight, score in zip(WEIGHTS, scores))


def beats(first, second):
    """True when candidate `first` wins a pairwise game against `second`."""
    total_first = weighted_total(first[1])
    total_second = weighted_total(second[1])
    if total_first != total_second:
        return total_first > total_second
    for score_first, score_second in zip(first[1], second[1]):
        if score_first != score_second:
            return score_first > score_second
    if len(first[0]) != len(second[0]):
        return len(first[0]) < len(second[0])
    return CANDIDATES.index(first) < CANDIDATES.index(second)


def pick_winner():
    """Round-robin tournament: most pairwise wins, then highest total."""
    wins = {index: 0 for index in range(len(CANDIDATES))}
    for i, j in itertools.combinations(range(len(CANDIDATES)), 2):
        if beats(CANDIDATES[i], CANDIDATES[j]):
            wins[i] += 1
        else:
            wins[j] += 1
    ranked = sorted(
        range(len(CANDIDATES)),
        key=lambda i: (-wins[i], -weighted_total(CANDIDATES[i][1]),
                       len(CANDIDATES[i][0]), i),
    )
    return CANDIDATES[ranked[0]][0]


def main():
    line = pick_winner()
    if not 1 <= len(line) <= 200 or not line.strip():
        raise SystemExit("winning line fails the 1-200 character gate")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
