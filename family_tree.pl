% =============================================================================
%  CUSTOM FAMILY TREE — Prolog Program
%
%  Family structure (3 generations):
%
%  Generation 1 (Grandparents):
%    George + Mary (paternal)   |   Henry + Ruth (maternal)
%
%  Generation 2 (Parents / Aunts / Uncles):
%    James (son of George & Mary) married to Susan (daughter of Henry & Ruth)
%    Carol (daughter of George & Mary)  ← aunt
%    Paul  (son of Henry & Ruth)        ← uncle
%
%  Generation 3 (Children / Grandchildren / Cousins):
%    Alice, Tom  → children of James & Susan
%    Emma        → child  of Carol  (cousin of Alice & Tom)
%    Luke        → child  of Paul   (cousin of Alice & Tom)
%
% =============================================================================
 
 
% ─── SECTION 1: BASE FACTS ───────────────────────────────────────────────────
% Format: parent(Parent, Child)
% These are the raw facts from which all rules are derived.
 
% George and Mary's children
parent(george, james).
parent(george, carol).
parent(mary,   james).
parent(mary,   carol).
 
% Henry and Ruth's children
parent(henry, susan).
parent(henry, paul).
parent(ruth,  susan).
parent(ruth,  paul).
 
% James and Susan's children
parent(james, alice).
parent(james, tom).
parent(susan, alice).
parent(susan, tom).
 
% Carol's child
parent(carol, emma).
 
% Paul's child
parent(paul,  luke).
 
 
% ─── SECTION 2: GENDER FACTS ─────────────────────────────────────────────────
% Needed to distinguish mother/father, aunt/uncle, etc.
 
male(george).
male(henry).
male(james).
male(paul).
male(tom).
male(luke).
 
female(mary).
female(ruth).
female(susan).
female(carol).
female(alice).
female(emma).
 
 
% ─── SECTION 3: MARRIAGE FACTS ───────────────────────────────────────────────
% spouse/2 is symmetric (if A is married to B, B is married to A)
 
married(george, mary).
married(henry,  ruth).
married(james,  susan).
 
spouse(X, Y) :- married(X, Y).
spouse(X, Y) :- married(Y, X).   % make it bidirectional
 
 
% =============================================================================
%  SECTION 4: DERIVED RULES
%  Each rule is built from parent/2 and gender/1 facts above.
% =============================================================================
 
% ── Father: a parent who is male ─────────────────────────────────────────────
father(F, C) :-
    parent(F, C),
    male(F).
 
% ── Mother: a parent who is female ───────────────────────────────────────────
mother(M, C) :-
    parent(M, C),
    female(M).
 
% ── Child: inverse of parent ─────────────────────────────────────────────────
% child(Child, Parent)
child(C, P) :- parent(P, C).
 
% ── Son: a child who is male ─────────────────────────────────────────────────
son(S, P) :-
    child(S, P),
    male(S).
 
% ── Daughter: a child who is female ──────────────────────────────────────────
daughter(D, P) :-
    child(D, P),
    female(D).
 
% ── Grandparent: parent of a parent ──────────────────────────────────────────
% grandparent(Grandparent, Grandchild)
grandparent(GP, GC) :-
    parent(GP, P),
    parent(P,  GC).
 
% ── Grandfather ───────────────────────────────────────────────────────────────
grandfather(GF, GC) :-
    grandparent(GF, GC),
    male(GF).
 
% ── Grandmother ───────────────────────────────────────────────────────────────
grandmother(GM, GC) :-
    grandparent(GM, GC),
    female(GM).
 
% ── Grandchild: inverse of grandparent ───────────────────────────────────────
grandchild(GC, GP) :- grandparent(GP, GC).
 
% ── Sibling: two people with at least one common parent ──────────────────────
% X \= Y prevents a person being their own sibling
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.
 
% ── Brother: a male sibling ───────────────────────────────────────────────────
brother(B, X) :-
    sibling(B, X),
    male(B).
 
% ── Sister: a female sibling ──────────────────────────────────────────────────
sister(S, X) :-
    sibling(S, X),
    female(S).
 
% ── Uncle: a brother of one's parent ─────────────────────────────────────────
uncle(U, C) :-
    parent(P, C),
    brother(U, P).
 
% ── Aunt: a sister of one's parent ───────────────────────────────────────────
aunt(A, C) :-
    parent(P, C),
    sister(A, P).
 
% ── Cousin: children of siblings ─────────────────────────────────────────────
% X and Y are cousins if their parents are siblings
cousin(X, Y) :-
    parent(PX, X),
    parent(PY, Y),
    sibling(PX, PY),
    X \= Y.
 
 
% =============================================================================
%  SAMPLE QUERIES — paste these one at a time into the SWI-Prolog console
%  after loading this file with: ?- consult('family_tree.pl').
% =============================================================================
%
%  --- Check specific relationships ---
%  ?- grandparent(george, alice).       % Is George Alice's grandparent? → true
%  ?- grandmother(ruth, tom).           % Is Ruth Tom's grandmother?     → true
%  ?- uncle(paul, alice).               % Is Paul Alice's uncle?         → true
%  ?- aunt(carol, alice).               % Is Carol Alice's aunt?         → true
%  ?- cousin(alice, emma).              % Are Alice and Emma cousins?    → true
%  ?- cousin(tom, luke).                % Are Tom and Luke cousins?      → true
%
%  --- List all members of a relationship ---
%  ?- grandchild(GC, george).           % Who are George's grandchildren?
%  ?- grandparent(GP, alice).           % Who are Alice's grandparents?
%  ?- uncle(U, alice).                  % Who are Alice's uncles?
%  ?- aunt(A, tom).                     % Who are Tom's aunts?
%  ?- cousin(C, alice).                 % Who are Alice's cousins?
%  ?- sibling(S, james).                % Who are James's siblings?
%
%  --- General queries ---
%  ?- parent(X, alice).                 % Who are Alice's parents?
%  ?- child(C, james).                  % Who are James's children?
%  ?- grandfather(GF, emma).            % Who is Emma's grandfather?
%  ?- spouse(james, X).                 % Who is James married to?
 