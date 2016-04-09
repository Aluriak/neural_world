%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Cleaning of a simple binary neural network.
% Delete useless neurons (those that are not connected to an output neuron),
%  and put an orientation in the edges.
%
% Inputs:
%       - edge(i,j): neurons of id i is linked to neuron of id j.
%       - neuron(i,t): neuron of id i is typed as t, with t in IXANO (see below).
%       - output(i,D): neuron of id i is an output associated to direction D.
%       - memwrite(i,A): neuron of id i is a memory writting neuron to address A
%                      (with A in [0;memory size[)
% Outputs:
%       - edge(i,j): neurons of id i is a predecessor of neuron of id j.
%       - neuron(i,t): neuron of id i is typed as t, with t in IXANO (see below).
%       - output(i,D): neuron of id i is an output associated to direction D.
%
% IXANO is the notation of the neuron types, which are Input, Xor, And, Not and Or.
%  In the ASP code, these letter are in lowercase (constants).
%  For example, neuron(3,i) says that the neuron of id 3 's type is Input.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Keep edges oriented, from predecessor to successor.
% Input neurons can't be successor of other neurons.
oedge(X,Y):- edge(X,Y) ; X<Y ; not neuron(Y,i).
oedge(X,Y):- edge(Y,X) ; X<Y ; not neuron(X,i).

% Shortcut: a neuron is a neuron, whatever its type.
neuron(X):- neuron(X,_).

% A neuron is connected to another neuron if an oriented path exist between them.
connected(X,Y):- neuron(X) ; neuron(Y) ; oedge(X,Y).
connected(X,Y):- neuron(X) ; neuron(Y) ; oedge(X,Z) ; connected(Z,Y).

% A neuron is connected to itself.
connected(X,X):- neuron(X).

% A neuron is reachable if connected to an output and an input neurons.
reachable(X):- neuron(I,i) ; connected(I,X) ; output(O) ; connected(X,O).

#show.
#show edge(X,Y): oedge(X,Y), reachable(X), reachable(Y).
#show neuron(X,T): neuron(X,T), reachable(X).
#show output(X): output(X), reachable(X).
