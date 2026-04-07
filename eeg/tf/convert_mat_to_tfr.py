import os
from scipy.io import loadmat
import numpy as np

import mne
from mne.time_frequency import tfr_morlet

# Import the mat files from time-frequency analysis to Python
# And convert into MNE-python tfr object

# Set montage file
montage = mne.channels.make_standard_montage(kind='standard_1005')

# Set some lists and variables for the loop
conditions = ['reward1', 'reward2', 'reward3', 'reward4', 'reward5',
              'noreward1', 'noreward2', 'noreward3', 'noreward4', 'noreward5']
pType = ['evoked', 'total', 'induced']
subs = []
path = 'file_directory'

samples = 5001
chNr = 28
sfreq = 1000
subNr = len(subs)

# Create dummy of tf object
rdata = np.random.randn(subNr, chNr, samples)

epochs=mne.read_epochs(path + 'epochs/sub01_tf64-epo.fif')
info=epochs.pick_types(meg=False, eeg=True, ref_meg=False).info

# Create events for dummy epochs
events = np.array([np.arange(0, len(subs), 1), np.repeat(1, len(subs)), np.repeat(1, len(subs))]).T

event_id = dict(subjects=1)

# Trials were cut from -2.5 to 2.5 seconds
tmin = -2.5
tmax = 2.5
custom_epochs = mne.EpochsArray(rdata, info=info, events=events, tmin=tmin, event_id=event_id)

# Transform the dummy epochs to a tfr object
decim = 1
freqs = np.arange(1, 51, 1)
n_cycles = 0.5

tfr_epochs = tfr_morlet(custom_epochs, freqs,
                        n_cycles=n_cycles, decim=decim,
                        return_itc=False, average=False)

tfr_ave = tfr_epochs.average()

my_array=np.zeros(shape=(chNr, 50, samples))
ch_names = info['ch_names']

s = 0
c = 0
my_subs_array=np.zeros(shape=(subNr, chNr, 50, samples))

# Load every time frequency result exported from matlab and transform it into an mne tfr object
for condName in conditions:

    for powtype in pType:

        s = 0
        if powtype == 'evoked':
            key = 'POW_evoked'
        else:
            key = 'POW_BASE_subj'

        for sub in subs:

            c = 0

            for cl in ch_names:

                file = path + 'POW' + powtype + '_' + 'sub' + sub + '_' + condName + '_' + cl + '.mat'
                data = np.squeeze(loadmat(file)[key])[0:50,:]

                my_array[c, :, :] = data
                c = c + 1

            tfr_ave.data = my_array
            tfr_ave.save(path + 'tf/sub' + sub + '_' + condName + '_' + powtype + '-tfr.h5', overwrite=True)

            my_subs_array[s, :, :, :] = my_array
            my_array = np.zeros(shape=(chNr, 50, samples))

            s = s + 1

        tfr_ave.data = np.mean(my_subs_array, axis=0)
        tfr_ave.save(path + 'tf/' + condName + '_' + powtype + '-tfr.h5', overwrite=True)
