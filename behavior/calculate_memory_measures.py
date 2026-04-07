import pandas as pd
import numpy as np

from scipy.stats import norm
import math
import re

import mne

path = 'file_directory'
# In addition to the root directory, specify the location of the experiment images
imagePath = path + 'experiment/images/'

# Set the column names for each iteration of the loop below
cols = ['response1', 'response2', 'response3', 'response4', 'response5', 'response6', 'response7', 'response8',
        'response9', 'response10',
        'pillar1', 'pillar2', 'pillar3', 'pillar4', 'pillar5', 'recall_pillar1',
        'recall_pillar2', 'recall_pillar3', 'recall_pillar4', 'recall_pillar5', 'recall_pillar6', 'recall_pillar7',
        'recall_pillar8', 'recall_pillar9', 'recall_pillar10',
        'rt_pillar1', 'rt_pillar2', 'rt_pillar3', 'rt_pillar4', 'rt_pillar5', 'rt_pillar6', 'rt_pillar7', 'rt_pillar8',
        'rt_pillar9', 'rt_pillar10']
slide = ['slide8', 'slide18', 'slide28', 'slide38', 'slide48']
# Create a dictionary to simplify pillar labels for general pillar identities
key = {'pillar1': 'p1', 'pillar2': 'p2', 'pillar3': 'p5', 'pillar4': 'p4', 'pillar5': 'p3'}
# Create a dictionary to write the reward cue pillar labels
encodingKey = {'pillar1': '_reward1', 'pillar2': '_reward2', 'pillar3': '_reward3', 'pillar4': '_reward4',
               'pillar5': '_reward5'}
# Create a dictionary to write the correct response labels
hitKey = {'pillar1': '_correct_recall1', 'pillar2': '_correct_recall2', 'pillar3': '_correct_recall3',
          'pillar4': '_correct_recall4', 'pillar5': '_correct_recall5'}
# Create a dictionary to write the miss labels
missKey = {'pillar1': '_miss1', 'pillar2': '_miss2', 'pillar3': '_miss3', 'pillar4': '_miss4', 'pillar5': '_miss5'}
# Create a list of strings with the pillar labels
pictures = ['p' + str(item) for item in np.arange(1, 11)]
# Prepare the data frame and add the column names for the columns to be added
allSub = pd.DataFrame(np.zeros((0, 53)))
allSub.columns = cols + ['trial', 'correctPillar', 'rt_correctPillar', 'rt_incorrectPillars',
                         'hits', 'misses', 'fas', 'crs',
                         'd_pillar', 'beta_pillar', 'c_pillar', 'Ad_pillar', 'tpr_pillar', 'fpr_pillar',
                         'tpr_all', 'fpr_all', 'd_all', 'subject']
  
subs = []

Z = norm.ppf

def SDT(hits, misses, fas, crs):
    """ Creates a dict of d' measures using hits, misses, false alarms, and correct rejections"""
    # Floors and ceilings are replaced by half hits and half FA's
    half_hit = 0.5 / (hits + misses)
    half_fa = 0.5 / (fas + crs)

    # Calculate hit_rate and avoid d' infinity
    hit_rate = hits / (hits + misses)
    if hit_rate == 1:
        hit_rate = 1 - half_hit
    if hit_rate == 0:
        hit_rate = half_hit

    # Calculate false alarm rate and avoid d' infinity
    fa_rate = fas / (fas + crs)
    if fa_rate == 1:
        fa_rate = 1 - half_fa
    if fa_rate == 0:
        fa_rate = half_fa

    # Return d', beta, c and Ad'
    out = {}
    out['d'] = Z(hit_rate) - Z(fa_rate)
    out['beta'] = math.exp((Z(fa_rate) ** 2 - Z(hit_rate) ** 2) / 2)
    out['c'] = -(Z(hit_rate) + Z(fa_rate)) / 2
    out['Ad'] = norm.cdf(out['d'] / math.sqrt(2))

    return (out)

