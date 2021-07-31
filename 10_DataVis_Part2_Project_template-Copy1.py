#!/usr/bin/env python
# coding: utf-8

# # Data Visualization 
# 

# In[3]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns


# In[4]:


annotation = pd.read_csv("10_project_data_annotation.csv")
annotation.head()


# In[5]:


signals = pd.read_csv("10_project_data_signals.csv")
signals.head()


# ### 1.1: Version.1

# In[13]:


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches 



class AnnotationPlot:
    
    def __init__(self, annotation,signals):
        """Initialize annotation and signals attributes"""
        
        self.annotation = annotation
        self.signals = signals
    
    def f_axes(self, gridspec_kw=None,signals=0):
        
        
        """the function handles 2 conditions with conditions 1 to make a suplot 
        by returning lenght of signal as list
        and condition 2, lenght of signals as integer for the upcoming plots.5 rows and a column
        for each plot with gridspec set as NONE by default"""
        
        nrow = None
        try:
            nrow = len(signals) # df signals return list
        except Exception as ex:
            nrow = signals # df signals return int
            
        return plt.subplots(nrows=nrow+1, sharex=True, ) if gridspec_kw==None else                 plt.subplots(nrows=nrow+1, sharex=True,gridspec_kw=gridspec_kw)
        
    def get_annotations(self,f=None,axes=None):
        

        ## code to plot annotations i.e boxplot
        axes[-1].set_xlabel('Genomic position')
        axes[-1].set_ylabel('annotations')
        axes[-1].set_ylim(-0.5, 1.5)
        axes[-1].set_yticks([0, 1])
        axes[-1].set_yticklabels(['−', '+'])

        #loop iterating over dataframe rows
        for _ , rws in self.annotation.iterrows():
            marker = '|'
            lw=1
            # if its "type" has "exon"
            if rws['type'] == 'exon':
                """column type has 'exon, set marker as None' """
                marker=None
                lw=8 #width length of 8
            y = 1 if rws['strand'] == '+' else 0
            axes[-1].plot((rws['start'], rws['stop']), (y, y),
                    marker=marker, lw=lw,
                    solid_capstyle='butt',
                    color='black')

        # remove space between plots
        plt.subplots_adjust(hspace=0)

        # set plot size
        f.set_size_inches(15, 5)
        
    def getplot_version1(self,):
        
        """return f_axes function and assign to f, axes"""
        
        f, axes = self.f_axes(signals=self.signals.columns)
        
        
        # set dimension and color for signals col plot
        i = 0
        x1 = self.signals
        for col in x1.columns:
            x1[col].plot(ax=axes[i], color='#434343')
            axes[i].set_ylim(0, 1.3)
            axes[i].set_ylabel(col) # set col names of signals df
            i+=1
        self.get_annotations(f,axes) # call anotation function
        axes[-1].set_xlim(0, len(signals))
        
    def getplot_version2(self,):
        
        """Creat the subplots with geometry on how the plot should be placed.
        sending  "kwargs" to "GridSpec" from within  subplots call, using the gridspec_kw argument
        which is a dictionary with "height_ratios" as keyword and hold the lenght of "signals" columns
        obtain by using "np.repeat" method to repeat column lenght by 1 """

        gridspec_kw={'height_ratios':np.append(np.repeat(1, len(signals.columns)), 3)}
        f, axes = self.f_axes(gridspec_kw=gridspec_kw,signals=self.signals.columns)
        
        # plots for signals dataframe columns
        i = 0
        x1 = self.signals
        for col in x1.columns:
            axes[i].scatter(x=x1.index, y=np.repeat(0, len(x1)), c=x1[col], marker='|', cmap='Greys')
            axes[i].set_ylim(-0.5, 0.5) #set possition for boxplot on annotation
            axes[i].set_yticks([0])
            axes[i].set_yticklabels([col]) # set col names of signals df 
            i+=1
        self.get_annotations(f,axes)
        

    def getplot_version3(self,):
        
        """return f_axes and assign to fig, axs which handles the 
        catch exeption to take the lenght of signals df as an integer
        for the plot."""
        
        fig, axs = self.f_axes(signals=1)
       
        # plots for signals dataframe
        axs[0].plot(self.signals["P1"], c="#06C2AC")
        axs[0].plot(self.signals["P2"], c="#7BC8F6")
        axs[0].plot(self.signals["P3"], c="#FFD700")
        axs[0].plot(self.signals["P4"], c="#808080")
    
        #legend plots
        legend_a = mpatches.Patch(color='#06C2AC', label='P1')
        legend_b = mpatches.Patch(color='#7BC8F6', label='P2')
        legend_c = mpatches.Patch(color='#FFD700', label='P3')
        legend_d = mpatches.Patch(color='#808080', label='P4')
        plt.legend(handles=[legend_a,legend_b,legend_c,legend_d], loc='upper left')
        
        self.get_annotations(fig,axs)
        axs[-1].set_xlim(0, len(signals))

        
        


# In[14]:


# initialize the Class object
data = AnnotationPlot(annotation,signals)


# In[15]:


data.getplot_version1()


# In[16]:


data.getplot_version2()


# In[10]:


data.getplot_version3()

