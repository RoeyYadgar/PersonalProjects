%%
com_str = read_text('commands.txt');
com_time = zeros(length(com_str)-1,1);

for i = 1:length(com_time)
    slt = split(com_str(i),'-');
    time = datetime(slt(1),'InputFormat','MM/dd/uu HH:mm:ss');
    time.Year = time.Year+2000;
    com_time(i) = posixtime(time);
    com_str(i) = slt(2);
    com(i) = jsondecode(char(com_str(i)));
end

tmp_str = read_text('temperature.txt');
tmp = zeros(length(tmp_str)-1,1);
tmp_time = zeros(length(tmp_str)-1,1);

for i = 1:length(tmp)
    slt = split(tmp_str(i),'-');
    time = datetime(slt(1),'InputFormat','MM/dd/uu HH:mm:ss');
    time.Year = time.Year+2000;
    tmp_time(i) = posixtime(time);
    tmp(i) = str2double(slt(2));
end

%%
hold on
plot(tmp_time,tmp);
for i = 1:length(com)
    text(com_time(i),26,com(i).State);
end
hold off


%%

function str = read_text(path)
    fid = fopen(path);
    str = string(char(fread(fid,'char'))');
    fclose(fid);
    str = split(str,newline);
end