% To use, simply run and select the first image in the stack of images you
% want to squish.  

[fileName,pathName] = uigetfile('*.tif');                  % Get .tif files
dname = fullfile(pathName,fileName);                       % Find full path name of selected file
filelist = dir([fileparts(dname) filesep '*.tif']);        % Create struct of file data
fileNames = fullfile(pathName,{filelist.name}');           % Get full path of all files (in case we're not in the source directory)
num_frames = (numel(filelist));                            % Number of elements in list
frameHolder = cell(num_frames, 1);
for frame = 1:num_frames
    full_name = fullfile(pathName, fileNames{frame});   
    frameHolder{frame}=imread(fileNames{frame});           % Load each image into a cell
end
figure('Name','Image vs Native Matlab Edge Detection')
I = imread((fileNames{200})); %to show the first image in the selected folder
e = edge(I, 'Canny',0);
subplot(1,2,2)
imshow(e);                                                 % Show matlab edge detection
subplot(1,2,1)
imshow(I, []);                                             % Show original image

differentialArray = zeros(size(frameHolder{1}),'uint16');
figure('Name','Differential Matrix Squishing')
subplot(2,2,1)
I = imread((fileNames{250}));                              % Read the 250th image (arbitrary)
imshow(I,[]);
for k = 100:length(frameHolder)                            % Look through images starting at the 100th (drop early data)
    if k == 100
        old = frameHolder{k};
    else
        new = frameHolder{k};                              % Take derivative
        difference = new - old;
        differentialArray = differentialArray + difference;
    end    
end

subplot(2,2,2)
imshow(differentialArray);                                 % Show untouched heatmap of activity

subplot(2,2,3)
brightest = max(differentialArray);                        % Find highest intensity pixel

differentialArray(differentialArray<brightest-250)=0;      % Normalize based on highest intensity
imshow(differentialArray);

[a,b] = size(differentialArray);
step = 5;
factor = .7;                                              % Allow 70% lenience in group intensity
% Loop for searching matrix and removing areas of size step^2 with
% intensity less than the brightest pixel multiplied by factor
for i=1:step:a
    for j=1:step:b
        section = differentialArray(i:i+step-1,j:j+step-1);
        score = mean(mean(section));
        if score<brightest*factor
            differentialArray(i:i+step-1,j:j+step-1)=differentialArray(i:i+step-1,j:j+step-1)*0;
        end
    end
end
subplot(2,2,4)
e = edge(differentialArray, 'Canny',0);                    % Retry Canny edge detection algorithm 
imshow(e);