function [x,y,P] = kalmanFilter(u,A,B,C,Q,R,y0,x0,P0)
%State estimation using a Kalman filter

xm=(A*x0+B*u);
Pm=(A*P0*A'+Q);
ym=y0-C*xm;
L=Pm*C'/(C*Pm*C'+R);
x=xm+L*ym;
y=C*x;
P=(eye(length(x0))-L*C)*Pm;

end

