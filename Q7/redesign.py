"""Q7 - Diagnose, redesign and validate.
Chosen program: Q1's if-elif slab decision, when the tariff grows from 3 slabs to k slabs (requirement changes / input grows).
Original  : if-elif chain / linear search of slabs        -> comparisons grow with k  (O(k))
Redesign  : binary search written by hand on the sorted limits -> comparisons ~ log2(k) (O(log k))
Both versions COUNT the comparisons they make."""
import random

def make_slabs(k, step=10):
    """k slabs: upper limits step, 2*step, ... k*step (units); slab i has decision label i; last slab is open-ended."""
    limits = [step * (i + 1) for i in range(k - 1)]       # k-1 limits, the k-th slab is 'above the last limit'
    labels = list(range(k))
    return limits, labels

def decide_linear(units, limits, labels):
    """ORIGINAL: check slab after slab (what the if-elif chain does). Returns (label, comparisons)."""
    comparisons = 0
    for i, limit in enumerate(limits):
        comparisons += 1
        if units <= limit:
            return labels[i], comparisons
    return labels[-1], comparisons

def decide_binary(units, limits, labels):
    """REDESIGN: limits are sorted, so each comparison can discard half of the remaining slabs.
    Finds the first index i with units <= limits[i]. Returns (label, comparisons)."""
    low, high = 0, len(limits)                            # search window [low, high); high = 'above all limits'
    comparisons = 0
    while low < high:
        mid = (low + high) // 2
        comparisons += 1
        if units <= limits[mid]:
            high = mid                                    # answer is mid or to its left
        else:
            low = mid + 1                                 # answer is to the right
    return labels[low], comparisons
