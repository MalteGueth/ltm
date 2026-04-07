# Data management
import os

# EEG
import mne
from mne.preprocessing import ICA

# Set the directory and file name
path = 'file_directory/'
raw_file = os.path.join(path, 'raw', 'filename.vhdr')

# Read the first file and create a montage with EOG channels as before
raw = mne.io.read_raw_brainvision(sample_data_eeg, preload=True)

# Load the digital montage file used for the EEG montage
montage = mne.channels.make_standard_montage(kind='standard_1005')
raw.set_montage(montage=montage, on_missing='ignore')

# For setting the EEG montage, first identify the eog channels which cannot be recognized from standard digital montage names
raw.set_channel_types({'LHEOG': 'eog', 'RHEOG': 'eog', 'VEOG': 'eog'})

# For an overview of the sensor maps, plot topographies for EEG
raw.plot_sensors(kind='topomap', show_names=True, title='28 channel EEG montage');

events, event_dict = mne.events_from_annotations(raw)
fig = mne.viz.plot_events(events)

# Build a temporary dictionary of event ids
event_id = {'move_to_p1': 1}

# Plot all events across time
fig = mne.viz.plot_events(events, raw.info['sfreq'],
                          event_id=event_id, first_samp=raw.first_samp)

# Save event array
mne.write_events(path + 'events/' + sub + '-eve.fif', events)

# Bandpass filter data between 0.1 Hz and 60 Hz
filter_raw = raw.filter(l_freq=.1, h_freq=60, fir_window='hamming', method='fir')

# Plot average across all events to check for faulty channels
raw2 = filter_raw.copy()
epochs = mne.Epochs(raw2, events=events, event_id=event_id).average().plot()

# Interpolate channels if necessary
filter_raw.info['bads'] = []
filter_raw = filter_raw.interpolate_bads(reset_bads=True)

# For the ocular and other artifacts, employ an ICA correction approach
# Set parameters for ICA
n_components = 25
method='infomax'

# Create ICA object
ica = ICA(n_components=n_components, method=method)

# Apply stricter high-pass filter at 1 Hz to copy of raw data to be fed into ICA
# to reduce influence of slow drifts and other high amplitude low frequency artifacts
ica.fit(filter_raw.copy().filter(l_freq=1, h_freq=60))

# Save ICA
ica.save(path + 'ica/sub' + sub + '-ica.fif', overwrite=True)

# Plot all ica components as topomaps and their respective time course contributions
ica.plot_components()
ica.plot_sources(filter_raw, start=100);
# To be sure, we can look at exact properties of these components
ica.plot_properties(filter_raw, picks=[])

# Select components to be excluded from back-projection to continuous data
bads = []
ica.exclude = bads

# Validate artifact component selection by running automatic ICA eog component identification
eog_indices, eog_scores = ica.find_bads_eog(raw)
ica.exclude = eog_indices

# Plot the component artifact scores along with component properties and averaged raw data around EOG events with the best matching component excluded
ica.plot_scores(eog_scores);
ica.plot_properties(raw, picks=eog_indices);
ica.plot_sources(raw, start=100);
ica.plot_sources(eog_epochs.average());

# Back-project to continous data without artifact components
reconst_raw = filter_raw.copy()
ica.apply(reconst_raw)

# The same procedure can be applied using an automatic detection ICA-approach
# Build an empty list for component indices to be excluded
ica.exclude = []

# Rereference to the average of all channels
reconst_raw.set_eeg_reference(ref_channels='average')

# Epoch cleaned data around the start of the track (-0.4 seconds before and 6 seconds after) for time frequency analysis
# These segments are only for testing how well the cleaning worked and will not be saved
epochs = mne.Epochs(reconst_raw, events, event_id, tmin=-.4, tmax=6, baseline=None, preload=True, on_missing='ignore')

# Reject artifact epochs by first setting ampltiude criteria
reject = dict(eeg=100e-6) # 100 microV
# Drop epochs exceeding amplitude threshold
epochs = epochs.drop_bad(reject=reject)
# If needed show distribution of dropped segments across channels 
epochs.plot_drop_log()

# Save data
reconst_raw.save(path + 'raw/sub' + sub + '-raw.fif', overwrite=True)
