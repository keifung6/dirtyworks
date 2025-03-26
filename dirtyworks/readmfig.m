h1= openfig(".fig",'reuse'); % adress of the figure


axesHandles = findall(h1, 'Type', 'axes');

% initialize data each axes
data = struct('x', [], 'y', [], 'z', []);

% looping subplots
for i = 1:length(axesHandles)
    axesHandle = axesHandles(i); 
    D = get(axesHandle, 'Children'); 
    
    for j = 1:length(D)
        XData = get(D(j), 'XData');
        YData = get(D(j), 'YData'); 
        

        if i == 1
            data.x = XData(:); 
            data.y = [data.y, YData(:)];
     
        elseif i == 2
            data.z = [data.z, YData(:)];
    end
end


result = [data.x, data.y, data.z];


disp(result);





