function createfigure(X1, Y1)
%CREATEFIGURE(X1, Y1)
%  X1:  vector of plot x data
%  Y1:  vector of plot y data

%  Auto-generated by MATLAB on 16-Oct-2024 14:35:23

% Create figure
figure1 = figure;

% Create axes
axes1 = axes('Parent',figure1);
hold(axes1,'on');

% Create plot
plot(X1,Y1,'LineWidth',1);

% Create ylabel
ylabel({'Voltaggio [V]'});

% Create xlabel
xlabel({'Tempo [s]'});

% Create title
title({'Impulso di 90ns'},'FontSize',18);

box(axes1,'on');
hold(axes1,'off');
% Set the remaining axes properties
set(axes1,'XGrid','on','YGrid','on');
