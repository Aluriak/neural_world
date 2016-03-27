%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Modelization of a simple binary neural network.
%
% Inputs:
%       - up(i): i is the id of a up-state input neuron.
%       - down(i): i is the id of a down-state input neuron.
%       - edge(i,j): neurons of id i is a predecessor of neuron of id j.
%       - neuron(i,t): neuron of id i is typed as t, with t in IXANO (see below).
% Outputs:
%       - up(i): i is the id of a up-state neuron.
%       - down(i): i is the id of a down-state neuron.
%       - output_up(i): i is the id of a up-state output neuron.
%
% IXANO is the notation of the neuron types, which are Input, Xor, And, Not and Or.
%  In the ASP code, these letter are in lowercase (constants).
%  For example, neuron(3,i) says that the neuron of id 3 's type is Input.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Shortcut: a neuron is a neuron, whatever is its type.
neuron(X):- neuron(X,_).


% All edges must link smaller neurons to higher neurons.
:- edge(X, Y) ; X > Y.

% All neurons must have an IXANO type.
type((i;x;a;n;o)).
:- neuron(_,T) ; not type(T).

% A neuron is down if not up.
down(X):- not up(X) ; neuron(X).


% A neuron of type XOR is up iif there is exactly one up-state predecessor.
up(Y):- neuron(Y,x) ; 1 { edge(X,Y): up(X) } 1.

% A neuron of type AND is up iif none of its predecessor is down.
up(Y):- neuron(Y,a) ; not neuron(X): edge(X,Y), down(X).

% A neuron of type OR is up iif at least one of its predecessor is up.
up(Y):- neuron(Y,o) ; edge(X,Y) ; up(X).

% A neuron of type NOT is up iif its predecessor is down.
up(Y):- neuron(Y,n) ; edge(X,Y) ; down(X).


% outputs all id of output neurons that are in up state.
#show.
#show up/1.
#show down/1.
#show output_up(X): output(X), up(X).
