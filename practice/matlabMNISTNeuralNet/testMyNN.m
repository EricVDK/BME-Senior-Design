
test = double(rgb2gray(imread('myNum0.jpg')))';
disp(test)
test = test(:);

disp(test)
myNeuralNetworkFunction(test)