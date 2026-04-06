%% Time-Frequency Analaysis for t-maze experiments

clc
clear
close all

pathdata = 'file_directory/export/';
pathout='file_directory/tf/';
mkdir(pathout);

SRate = 1000;    % Sampling Rate 1000
Freq = 1:60;  % Frequency range for the analysis

conlist={'_reward1', '_reward2', '_reward3', '_reward4', '_reward5', ...
         '_noreward1', '_noreward2', '_noreward3', '_noreward4', '_noreward5'};

chanList=textread('file_directory/channel_names_cl.txt','%s');
chanNum=28;
TIME=5001;

subs = []

for s = 1:length(subs)

    sub = int2str(subs(s));
    
    for ai=1:numel(conlist)
    
        conName=conlist{ai};
        conName=['sub' sub '_' conName];
        files=dir(strcat(pathdata,conName,'.mat'));


        for ci=1:chanNum
              
      		chanVariable=chanList{ci}; % change channel names when switching between EEG and MEG
      		POW_subj=zeros(1,60,TIME); %subject, frequency, data points
      		POW_BASE_subj = zeros(1,60,TIME);
      	  
      		disp(strcat('Start processing for Channel:',chanVariable));
            
          Name = files(fi).name;
          tmp=load ([pathdata, files(fi).name])
          chanData=tmp.epochs;
          
          fName = files(1).name;
          tmp=load ([pathdata, files(fi).name]);
          chanData=tmp.epochs;
          chanVariable=chanListeeg64{ci};
          tmpchan=reshape(chanData(ci,:,:),[TIME,size(chanData,3)])';
          POW = zeros(60,TIME);% freq, data points
          
          for k=1:size(tmpchan,1)
            COEFS = cwt (tmpchan(k,:),SRate*1.5./Freq,'cmor1-1.5');
            POW = POW + abs (COEFS(:,1:TIME)).^2; 
          end

          POW_subj(1,:,:)=POW;          
          
          BASE=squeeze(mean(POW_subj(1,:,2300:2400),3));
          BASE=repmat(BASE',1,TIME);
          POW_BASE_subj(1,:,:)=(squeeze(POW_subj(1,:,:))-BASE)./BASE;  

          save([pathout 'POWtotal_', conName, '_',chanVariable,'.mat'], 'POW_BASE_subj');
          POWtot = POW_BASE_subj;

          %%%%induced 
      		disp(strcat('Start induced for Channel:',chanVariable));
      		POW_subj=zeros(1,60,TIME); % subject, frequency, data points
      		POW_BASE_subj = zeros(1,60,TIME);

          fName = files(1).name;
          tmp=load ([pathdata, files(1).name]);
          chanData=tmp.epochs;
          tmpchan=reshape(chanData(ci,:,:),[TIME,size(chanData,3)])';
        
          theMean = mean(tmpchan, 1);
          POW = zeros(60,TIME); % freq, data points-same as above
          
          for k = 1:size(tmpchan,1)
              inducedC3(k,:) = tmpchan(k,:) - theMean; 
              COEFS = cwt(inducedC3(k,:), SRate*1.5./Freq, 'cmor1-1.5');
              POW = POW + abs(COEFS(:,1:TIME)).^2; 
          end

          POW_subj(1,:,:)=POW;
        
          BASE=squeeze(mean(POW_subj(1,:,2300:2400),3));
          BASE=repmat(BASE',1,TIME);
          POW_BASE_subj(1,:,:)=(squeeze(POW_subj(1,:,:))-BASE)./BASE;
        
          disp(strcat('done for suject',fName));

		      save([pathout 'POWinduced_', conName, '_',chanVariable,'.mat'], 'POW_BASE_subj');

      		POWind = POW_BASE_subj;
      		POW_evoked = POWtot-POWind;
      		
      		save([pathout 'POWevoked_', conName, '_',chanVariable,'.mat'], 'POW_evoked');

        end  %%%for each channel

    end %%for each list
    
end  %%for each subject
