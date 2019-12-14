"""
This is a selection of functions for plotting MDS projections of relative magnitude-trained networks.

Author: Hannah Sheahan, sheahan.hannah@gmail.com
Date: 13/12/2019
Notes: N/A
Issues: N/A
"""
# ---------------------------------------------------------------------------- #
import define_dataset as dset
import matplotlib.pyplot as plt
import numpy as np
import copy
import sys
import random

from sklearn.metrics import pairwise_distances
from sklearn.manifold import MDS
from sklearn.utils import shuffle

# generic plotting settings
contextcolours = ['gold', 'dodgerblue', 'orangered']   # 1-15, 1-10, 5-15 like fabrices colours

# ---------------------------------------------------------------------------- #

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)

# ---------------------------------------------------------------------------- #

def autoSaveFigure(basetitle, blockedTraining, sequentialABTraining, labelNumerosity, saveFig):
    """This function will save the currently open figure with a base title and some details pertaining to how the activations were generated."""
    # automatic save file title details
    if blockedTraining:
        blockedtext = '_blocked'
    else:
        blockedtext = ''

    if sequentialABTraining:
        seqtext = '_sequential'
    else:
        seqtext = ''
    if labelNumerosity:
        labeltext = '_numerosity'
    else:
        labeltext = '_contexts'

    if saveFig:
        plt.savefig(basetitle+blockedtext+seqtext+labeltext+'.pdf',bbox_inches='tight')

# ---------------------------------------------------------------------------- #

def activationRDMs(activations, sl_activations):
    """Plot the representational disimilarity structure of the hidden unit activations, sorted by context, and within that magnitude.
    Context order:  1-15, 1-10, 5-15
    """
    fig, ax = plt.subplots(1,2)
    D = pairwise_distances(activations)  # note that activations are structured by: context (1-15,1-10,5-15) and judgement value magnitude within that.
    im = ax[0].imshow(D, zorder=2, cmap='Blues', interpolation='nearest')
    fig.colorbar(im, ax=ax[0])
    ax[0].set_title('All activations')

    # this looks like absolute magnitude to me (note the position of the light diagonals on the between context magnitudes - they are not centred)
    D = pairwise_distances(sl_activations)
    im = ax[1].imshow(D, zorder=2, cmap='Blues', interpolation='nearest')
    fig.colorbar(im, ax=ax[1])
    ax[1].set_title('Averaged activations')

# ---------------------------------------------------------------------------- #

def plot3MDS(MDS_activations, MDSlabels, labels_refValues, labels_judgeValues, labels_contexts, labelNumerosity, blockedTraining, sequentialABTraining, saveFig):
    """This is a function to plot the MDS of activations and label according to numerosity and context"""

    # Plot the hidden activations for the 3 MDS dimensions
    fig,ax = plt.subplots(3,3, figsize=(14,15))
    colours = get_cmap(10, 'viridis')
    diffcolours = get_cmap(20, 'viridis')

    for k in range(3):
        for j in range(3):  # 3 MDS dimensions
            if j==0:
                dimA = 0
                dimB = 1
                ax[k,j].set_xlabel('dim 1')
                ax[k,j].set_ylabel('dim 2')
            elif j==1:
                dimA = 0
                dimB = 2
                ax[k,j].set_xlabel('dim 1')
                ax[k,j].set_ylabel('dim 3')
            elif j==2:
                dimA = 1
                dimB = 2
                ax[k,j].set_xlabel('dim 2')
                ax[k,j].set_ylabel('dim 3')

            for i in range((MDS_activations.shape[0])):
                if labelNumerosity:

                    # colour by numerosity
                    if k==0:
                        ax[k,j].scatter(MDS_activations[i, dimA], MDS_activations[i, dimB], color=diffcolours(int(10+labels_judgeValues[i]-labels_refValues[i])), edgecolors=contextcolours[int(labels_contexts[i])-1])
                    elif k==1:
                        ax[k,j].scatter(MDS_activations[i, dimA], MDS_activations[i, dimB], color=colours(int(labels_refValues[i])-1), edgecolors=contextcolours[int(labels_contexts[i])-1])
                    else:
                        im = ax[k,j].scatter(MDS_activations[i, dimA], MDS_activations[i, dimB], color=colours(int(labels_judgeValues[i])-1), edgecolors=contextcolours[int(labels_contexts[i])-1])
                        if j==2:
                            if i == (MDS_activations.shape[0])-1:
                                cbar = fig.colorbar(im, ticks=[0,1])
                                if labelNumerosity:
                                    cbar.ax.set_yticklabels(['1','15'])

                else:
                    # colour by true/false label
                    if MDSlabels[i]==0:
                        colour = 'red'
                    else:
                        colour = 'green'
                    ax[k,j].scatter(MDS_activations[i, dimA], MDS_activations[i, dimB], color=colour)

                # some titles
                if k==0:
                    ax[k,j].set_title('value difference')
                    ax[k,j].axis('equal')
                elif k==1:
                    ax[k,j].set_title('reference')
                else:
                    ax[k,j].set_title('judgement')
                ax[k,j].set(xlim=(-3, 3), ylim=(-3, 3))  # set axes equal and the same for comparison

    autoSaveFigure('figures/3MDS60_', blockedTraining, sequentialABTraining, labelNumerosity, saveFig)

