import mne
import numpy as np

# To extract more complex conditional events (e.g., reward cue at specific pillar that wa slater correctly recalled)
# the event arrays need to be re-coded from the basic event codes written during the experiment.

# The logic for re-coding will be to build running variables that keep track of previous events within a trial.

# Build a list of strings for all used subjects
subs = []

path = 'file_directory'

# The task events in the eprime code do not directly reflect which events during the recall
# were the reward pillar during the previous encoding stage and whether those were correctly identified.
# This first loop is for accurate identification of reward and no reward cue locations
# during the encoding and recall stage.
for sub in subs:

    # Read event files
    events = mne.read_events(path + 'events/events' + sub + '-eve.fif')

    # Create empty running variables to be updated
    reward = 0
    listType = 0
    recallRew = 0

    # Loop over lines in exisiting event arrays
    for line in np.arange(1, len(events)):

        # First remove some code duplicates that would complicate the rest of the code
        # These are feedback codes that lack the code for the step before a feedback cue
        if events[line, 2] == 11 and events[line-1, 2] != 101:
            events[line, 2] = 999
        elif events[line, 2] == 22 and events[line - 1, 2] != 102:
            events[line, 2] = 999
        elif events[line, 2] == 33 and events[line - 1, 2] != 103:
            events[line, 2] = 999
        elif events[line, 2] == 44 and events[line - 1, 2] != 104:
            events[line, 2] = 999
        elif events[line, 2] == 55 and events[line - 1, 2] != 105:
            events[line, 2] = 999
        elif events[line, 2] == 12 and events[line - 1, 2] != 101:
            events[line, 2] = 999
        elif events[line, 2] == 13 and events[line - 1, 2] != 101:
            events[line, 2] = 999
        elif events[line, 2] == 14 and events[line - 1, 2] != 101:
            events[line, 2] = 999
        elif events[line, 2] == 15 and events[line - 1, 2] != 101:
            events[line, 2] = 999
        elif events[line, 2] == 21 and events[line - 1, 2] != 102:
            events[line, 2] = 999
        elif events[line, 2] == 23 and events[line - 1, 2] != 102:
            events[line, 2] = 999
        elif events[line, 2] == 24 and events[line - 1, 2] != 102:
            events[line, 2] = 999
        elif events[line, 2] == 25 and events[line - 1, 2] != 102:
            events[line, 2] = 999
        elif events[line, 2] == 31 and events[line - 1, 2] != 103:
            events[line, 2] = 999
        elif events[line, 2] == 32 and events[line - 1, 2] != 103:
            events[line, 2] = 999
        elif events[line, 2] == 34 and events[line - 1, 2] != 103:
            events[line, 2] = 999
        elif events[line, 2] == 35 and events[line - 1, 2] != 103:
            events[line, 2] = 999
        elif events[line, 2] == 41 and events[line - 1, 2] != 104:
            events[line, 2] = 999
        elif events[line, 2] == 42 and events[line - 1, 2] != 104:
            events[line, 2] = 999
        elif events[line, 2] == 43 and events[line - 1, 2] != 104:
            events[line, 2] = 999
        elif events[line, 2] == 45 and events[line - 1, 2] != 104:
            events[line, 2] = 999
        elif events[line, 2] == 51 and events[line - 1, 2] != 105:
            events[line, 2] = 999
        elif events[line, 2] == 52 and events[line - 1, 2] != 105:
            events[line, 2] = 999
        elif events[line, 2] == 53 and events[line - 1, 2] != 105:
            events[line, 2] = 999
        elif events[line, 2] == 54 and events[line - 1, 2] != 105:
            events[line, 2] = 999

        # Account for the pre-release in ms
        if events[line, 2] in [11, 22, 33, 44, 55, 12, 13, 14, 15, 21, 23, 24, 25, 31, 32, 34, 35, 41, 42, 43, 45, 51,
                               52, 53, 54]:
            events[line, 0] = events[line, 0] + 250

        # Set the reward running variable to the pillar with the reward cue on a given trial
        if events[line, 2] == 11:  # reward at first pillar
            reward = 1
        elif events[line, 2] == 22:  # reward at second pillar
            reward = 2
        elif events[line, 2] == 33:  # reward at third pillar
            reward = 3
        elif events[line, 2] == 44:  # reward at fourth pillar
            reward = 4
        elif events[line, 2] == 55:  # reward at fifth pillar
            reward = 5

        # Note the order of the pillar presentation during the recall stage on this trial
        # There were four fixed possible pseudorandom pillar orders for the recall
        if events[line, 2] == 81:  # first recall pillar order
            listType = 1
        elif events[line, 2] == 82:  # second recall pillar order
            listType = 2
        elif events[line, 2] == 83:  # third recall pillar order
            listType = 3
        elif events[line, 2] == 84:  # fourth recall pillar order
            listType = 4

        # Set the identity of the reward pillar based on the reward location and the list type
        if (listType == 1 and reward == 1 and events[line, 2] == 91) or \
                (listType == 2 and reward == 1 and events[line, 2] == 100) or \
                (listType == 3 and reward == 1 and events[line, 2] == 95) or \
                (listType == 4 and reward == 1 and events[line, 2] == 99):
            recallRew = 1
        elif (listType == 1 and reward == 2 and events[line, 2] == 92) or \
                (listType == 2 and reward == 2 and events[line, 2] == 92) or \
                (listType == 3 and reward == 2 and events[line, 2] == 94) or \
                (listType == 4 and reward == 2 and events[line, 2] == 97):
            recallRew = 2
        elif (listType == 1 and reward == 3 and events[line, 2] == 95) or \
                (listType == 2 and reward == 3 and events[line, 2] == 99) or \
                (listType == 3 and reward == 3 and events[line, 2] == 91) or \
                (listType == 4 and reward == 3 and events[line, 2] == 92):
            recallRew = 3
        elif (listType == 1 and reward == 4 and events[line, 2] == 94) or \
                (listType == 2 and reward == 4 and events[line, 2] == 97) or \
                (listType == 3 and reward == 4 and events[line, 2] == 92) or \
                (listType == 4 and reward == 4 and events[line, 2] == 94):
            recallRew = 4
        elif (listType == 1 and reward == 5 and events[line, 2] == 93) or \
                (listType == 2 and reward == 5 and events[line, 2] == 95) or \
                (listType == 3 and reward == 5 and events[line, 2] == 98) or \
                (listType == 4 and reward == 5 and events[line, 2] == 96):
            recallRew = 5

        # Finally, replace the exisiting code for pillar presentation
        # with one that reflects whether the correct pillar was identified
        if (recallRew == 1 and events[line, 2] == 151) or \
                (recallRew == 1 and events[line, 2] == 169) or \
                (recallRew == 1 and events[line, 2] == 159) or \
                (recallRew == 1 and events[line, 2] == 167):
            events[line-1, 2] = 211 # correct p1 
        elif (recallRew == 1 and events[line, 2] == 152) or \
                (recallRew == 1 and events[line, 2] == 170) or \
                (recallRew == 1 and events[line, 2] == 160) or \
                (recallRew == 1 and events[line, 2] == 168):
            events[line-1, 2] = 212 # miss p1
        elif (recallRew == 2 and events[line, 2] == 153) or \
                (recallRew == 2 and events[line, 2] == 153) or \
                (recallRew == 2 and events[line, 2] == 157) or \
                (recallRew == 2 and events[line, 2] == 163):
            events[line-1, 2] = 221 # correct p2
        elif (recallRew == 2 and events[line, 2] == 154) or \
                (recallRew == 2 and events[line, 2] == 154) or \
                (recallRew == 2 and events[line, 2] == 158) or \
                (recallRew == 2 and events[line, 2] == 164):
            events[line-1, 2] = 222 # miss p2
        elif (recallRew == 3 and events[line, 2] == 159) or \
                (recallRew == 3 and events[line, 2] == 167) or \
                (recallRew == 3 and events[line, 2] == 151) or \
                (recallRew == 3 and events[line, 2] == 153):
            events[line-1, 2] = 231 # correct p3
        elif (recallRew == 3 and events[line, 2] == 160) or \
                (recallRew == 3 and events[line, 2] == 168) or \
                (recallRew == 3 and events[line, 2] == 152) or \
                (recallRew == 3 and events[line, 2] == 154):
            events[line-1, 2] = 232 # miss p3
        elif (recallRew == 4 and events[line, 2] == 157) or \
                (recallRew == 4 and events[line, 2] == 163) or \
                (recallRew == 4 and events[line, 2] == 153) or \
                (recallRew == 4 and events[line, 2] == 157):
            events[line-1, 2] = 241 # correct p4
        elif (recallRew == 4 and events[line, 2] == 158) or \
                (recallRew == 4 and events[line, 2] == 164) or \
                (recallRew == 4 and events[line, 2] == 154) or \
                (recallRew == 4 and events[line, 2] == 158):
            events[line-1, 2] = 242 # miss p4
        elif (recallRew == 5 and events[line, 2] == 155) or \
                (recallRew == 5 and events[line, 2] == 159) or \
                (recallRew == 5 and events[line, 2] == 167) or \
                (recallRew == 5 and events[line, 2] == 161):
            events[line-1, 2] = 251 # correct p5
        elif (recallRew == 5 and events[line, 2] == 156) or \
                (recallRew == 5 and events[line, 2] == 160) or \
                (recallRew == 5 and events[line, 2] == 168) or \
                (recallRew == 5 and events[line, 2] == 162):
            events[line-1, 2] = 252 # miss p5

    # For sanity check, print the current trial number (should be 120 at the end) 
    trialnr = str(np.sum(events[events[:,2] == 1, 2]))
    print('Suject ' + sub + ', trials: ' + trialnr)

    # Save the new events
    mne.write_events(path + 'events/events' + sub + '-recoded-eve.fif',
                     events, overwrite=True)