for sub in subs:
  ` 
    # Load pre-formatted and filtered e-prime text files
    events = pd.read_csv(path + 'sub' + sub + '_rt.txt', sep="\t", skiprows=0)
    # Assign column names
    events.columns = cols
    # Add a trial counter column
    events['trial'] = np.arange(1,len(events)+1)

    # There are 10 unique columns (5 encoding, 5 distractors during recall)
    for p in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
        # Check all lines and set RT for invalid cases to nan (RT > 2500 ms or < 100 ms
        for line in np.arange(0, len(events)):
            if events.loc[line, 'rt_pillar' + p] >= 2500 or events.loc[line, 'rt_pillar' + p] < 100:
                events.loc[line, 'rt_pillar' + p] = np.nan

    # Set a list of column names for the pillars
    strCols = ['pillar1', 'pillar2', 'pillar3', 'pillar4', 'pillar5']
    # Initiate a column counter and a loop
    colCounter = 0
    for col in strCols:
        # Map the reward and no reward label onto the image names from the e-prime file
        # and write the labels into the each column to extract which column was the reward
        # cue pillar on a given trial
        events[col] = events[col].map({imagePath + 'reward' + str(colCounter + 1) + '.bmp': 'reward',
                                       imagePath + slide[colCounter] + '.bmp': 'noreward'})
        colCounter = colCounter + 1

    # Do the same for the recall pillars
    strCols = ['recall_pillar1', 'recall_pillar2', 'recall_pillar3', 'recall_pillar4', 'recall_pillar5',
               'recall_pillar6', 'recall_pillar7', 'recall_pillar8', 'recall_pillar9', 'recall_pillar10']
    colCounter = 0
    for col in strCols:
        events[col] = events[col].map({imagePath + pictures[0] + '.BMP': pictures[0],
                                       imagePath + pictures[1] + '.BMP': pictures[1],
                                       imagePath + pictures[2] + '.BMP': pictures[2],
                                       imagePath + pictures[3] + '.BMP': pictures[3],
                                       imagePath + pictures[4] + '.BMP': pictures[4],
                                       imagePath + pictures[5] + '.BMP': pictures[5],
                                       imagePath + pictures[6] + '.BMP': pictures[6],
                                       imagePath + pictures[7] + '.BMP': pictures[7],
                                       imagePath + pictures[8] + '.BMP': pictures[8],
                                       imagePath + pictures[9] + '.BMP': pictures[9]
                                       })

    # From the e-prime data, extract the indices of the reward cue pillars
    events['correctPillar'] = events.loc[:,'pillar1':'pillar5'].isin(['reward']).idxmax(1)

    # Add new behavioral results columns
    events['rt_correctPillar'] = 0
    events['rt_incorrectPillars'] = 0
    events['hits'] = 0
    events['misses'] = 0
    events['fas'] = 0
    events['crs'] = 0
    events['d_pillar'] = 0
    events['beta_pillar'] = 0
    events['c_pillar'] = 0
    events['Ad_pillar'] = 0
    events['tpr_pillar'] = 0
    events['fpr_pillar'] = 0
    events['d_block'] = 0
    events['beta_block'] = 0
    events['c_block'] = 0
    events['Ad_block'] = 0
    events['tpr_block'] = 0
    events['fpr_block'] = 0
    events['tpr_all'] = 0
    events['fpr_all'] = 0
    events['block'] = 0
  
    # Go through each trial in the e-prime data
    for line in np.arange(0, len(events)):

        # Extract the correct pillar, correpsonding image file for the recall stage, 
        # the corresponding column in the data frame, and all incorrect pillar columns
        correctPillar = key[events['correctPillar'][line]]
        correctRecallImage = events.loc[:, 'recall_pillar1':'recall_pillar10'].isin([correctPillar]).idxmax(1)[line]
        correctRecallCol = 'response' + ''.join(c for c in correctRecallImage if c.isdigit())
        incorrectRecallCols = ['response1', 'response2', 'response3', 'response4', 'response5', 'response6',
                               'response7', 'response8', 'response9', 'response10']
        incorrectRecallCols.remove(correctRecallCol)

        # If the correct pillar was chosen, the corresponding line in hits to 1
        # It it wasn't, set the line in miss to 1
        if events.loc[line, correctRecallCol] == 1:
            events['hits'][line] = 1
        elif events.loc[line, correctRecallCol] == 2:
            events['misses'][line] = 1

        # False alarms is defined as the sum of hits for incorrect pillars
        events['fas'][line] = np.sum(events.loc[line, incorrectRecallCols] == 1)
        # Correct rejections is defined as the sum of not chosen incorrect pillars
        events['crs'][line] = np.sum(events.loc[line, incorrectRecallCols] == 2)

        # Pick the column name for the reaction time for the correct pillar
        correctRTCol = 'rt_pillar' + ''.join(c for c in correctRecallImage if c.isdigit())
        # Add the reaction time of the current correct pillar
        events['rt_correctPillar'][line] = events[correctRTCol][line]
        # Do the same for the average of the incorrect pillars
        incorrectRTCols = ['rt_pillar1', 'rt_pillar2', 'rt_pillar3', 'rt_pillar4', 'rt_pillar5', 'rt_pillar6',
                           'rt_pillar7', 'rt_pillar8', 'rt_pillar9', 'rt_pillar10']
        incorrectRTCols.remove(correctRTCol)
        events['rt_incorrectPillars'][line] = np.mean(events.loc[line, incorrectRTCols])

    # Use the above SDT function to calculate the signal detection theory measures for each possible target pillar
    for pillar in np.unique(events['correctPillar']):

        # Extract trials where the current pillar had the reward cue
        dprimeEvents = events[(events['correctPillar'] == pillar)]
        # Calculate the SDT measures with the sum of hits, misses, false alarms, and correct rejections
        dprime = SDT(np.sum(dprimeEvents['hits']), np.sum(dprimeEvents['misses']),
                     np.sum(dprimeEvents['fas']), np.sum(dprimeEvents['crs']))

        # Calculate the true positive rate
        tpr = np.sum(dprimeEvents['hits']) / (np.sum(dprimeEvents['hits']) + np.sum(dprimeEvents['misses']))
        # Calculate the false positive rate
        fpr = np.sum(dprimeEvents['fas']) / (np.sum(dprimeEvents['fas']) + np.sum(dprimeEvents['crs']))

        # Assign all the measures to their respective trials (the same value will be set for all trials with a given reward pillar identity)
        events.loc[events['correctPillar'] == pillar, 'd_pillar'] = dprime['d']
        events.loc[events['correctPillar'] == pillar, 'beta_pillar'] = dprime['beta']
        events.loc[events['correctPillar'] == pillar, 'c_pillar'] = dprime['c']
        events.loc[events['correctPillar'] == pillar, 'Ad_pillar'] = dprime['Ad']
        events.loc[events['correctPillar'] == pillar, 'tpr_pillar'] = tpr
        events.loc[events['correctPillar'] == pillar, 'fpr_pillar'] = fpr

    # Finally, calculate all the SDT measures regardless of reward cue location across the whole task
    events['d_all'] = SDT(np.sum(events['hits']), np.sum(events['misses']),
                          np.sum(events['fas']), np.sum(events['crs']))['d']
    events['tpr_all'] = np.sum(events['hits']) / (np.sum(events['hits']) + np.sum(events['misses']))
    events['fpr_all'] = np.sum(events['fas']) / (np.sum(events['fas']) + np.sum(events['crs']))

    # Set the current subject label
    events['subject'] = int(re.sub("[^0-9]", "", sub))
    # Concatenate the current data frame to the data frame for all subjects
    allSub = pd.concat([allSub, events], axis=0)

# Save the data frame to a csv file
allSub.to_csv(path + 'behavior/sdt_results.csv', index=False)
