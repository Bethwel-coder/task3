% --- FACTS: parent(Parent, Child) ---
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).

% --- RULES ---

% X is a grandparent of Z if X is a parent of Y, and Y is a parent of Z
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% X and Y are siblings if they share the same parent
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.