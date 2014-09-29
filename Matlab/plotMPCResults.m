%%
%This file is used to plot what the state-space model thinks it's doing at
%each step, both when seeing the experimental data and when no experimental
%data is given to it.

%Introduce experiment data here. It must have the following structure:
%column 1 --> times; column 2 --> fluorescence; column 3 --> reference;
%column 4 --> inputs; column 5 --> hidden states.
data=MPCsin17072014;

%%
%Introduce SS model here

%Old cytometer
% % A=[0.1028   -0.3208   -0.1697
% %    0.6076    0.7442   -0.1385
% %    0.0620    0.1414    0.9919];
% % B=[1.2150
% %    0.9915
% %    0.0582];
% % C=[0         0    0.2151];

%10 minutes sampling
% % A=  [0.3271   -0.3858   -0.1124
% %     0.3979    0.8597   -0.0413
% %     0.0366    0.1484    0.9977];
% % B=[ 0.7958
% %     0.2925
% %     0.0164];
% % C=[0         0    0.1531];

%5 minutes sampling
A=[0.6231   -0.2403   -0.0710;
    0.2515    0.9597   -0.0120;
    0.0106    0.0770    0.9997];
    
B=[    0.5029;
    0.0847;
    0.0023];

C=[    0         0    0.1531];


R=1;
Q=eye(length(A))*100;
P=zeros(length(A));

%%
%Initialize model variables and perform simulation where no experimental
%data is given
y=0;
x=[0;0;0];
total_Y=[];

for i=data(4,:)
    y=C*(B*i+A*x);
    x=A*x+B*i;
    total_Y=[total_Y;y];
end

%%
%Initialize model variables and perform simulation where experimental data
%is given
y=0;
x=[0;0;0];
total_Y=0;
[x,yCorr,P]=kalmanFilter(0,A,B,C,Q,R,0,x,P);
for i=2:length(data(4,:))
    y=C*(B*data(4,i-1)+A*x);
    [x,yCorr,P]=kalmanFilter(data(4,i-1),A,B,C,Q,R,data(2,i)-data(2,1),x,P);
    total_Y=[total_Y;y];
end

%%
%Given the hidden states from the experiment, compute where the system thinks
%it will go to on the next time step, after the optimized LED input has been
%computed.
total_Y=0;
for i=2:length(data(4,:))
    y=C*(B*data(4,i)+A*data(5,i));
    total_Y=[total_Y;y];
end
%%
%Initialize model variables and perform simulation given an initial
%condition and a light input sequence
clf
hold all

reference=[0.,0.,0.,0.03,0.06,0.09,0.12,0.15,0.18,0.21,0.24,0.27,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.27,0.24,0.21,0.18,0.15,0.12,0.09,0.06,0.03,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.];
future_steps=5;

for j=1:length(MPCupdown12082014(1,:))-future_steps
    total_Y=[];
    x=MPCupdown12082014(7:9,j);
    Ig=lsqnonlin(@(input) MPCmultipleSS(input,x,reference(j:j+future_steps-1)',future_steps),zeros(future_steps,1),zeros(future_steps,1),ones(future_steps,1));
    for i=1:future_steps
        y=C*(B*Ig(i)+A*x);
        x=A*x+B*Ig(i);
        total_Y=[total_Y;y];
    end
    plot(MPCupdown12082014(1,j:length(total_Y)+j-1),total_Y+MPCupdown12082014(2,1))
    pause()
end
plot(MPCupdown12082014(1,:),MPCupdown12082014(2,:),'-s','LineWidth',2)
pause()
plot(MPCupdown12082014(1,:),MPCupdown12082014(3,:)+MPCupdown12082014(2,1),'--','LineWidth',2)
hold off
%%
%Plot data
clf
plot(data(1,:),[data([2,3],:);total_Y'+data(2,1)],'-s')

%%
plot(MPCupdown12082014(1,:),MPCupdown12082014(2,:),'-s','LineWidth',2)
plot(MPCupdown12082014(1,:),MPCupdown12082014(3,:)+MPCupdown12082014(2,1),'--','LineWidth',2)



