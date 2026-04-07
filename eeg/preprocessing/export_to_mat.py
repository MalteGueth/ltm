import mne
import scipy.io as sio
import numpy as np

path = file_directory

# Create subjects list
subs = []

# Loop over subjects example for encoding stage (reward cues vs. no reward cues)
for sub in subs:

    epochs = mne.read_epochs(path + epochs/encoding/sub' + sub + '_tf-epo.fif', preload=True).drop_channels(['F7', 'F8'], on_missing="ignore")
    
    # Select the different conditions
    rew1 = epochs['reward_p1'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    rew1 = rew1.reshape((int(rew1.shape[0]/5001)), 5001, 28)
    rew2 = epochs['reward_p2'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    rew2 = rew2.reshape((int(rew2.shape[0]/5001)), 5001, 28)
    rew3 = epochs['reward_p3'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    rew3 = rew3.reshape((int(rew3.shape[0]/5001)), 5001, 28)
    rew4 = epochs['reward_p4'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    rew4 = rew4.reshape((int(rew4.shape[0]/5001)), 5001, 28)
    rew5 = epochs['reward_p5'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    rew5 = rew5.reshape((int(rew5.shape[0]/5001)), 5001, 28)
    norew1 = epochs['noreward_p1'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    norew1 = norew1.reshape((int(norew1.shape[0]/5001)), 5001, 28)
    norew2 = epochs['noreward_p2'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    norew2 = norew2.reshape((int(norew2.shape[0]/5001)), 5001, 28)
    norew3 = epochs['noreward_p3'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    norew3 = norew3.reshape((int(norew3.shape[0]/5001)), 5001, 28)
    norew4 = epochs['noreward_p4'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    norew4 = norew4.reshape((int(norew4.shape[0]/5001)), 5001, 28)
    norew5 = epochs['noreward_p5'].copy().drop_channels('V').to_data_frame().drop(['time', 'condition', 'epoch'], axis=1).to_numpy()
    norew5 = norew5.reshape((int(norew5.shape[0]/5001)), 5001, 28)

    # Save the data array as a mat file and re-arrange the dimensions, so that it is channels by samples by trials
    sio.savemat(path + 'export/sub' + sub + '_reward1.mat',
                mdict={'epochs': np.moveaxis(rew1, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_reward2.mat',
                mdict={'epochs': np.moveaxis(rew2, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_reward3.mat',
                mdict={'epochs': np.moveaxis(rew3, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_reward4.mat',
                mdict={'epochs': np.moveaxis(rew4, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_reward5.mat',
                mdict={'epochs': np.moveaxis(rew5, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_noreward1.mat',
                mdict={'epochs': np.moveaxis(norew1, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_noreward2.mat',
                mdict={'epochs': np.moveaxis(norew2, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_noreward3.mat',
                mdict={'epochs': np.moveaxis(norew3, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_noreward4.mat',
                mdict={'epochs': np.moveaxis(norew4, [0, 1, 2], [-1, 1, 0])},)
    sio.savemat(path + 'export/sub' + sub + '_noreward5.mat',
