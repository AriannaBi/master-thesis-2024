(declare-const x Int)
(assert (forall ((v Int)) (= v (* x x))))
(check-sat)