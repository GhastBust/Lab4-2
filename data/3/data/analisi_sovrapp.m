% Nome del file CSV
filename = ['opamp_triang.csv'];

% Importa il file CSV in una matrice
M = readmatrix(filename);


t=M(3:end,1);
V_1=M(3:end,2);
%V_2=M(3:end,3);


createfigure(t,V_1);
%hold on;
%plot(t,V_2);

