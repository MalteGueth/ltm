import mne
import numpy as np

# From the script create_events.py several segmentations can be made depending on the analysis goal
# The following event_id dictionaries and loops serve to segment for the analysis of:
# 1) the full trial period from the starting location to the end of the encoding stage
# 2) reward vs. no reward cues during encoding
# 3) target vs. distractor pillars during recall

subs = []

# Just the starting location
event_id = {'move_to_p1': 1}

reject = dict(eeg=150e-6) # 100 microV

for sub in subs:

    # Load the cleaned raw data
    raw = mne.io.read_raw('file_directory/raw/sub' + sub + '-raw.fif', preload=True)

    # Load the re-coded events
    events = mne.read_events('file_directory/events/events' + sub + '-recoded-eve.fif')

    # Set the channel types for the EOG
    raw.set_channel_types({'V': 'eog', 'F9': 'eeg', 'F10': 'eeg'})

    # Segment the data for the full trial
    epochs = mne.Epochs(raw, events, event_id, tmin=-1, tmax=7, baseline=None, preload=True,
                        on_missing='ignore').drop_channels(['V'])

    # Remove epochs exceeding threshold
    epochs = epochs.drop_bad(reject=reject)

    epochs.save('file_directory/epochs/go/sub' + sub + '-epo.fif', overwrite=True)

event_id = {'recall_p1': 91, 'recall_p2': 92, 'recall_p3': 93, 'recall_p4': 94, 'recall_p5': 95, 
            'recall_p6': 96, 'recall_p7': 97, 'recall_p8': 98, 'recall_p9': 99, 'recall_p10': 100,
            'correct_recall_p1': 211, 'miss_recall_p1': 212, 'correct_recall_p2': 221, 'miss_recall_p2': 222,
            'correct_recall_p3': 231, 'miss_recall_p3': 232, 'correct_recall_p4': 241, 'miss_recall_p4': 242,
            'correct_recall_p5': 251, 'miss_recall_p5': 252}

########################
# Reward vs. no reward cues during encoding stage
event_id = {'reward_p1': 11, 'reward_p2': 22,  'reward_p3': 33, 'reward_p4': 44, 'reward_p5': 55,
            'noreward_p1': 1111, 'noreward_p2': 2222, 'noreward_p3': 3333, 'noreward_p4': 4444, 'noreward_p5': 5555}

reject = dict(eeg=150e-6) # 100 microV

for sub in subs:

    raw = mne.io.read_raw('file_directory/raw/sub' + sub + '-raw.fif', preload=True)
    events = mne.read_events('file_directory/events/events' + sub + '-recoded-eve.fif')
    raw.set_channel_types({'V': 'eog', 'F9': 'eeg', 'F10': 'eeg'})

    # Merge events together for the no reward cues
    events = mne.merge_events(events, [12, 13, 14, 15], 1111, replace_events=True)
    events = mne.merge_events(events, [21, 23, 24, 25], 2222, replace_events=True)
    events = mne.merge_events(events, [31, 32, 34, 35], 3333, replace_events=True)
    events = mne.merge_events(events, [41, 42, 43, 45], 4444, replace_events=True)
    events = mne.merge_events(events, [51, 52, 53, 54], 5555, replace_events=True)

    epochs = mne.Epochs(raw, events, event_id, tmin=-2.5, tmax=2.5, baseline=None, preload=True,
                        on_missing='ignore')

    epochs = epochs.drop_bad(reject=reject)

    epochs.save('file_directory/epochs/gencodingo/sub' + sub + '-epo.fif', overwrite=True)

########################
# Target vs. distractor pillars during recall stage

event_id = {'target_p1': 401, 'target_p2': 402, 'target_p3': 403, 'target_p4': 404, 'target_p5': 405,
            'distractor_p1': 411, 'distractor_p2': 412, 'distractor_p3': 413, 'distractor_p4': 414, 'distractor_p5': 415}

for sub in subs:

    raw = mne.io.read_raw('file_directory/raw/sub' + sub + '-raw.fif', preload=True)
    raw.set_channel_types({'V': 'eog', 'F9': 'eeg', 'F10': 'eeg'})

    events = mne.read_events('file_directory/events/events' + sub + '-recall-targetdist-eve.fif')
    epochs = mne.Epochs(raw, events, event_id, tmin=-2.5, tmax=2.5, baseline=None, preload=True,
                        on_missing='ignore')

    epochs = epochs.drop_bad(reject=reject)

    epochs.save('file_directory/epochs/recall/sub' + sub + '_tf-epo.fif', overwrite=True)
