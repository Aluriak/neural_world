%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Data test for neural_solving.lp ASP source code.
% Defines a little neural network and possible inputs.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%% NEURAL NETWORK %%%%
% Input neurons
neuron(1,i).
neuron(2,i).
neuron(3,i).
neuron(4,i).
% intermediary neurons
neuron(5,a).
neuron(6,o).
neuron(7,n).
neuron(8,x).
% output neurons (OR type)
neuron(9,o).
neuron(10,o).
% edges
edge((1;2),5).
edge((3;4),6).
edge(6,7).
edge((7;5),8).
edge(8,9).
edge(7,10).

%%%% INPUT STATES SETS %%%%
up(1;2;3;4).
%up(2;3;4). down(1).
%up(1;3;4). down(2).
%up(1;2;4). down(3).
%up(1;2;3). down(4).
%up(1;2). down(3;4).
%up(2). down((1;3;4)).
