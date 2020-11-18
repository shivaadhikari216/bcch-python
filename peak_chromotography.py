#Program to analyze the size exclusion chromatogram for peaks
#https://github.com/shivaadhikari216/bcch-python.git
#Make sure you have the file with proper name in the directory
xx=open("superose6_50.asc") #Open the file 
cc=0 #Counter 
amps=[] #to keep track of the  amplitude 
vals=[] #to keep track of the time segments 
for x in xx:
    cc=cc+1
    if cc<4: #the first 4 lines seems to be the header file 
        continue
    x=x.rstrip()
    x=x.split("\t")
    if len(x)<2: #need 2 columns at least 
        continue
    vals.append(float(x[0]))
    amps.append(float(x[1]))
import matplotlib.pyplot as plt
plt.plot(amps)
#plt.show()
peaks=[] #to capture the amplitude of peaks 
peaks_windows=[] #to capture the timstamps of peaks 
running_peak=0 #a flag to check if a peak streak is running or not , set for False 
peakidx=-1 #start with 0 peaks 
peak_threshold=2 #adjustable parameter that we would need to set on the max height of change to define a peak as
for idx in range(0,len(amps)-2): #We check for current amplitude with next 2 amplitudes so 
    if abs(amps[idx+1]-amps[idx])>peak_threshold and abs(amps[idx+2]-amps[idx])>peak_threshold: #chec
        #if thereis an increase in amp above the threshold
        if running_peak==0: #check if there is a peak already running
            running_peak=1 #if no active peak , trigger one 
            peakidx+=1 #increase the peak index
            peaks.append([]) #lay out a new peak array for values
            peaks[peakidx].append(amps[idx]) #add the current index amplitude
            peaks_windows.append([]) # lay out a new peak array for window
            peaks_windows[peakidx].append(vals[idx]) #add the current timestamp
        else:
            #a peak is already running , so just add the current time frame and amplitude to the peakidx(current)array
            peaks[peakidx].append(amps[idx]) 
            peaks_windows[peakidx].append(vals[idx])
    else:
        running_peak=0 # Discountinue an active peak (if there was one )
print("There were ",peakidx+1," peaks identified")
thresholded_peaks=[]
thresholded_peak_windows=[]
min_peak_window=5 # We need to clean off noise taht may be brought by smaller window of peak length 
#We noticed that for one second of time there are around 5 observations , so we set 5 as the window 
#Any peak that doesn't have at least 5 entries will be discarded 
for peakid in range(0,peakidx+1):
    if len(peaks[peakid])>min_peak_window:
        thresholded_peaks.append(peaks[peakid])
        thresholded_peak_windows.append(peaks_windows[peakid])
#Now let's print the peak stats 
for peakid in range(0,len(thresholded_peaks)):
    print("Peak ",peakid+1)
    print("Begins at ",thresholded_peak_windows[peakid][0]) #Get the starting point 
    print("Ends at ",thresholded_peak_windows[peakid][-1]) #Get the endinng point 
    maxval=max(thresholded_peaks[peakid])
    maxidx=thresholded_peaks[peakid].index(maxval) # Get the index where it occured 
    print("Maximum observance value at Peak",peakid+1," : ",maxval," occuring at time",thresholded_peak_windows[peakid][maxidx])
    print("----------")
plt.show()
