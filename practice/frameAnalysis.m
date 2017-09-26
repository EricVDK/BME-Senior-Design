differentialArray = zeros(size(frameHolder{1}),'uint16');
for k = 100:length(frameHolder)
    if k == 1
        old = frameHolder{k};
    else
        new = frameHolder{k};
        difference = new - old;
        differentialArray = differentialArray + difference;
    end    
end

subplot(2,2,1)
imshow(differentialArray);

subplot(2,2,2)
brightest = max(differentialArray);

differentialArray(differentialArray<brightest-250)=0;
imshow(differentialArray);
[a,b] = size(differentialArray);
step = 5;
factor = 1.3;
for i=1:step:a
    for j=1:step:b
        section = differentialArray(i:i+step-1,j:j+step-1);
        score = mean(mean(section));
        if score<brightest/factor
            differentialArray(i:i+step-1,j:j+step-1)=differentialArray(i:i+step-1,j:j+step-1)*0;
        end
    end
end
subplot(2,2,[3,4])
imshow(differentialArray);