# Next, this loop will take the re-coded data and change the encoding code identity
# to reflect whether this trial was a hit

subs = [str(x) for x in np.arange(1, 34)]
subs.remove('21')
subs.remove('27')

for sub in subs:

    events = mne.read_events(path + 'events/events' +
                             sub + '-recoded-eve.fif')

    for line in np.arange(0, len(events)):

        if 211 in events[line:line + 45, 2] and events[line, 2] == 11:
            events[line, 2] = 311 # correct recognition pillar 1
        elif 221 in events[line:line + 45, 2] and events[line, 2] == 22:
            events[line, 2] = 322 # correct recognition pillar 2
        elif 231 in events[line:line + 45, 2] and events[line, 2] == 33:
            events[line, 2] = 333 # correct recognition pillar 3
        elif 241 in events[line:line + 45, 2] and events[line, 2] == 44:
            events[line, 2] = 344 # correct recognition pillar 4
        elif 251 in events[line:line + 45, 2] and events[line, 2] == 55:
            events[line, 2] = 355 # correct recognition pillar 5

    mne.write_events(path + 'events/events' + sub +
                     '-encoding-hitmiss-eve.fif', events, overwrite=True)

# This loop uses the same approach as the first, but specifically separates
# pillars during the recall stage based on whether they were distractors
# or target pillars regardless of performance