# ---------------------------------------------------------------------------- #

def plot3MDSContexts(MDS_activations, MDSlabels, labels_refValues, labels_judgeValues, labels_contexts, labelNumerosity, blockedTraining, sequentialABTraining, saveFig):
    """This is a just function to plot the MDS of activations and label the dots with the colour of the context."""

    fig,ax = plt.subplots(1,3, figsize=(14,5))
    colours = get_cmap(10, 'magma')
    diffcolours = get_cmap(20, 'magma')
    for j in range(3):  # 3 MDS dimensions

        if j==0:
            dimA = 0
            dimB = 1
            ax[j].set_xlabel('dim 1')
            ax[j].set_ylabel('dim 2')
        elif j==1:
            dimA = 0
            dimB = 2
            ax[j].set_xlabel('dim 1')
            ax[j].set_ylabel('dim 3')
        elif j==2:
            dimA = 1
            dimB = 2
            ax[j].set_xlabel('dim 2')
            ax[j].set_ylabel('dim 3')

        ax[j].set_title('context')
        for i in range((MDS_activations.shape[0])):
            # colour by context
            ax[j].scatter(MDS_activations[i, dimA], MDS_activations[i, dimB], color=contextcolours[int(labels_contexts[i])-1])

        ax[j].axis('equal')
        ax[j].set(xlim=(-3, 3), ylim=(-3, 3))

    autoSaveFigure('figures/3MDS60_contexts_', blockedTraining, sequentialABTraining, labelNumerosity, saveFig)

# ---------------------------------------------------------------------------- #

def plot3MDSMean(MDS_activations, MDSlabels, labels_refValues, labels_judgeValues, labels_contexts, labelNumerosity, blockedTraining, sequentialABTraining, saveFig):
    """This function is just like plot3MDS and plot3MDSContexts but for the formatting of the data which has been averaged across one of the two numerosity values.
    Because there are fewer datapoints I also label the numerosity inside each context, like Fabrice does.
    """
    fig,ax = plt.subplots(1,3, figsize=(18,5))
    colours = get_cmap(10, 'magma')
    diffcolours = get_cmap(20, 'magma')
    for j in range(3):  # 3 MDS dimensions
        if j==0:
            dimA = 0
            dimB = 1
            ax[j].set_xlabel('dim 1')
            ax[j].set_ylabel('dim 2')
        elif j==1:
            dimA = 0
            dimB = 2
            ax[j].set_xlabel('dim 1')
            ax[j].set_ylabel('dim 3')
        elif j==2:
            dimA = 1
            dimB = 2
            ax[j].set_xlabel('dim 2')
            ax[j].set_ylabel('dim 3')

        ax[j].set_title('context')

        # perhaps draw a coloured line between adjacent numbers
        contextA = range(15)
        contextB = range(15,25)
        contextC = range(25, 35)
        ax[j].plot(MDS_activations[contextA, dimA], MDS_activations[contextA, dimB], color=contextcolours[2])
        ax[j].plot(MDS_activations[contextB, dimA], MDS_activations[contextB, dimB], color=contextcolours[0])
        ax[j].plot(MDS_activations[contextC, dimA], MDS_activations[contextC, dimB], color=contextcolours[1])

        for i in range((MDS_activations.shape[0])):
            # colour by context
            ax[j].scatter(MDS_activations[i, dimA], MDS_activations[i, dimB], color=contextcolours[int(labels_contexts[i])-1], s=80)

            # label numerosity in white inside the marker
            ax[j].text(MDS_activations[i, dimA], MDS_activations[i, dimB], str(int(labels_judgeValues[i])), color='black', size=8, horizontalalignment='center', verticalalignment='center')


        ax[j].axis('equal')
        ax[j].set(xlim=(-2.5, 2.5), ylim=(-2.5, 2.5))

    autoSaveFigure('figures/3MDS60_meanJudgement_', blockedTraining, sequentialABTraining, labelNumerosity, saveFig)

