function [ error ] = MPCmultipleSS(input,hiddenStates,reference,timeSteps)
    %SS Model extracted from experimental data
A=  [ 0.6231   -0.2403   -0.0710
    0.2515    0.9597   -0.0120
    0.0106    0.0770    0.9997];
B=[ 0.5029
    0.0847
    0.0023];
C=[0         0    0.1531];

    predictedFluorescence=zeros(timeSteps,1);%vector containing the GFP measurements predicted by the model

    weights=ones(timeSteps,1);%weights assigned to each data point for the optimization

    for iter=1:timeSteps
        predictedFluorescence(iter)=C*(B*input(iter)+A*hiddenStates);%model prediction
        hiddenStates=B*input(iter)+A*hiddenStates;%hidden states from the State-Space model
    end
    error=abs(weights.*(predictedFluorescence-reference));%vector containing the expected errors

end