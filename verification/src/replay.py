#!/usr/bin/env python3
"""Replay small private-channel instances using exact rational arithmetic."""
from fractions import Fraction as Q
from itertools import product


def test_forms(n, clauses):
    tests = []
    for i in range(1, n + 1):
        for a, b in ((1, -1), (Q(1, 8), -1), (Q(-7, 8), 1)):
            row = [Q(0)] * (n + 1)
            row[0], row[i] = Q(a), Q(b)
            tests.append(tuple(row))
    for terms in clauses:
        row = [Q(-1, 2)] + [Q(0)] * n
        for lit in terms:
            if lit > 0:
                row[lit] += 1
            else:
                row[0] += 1
                row[-lit] -= 1
        tests.append(tuple(row))
    assert all(abs(coefficient) <= 3 for row in tests for coefficient in row)
    return tests


def dot(x, y):
    return sum(a * b for a, b in zip(x, y))


def build_instance(n, clauses):
    tests = test_forms(n, clauses)
    count = len(tests)
    anchor = Q(1, 256 * (n + 1))
    a = Q(1, 64 * count)
    b = Q(1, 2)
    delta = anchor / (12 * count)
    pair_prior = (1 - anchor) / (2 * (n + 1))
    prior = (pair_prior,) * (2 * (n + 1)) + (anchor,)
    receiver = (Q(1), Q(-1)) * (n + 1) + (-delta,)
    num_states = len(prior)
    guards = [tuple(b if j // 2 == i else Q(0) for j in range(num_states)) for i in range(n + 1)]
    tests_channel = [
        tuple(prob for c in row for prob in (a * delta * max(c, 0), a * delta * max(-c, 0))) + (a,)
        for row in tests
    ]
    receiver_signals = guards + tests_channel
    used = tuple(map(sum, zip(*receiver_signals)))
    assert all(0 < p < 1 for p in used)
    assert all(p <= b + 3 * count * a * delta for p in used[:-1])
    assert used[-1] == Q(1, 64)
    padding = [tuple((1 - used[i]) if i == j else Q(0) for j in range(num_states)) for i in range(num_states)]
    channel = receiver_signals + padding
    assert all(sum(row) == 1 for row in zip(*channel))
    assert sum(prior) == 1 and len(channel) == count + 3 * (n + 1) + 1
    pad_payoff = sum(p * (1 - u) for p, d, u in zip(prior, receiver, used) if d > 0)
    baseline = pad_payoff + b * (1 - anchor)
    return prior, receiver, channel, baseline, a * anchor


def chosen_actions(message, receiver, channel):
    signed = tuple(q * d for q, d in zip(message, receiver))
    return tuple(dot(signed, r) >= 0 for r in channel)


def expected_payoff(messages, prior, receiver, channel):
    assert all(q >= 0 for message in messages for q in message)
    assert tuple(map(sum, zip(*messages))) == prior
    return sum(
        dot(message, r)
        for message in messages
        for r, action1 in zip(channel, chosen_actions(message, receiver, channel))
        if action1
    )


def satisfying_message(bits, prior):
    anchor = prior[-1]
    values = [32 * anchor] + [(30 if bit else 2) * anchor for bit in bits]
    message = tuple(v for value in values for v in (value, value)) + (anchor,)
    return message, tuple(p - q for p, q in zip(prior, message))


def check_small_positive_cases():
    cases = 0
    for bits in product((False, True), repeat=3):
        for signs in product((False, True), repeat=3):
            terms = tuple(i if sign else -i for i, sign in enumerate(signs, 1))
            satisfied = any(x == sign for x, sign in zip(bits, signs))
            prior, receiver, channel, baseline, unit = build_instance(3, (terms,))
            first, second = satisfying_message(bits, prior)
            actions = chosen_actions(first, receiver, channel)
            assert all(actions[:4])
            assert actions[4 + 9] == satisfied
            assert sum(actions[4:4 + 9]) == 6
            if satisfied:
                assert expected_payoff((first, second), prior, receiver, channel) >= baseline + 7 * unit
            cases += 1
    print(f"{cases} exact clause and guard checks over three Boolean variables")


def check_worked_pair():
    yes = ((1, 1, 1), (1, 1, 1))
    no = ((1, 1, 1), (-1, -1, -1))
    n = 1
    k = 4
    prior, receiver, channel, baseline, unit = build_instance(n, yes)
    first, second = satisfying_message((True,), prior)
    assert [first[0]/prior[-1], first[2]/prior[-1]] == [32, 30]
    assert sum(chosen_actions(first, receiver, channel)[2:7]) == k
    payoff = expected_payoff((first, second), prior, receiver, channel)
    assert payoff >= baseline + k * unit
    print(f"YES: exact two-message value {payoff}; (V-C0)/(a*mu_z) = {(payoff-baseline)/unit}")
    print(f"YES: certified lower bound {baseline + k * unit}; threshold {baseline + (k-Q(1,2))*unit}")

    prior, receiver, channel, baseline, unit = build_instance(n, no)
    tests = test_forms(n, no)
    for t, x in product(range(65), repeat=2):
        assert sum(dot(test, (t, x)) >= Q(1, 2) for test in tests) <= k - 1
    upper = baseline + (k - Q(3, 4)) * unit
    for split in product((Q(0), Q(1, 512), Q(1, 2), Q(1)), repeat=len(prior)):
        first = tuple(p * fraction for p, fraction in zip(prior, split))
        second = tuple(p - q for p, q in zip(prior, first))
        assert expected_payoff((first, second), prior, receiver, channel) <= upper
    print(f"NO: {65**2} balanced test choices and {4**len(prior)} sampled two-message policies")
    print(f"NO: certified upper bound {upper}; threshold {baseline + (k-Q(1,2))*unit}")
    assert unit == Q(1, 163840)


if __name__ == "__main__":
    check_small_positive_cases()
    check_worked_pair()