# ---------------------------------------------------------------------------- #

def averageReferenceNumerosity(dimKeep, activations, labels_refValues, labels_judgeValues, labels_contexts, MDSlabels):
    """This function will average the hidden unit activations over one of the two numbers involved in the representation:
    either the reference or the judgement number. This is so that we can then compare to Fabrice's plots
     which are averaged over the previously presented number (input B).
    Prior to performing the MDS we want to know whether to flatten over a particular value
    i.e. if plotting for reference value, flatten over the judgement value and vice versa.
     - dimKeep = 'reference' or 'judgement'
    """

    # initializing
    uniqueValues = [int(np.unique(labels_judgeValues)[i]) for i in range(len(np.unique(labels_judgeValues)))]
    Ncontexts = 3
    flat_activations = np.zeros((Ncontexts,len(uniqueValues),activations.shape[1]))
    flat_values = np.zeros((Ncontexts,len(uniqueValues),1))
    flat_outcomes = np.empty((Ncontexts,len(uniqueValues),1))
    flat_contexts = np.empty((Ncontexts,len(uniqueValues),1))
    divisor = np.zeros((Ncontexts,len(uniqueValues)))

    # which label to flatten over (we keep whichever dimension is dimKeep, and average over the other)
    if dimKeep == 'reference':
        flattenValues = labels_refValues
    else:
        flattenValues = labels_judgeValues

    # pick out all the activations that meet this condition for each context and then average over them
    for context in range(Ncontexts):
        for value in uniqueValues:
            for i in range(labels_judgeValues.shape[0]):
                if labels_contexts[i] == context+1:  # remember to preserve the context structure
                    if flattenValues[i] == value:
                        flat_activations[context, value-1,:] += activations[i]
                        flat_contexts[context,value-1] = context
                        flat_values[context,value-1] = value
                        flat_outcomes[context,value-1] = MDSlabels[i]
                        divisor[context,value-1] +=1

            # take the mean i.e. normalise by the number of instances that met that condition
            if int(divisor[context,value-1]) == 0:
                flat_activations[context, value-1] = np.full_like(flat_activations[context, value-1], np.nan)
            else:
                flat_activations[context, value-1] = np.divide(flat_activations[context, value-1, :], divisor[context,value-1])

    # now cast out all the null instances e.g 1-5, 10-15 in certain contexts
    flat_activations, flat_contexts, flat_values, flat_outcomes = [dset.flattenFirstDim(i) for i in [flat_activations, flat_contexts, flat_values, flat_outcomes]]
    sl_activations, sl_refValues, sl_judgeValues, sl_contexts, sl_MDSlabels = [[] for i in range(5)]

    for i in range(flat_activations.shape[0]):
        checknan = np.asarray([ np.isnan(flat_activations[i][j]) for j in range(len(flat_activations[i]))])
        if (checknan).all():
            pass
        else:
            sl_activations.append(flat_activations[i])
            sl_contexts.append(flat_contexts[i])
            sl_MDSlabels.append(flat_outcomes[i])

            if dimKeep == 'reference':
                sl_refValues.append(flat_values[i])
                sl_judgeValues.append(0)
            else:
                sl_refValues.append(0)
                sl_judgeValues.append(flat_values[i])

    # finally, reshape the outputs so that they match our inputs nicely
    sl_activations, sl_refValues, sl_judgeValues, sl_contexts, sl_MDSlabels = [np.asarray(i) for i in [sl_activations, sl_refValues, sl_judgeValues, sl_contexts, sl_MDSlabels]]
    if dimKeep == 'reference':
        sl_judgeValues = np.expand_dims(sl_judgeValues, axis=1)
    else:
        sl_refValues = np.expand_dims(sl_refValues, axis=1)

    return sl_activations, sl_contexts, sl_MDSlabels, sl_refValues, sl_judgeValues

# ---------------------------------------------------------------------------- #