subs = [str(x) for x in np.arange(1, 34)]
subs.remove('21')
subs.remove('27')

for sub in subs:

    events = mne.read_events(path + 'events/events' + sub + '-eve.fif')

    reward = 0
    listType = 0

    for line in np.arange(0, len(events)):

        if events[line, 2] == 11:  # reward at first pillar
            reward = 1
        elif events[line, 2] == 22:  # reward at second pillar
            reward = 2
        elif events[line, 2] == 33:  # reward at third pillar
            reward = 3
        elif events[line, 2] == 44:  # reward at fourth pillar
            reward = 4
        elif events[line, 2] == 55:  # reward at fifth pillar
            reward = 5

        if events[line, 2] == 81:  # first recall pillar order
            listType = 1
        elif events[line, 2] == 82:  # second recall pillar order
            listType = 2
        elif events[line, 2] == 83:  # third recall pillar order
            listType = 3
        elif events[line, 2] == 84:  # fourth recall pillar order
            listType = 4

        if (listType == 1 and reward == 1 and events[line, 2] == 91) or \
                (listType == 2 and reward == 1 and events[line, 2] == 100) or \
                (listType == 3 and reward == 1 and events[line, 2] == 95) or \
                (listType == 4 and reward == 1 and events[line, 2] == 99):
            events[line, 2] = 401 # target p1
        elif (listType == 1 and reward == 2 and events[line, 2] == 92) or \
                (listType == 2 and reward == 2 and events[line, 2] == 92) or \
                (listType == 3 and reward == 2 and events[line, 2] == 94) or \
                (listType == 4 and reward == 2 and events[line, 2] == 97):
            events[line, 2] = 402 # target p2
        elif (listType == 1 and reward == 3 and events[line, 2] == 95) or \
                (listType == 2 and reward == 3 and events[line, 2] == 99) or \
                (listType == 3 and reward == 3 and events[line, 2] == 91) or \
                (listType == 4 and reward == 3 and events[line, 2] == 92):
            events[line, 2] = 403 # target p3
        elif (listType == 1 and reward == 4 and events[line, 2] == 94) or \
                (listType == 2 and reward == 4 and events[line, 2] == 97) or \
                (listType == 3 and reward == 4 and events[line, 2] == 92) or \
                (listType == 4 and reward == 4 and events[line, 2] == 94):
            events[line, 2] = 404 # target p4
        elif (listType == 1 and reward == 5 and events[line, 2] == 93) or \
                (listType == 2 and reward == 5 and events[line, 2] == 95) or \
                (listType == 3 and reward == 5 and events[line, 2] == 98) or \
                (listType == 4 and reward == 5 and events[line, 2] == 96):
            events[line, 2] = 405 # target p5
        elif (listType == 1 and reward != 1 and events[line, 2] == 91) or \
                (listType == 2 and reward != 1 and events[line, 2] == 100) or \
                (listType == 3 and reward != 1 and events[line, 2] == 95) or \
                (listType == 4 and reward != 1 and events[line, 2] == 99):
            events[line, 2] = 411 # distractor p1
        elif (listType == 1 and reward != 2 and events[line, 2] == 92) or \
             (listType == 2 and reward != 2 and events[line, 2] == 92) or \
             (listType == 3 and reward != 2 and events[line, 2] == 94) or \
             (listType == 4 and reward != 2 and events[line, 2] == 97):
            events[line, 2] = 412  # distractor p2
        elif (listType == 1 and reward != 3 and events[line, 2] == 95) or \
                (listType == 2 and reward != 3 and events[line, 2] == 99) or \
                (listType == 3 and reward != 3 and events[line, 2] == 91) or \
                (listType == 4 and reward != 3 and events[line, 2] == 92):
            events[line, 2] = 413  # distractor p3
        elif (listType == 1 and reward != 4 and events[line, 2] == 94) or \
                (listType == 2 and reward != 4 and events[line, 2] == 97) or \
                (listType == 3 and reward != 4 and events[line, 2] == 92) or \
                (listType == 4 and reward != 4 and events[line, 2] == 94):
            events[line, 2] = 414  # distractor p4
        elif (listType == 1 and reward != 5 and events[line, 2] == 93) or \
                (listType == 2 and reward != 5 and events[line, 2] == 95) or \
                (listType == 3 and reward != 5 and events[line, 2] == 98) or \
                (listType == 4 and reward != 5 and events[line, 2] == 96):
            events[line, 2] = 415  # distractor p5

    mne.write_events(path + 'events/events' + sub +
                     '-recall-targetdist-eve.fif', events, overwrite=True)
