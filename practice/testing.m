[fileName,pathName] = uigetfile('*.tif');
dname = fullfile(pathName,fileName);
filelist = dir([fileparts(dname) filesep '*.tif']);
fileNames = {filelist.name}';
num_frames = (numel(filelist));
frameHolder = cell(num_frames, 1);
for frame = 1:num_frames
    frameHolder{frame}=imread(fileNames{frame});
end

I = imread((fileNames{200})); %to show the first image in the selected folder
e = edge(I, 'Prewitt',0);
subplot(1,2,1)
imshow(e);
subplot(1,2,2)
imshow(I, []);