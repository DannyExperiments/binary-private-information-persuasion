import Std

/-! Rational inequalities for the 3-SAT tests and the final payoff gap.
    This file does not formalize the persuasion model, message optimization,
    or the complexity reduction. -/
namespace PersuasionCertificate
open Lean.Grind

def low (t x : Rat) : Rat := t/8-x
def high (t x : Rat) : Rat := x-7*t/8
def clause (t x y z : Rat) : Rat := x+y+z-t/2

theorem oppositeAlternatives (t x anchor : Rat)
    (ht : 0 ≤ t) (ha : 0 < anchor) :
    ¬ (anchor/2 ≤ low t x ∧ anchor/2 ≤ high t x) := by
  unfold low high
  grind

theorem falseClause (t a b c : Rat) (ht : 0 ≤ t)
    (ha : a ≤ t/8) (hb : b ≤ t/8) (hc : c ≤ t/8) :
    clause t a b c ≤ -t/8 ∧ clause t a b c ≤ 0 := by
  unfold clause
  grind

theorem assignmentMargins (anchor : Rat) (h : 0 < anchor) :
    let t := 32*anchor
    let xf := t/16
    let xt := 15*t/16
    anchor < t-xf ∧ anchor < t-xt ∧ anchor < low t xf ∧ anchor < high t xt := by
  dsimp [low, high]
  grind

theorem trueClause (anchor a b c : Rat) (h : 0 < anchor)
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hbig : 30*anchor ≤ a ∨ 30*anchor ≤ b ∨ 30*anchor ≤ c) :
    anchor < clause (32*anchor) a b c := by
  unfold clause
  grind

theorem testSurvivesAverage (split ordinary imbalance anchor : Rat)
    (hclose : split - ordinary ≤ 3*imbalance)
    (hpass : anchor ≤ split) (hsmall : 3*imbalance ≤ anchor/2) :
    anchor/2 ≤ ordinary := by
  grind

theorem absorbingGuardLoss (base anchorUnit lostGuard value : Rat)
    (hloss : 0 ≤ lostGuard)
    (hvalue : value ≤ base - lostGuard/2 + (3/16)*lostGuard + anchorUnit/4) :
    value ≤ base + anchorUnit/4 := by
  grind

theorem thresholdGap (base unit yes no : Rat)
    (hunit : 0 ≤ unit) (hy : base + unit ≤ yes) (hn : no ≤ base + unit/4) :
    base + unit/2 + unit/4 ≤ yes ∧ no ≤ base + unit/2 - unit/4 := by
  grind

#print axioms oppositeAlternatives
#print axioms falseClause
#print axioms assignmentMargins
#print axioms trueClause
#print axioms testSurvivesAverage
#print axioms absorbingGuardLoss
#print axioms thresholdGap
end PersuasionCertificate
