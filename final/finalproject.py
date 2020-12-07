import matplotlib
#Use this to supress in command output , cuz we want to redirect all our output to the final html 
matplotlib.use('Agg')
import matplotlib.pyplot as plt

print("Welcome to Fluoroscence activity analyzer")
print("------")
#Used later as gloabl samples tracker
print("Please enter the number of samples")
numsamples=int(input())
#volume array 
vols=[]
#Samples array
samples=[]
print("-------")
#Take the name of samples in a loop 

#In this example case the samples would be tdp43 , grn7 , and tdp43_grn7
print("Enter the name of samples without the .csv extension (Note : should be same as the CSV data file")
for x in range(0,numsamples):
        print("Please enter the name of sample ",x+1)
        xx=input()
        samples.append(xx)
print("-------")
#Take the volumes of samples in a loop 
for x in range(0,numsamples):
	print("Please enter the volume of sample ",x+1)
	xx=int(input())
	vols.append(xx)
#Gather other data  
print("Enter the temperature for experiment (C) ")
temp=int(input())
print("--------")
print("Enter the wavelength for experiment (nm) ")
wavelength=int(input())
print("--------")
print("Enter the time for experiment (hours) ")
time=int(input())
print("---------")
print("Select an Assay (1 or 2)")
print("1. ThT")
print("2. Turbidity")
option=int(input())
assays={1:"ThT",2:"Turbidity"}

import time
print("Starting activity using ThT Assay for Temperature : ",temp," Wavelength : ",wavelength," Time : ",time)
time.sleep(3)

#Function time 
def calculateaggregration(X,Y):
        threshold=0.1 #slope rising threshold
        min_continuity=10 #should run for at least this much iterations
        starting=0
        aggregrated_start=0
        aggregrated_end=0
        for x in range(1,len(X)):
                if Y[x]-Y[x-1]>threshold: #Checking the slope 
                        if starting==0:
                                starting=1
                        else:
                                starting+=1
                if Y[x]-Y[x-1]<threshold: #Check for where it ends 
                        if starting!=0 and aggregrated_end==0:
                                aggregrated_end=X[x];
                if starting>min_continuity and aggregrated_start==0: #Check for where it starts 
                        aggregrated_start=X[x]
        return (aggregrated_start,aggregrated_end) #Return the start and end time tuple 

def plot(X,Y,filename,assayname): #plotting function based on given X array Y array and filename 
        plt.clf()
        plt.xlabel("time")
        plt.ylabel(assayname+" Fluroscence Au")
        plt.title(filename)
        plt.plot(X,Y,label=filename)
        plt.legend()
        plt.savefig(filename+".png")


#Read in the csv files based on the given inputs and build up the array of array 
Xs=[]
Ys=[]
for n in range(0,numsamples):
        X=[]
        Y=[]
        print("Reading "+samples[n]+".csv")
        xx=open(samples[n]+".csv")
        for x in xx:
                x=x.rstrip()
                x=x.split(",")
                X.append(float(x[0]))
                Y.append(float(x[1]))
        plot(X,Y,samples[n],assays[option])
        Xs.append(X)
        Ys.append(Y)
#Plot summary results
plt.clf()
plt.xlabel("time")
plt.ylabel(assays[option]+"Fluroscence Au")
plt.title("Aggregrate Results")
for n in range(0,numsamples):
        plt.plot(Xs[n],Ys[n],label=samples[n])
plt.legend()
plt.savefig("aggregrate_results.png")


#After we have generated the graphs , we start dynamically producing the HTML for our results web page 
#using the technique called format string in python 

finalhtml="""<html>
<head>
<title>
Fluorescence Activity to Mediate Aggregation
</title>
</head>
<body>
<h1>
Title : Monitoring Aggregation between TDP43-CTD and GRN-7 using Fluorescence
</h1>
<h2>
Background: Mutations in progranulins (PGRN) gene leading to its haploinsufficiency are
strong causative factors related to FTLD. Recently, specific GRN modules have been shown to
directly interact and exacerbate the toxicity of TDP-43. With the help of different biophysical
characterization, our lab has shown the interaction between the pathological C-terminal domain
of TDP-43 (TDP-43 CTD) and GRNs, -3, -5. The results showed that GRN-3 and GRN-5
modulate the aggregation and phase behavior of TDP-43 CTD in different ways. Now, in this
project we are interested in understanding the interaction between GRN-7 with TDP-43 CTD and
which leads us to extend these investigations on GRN-7 and its characterization. Intrinsically
disordered protein (IDP), Granulin-7 shows aggregation when reacted with TDP43-CTD
monitored by fluorescence assay.
</h2>
<h2> Assay and parameters </h1>
"""
#Feed in the additional metadata from the variables

finalhtml+=str(numsamples)+" Samples. "+"<br>"
for x in range(0,numsamples):
	finalhtml+=" Volume "+str(x)+" : "+ str(vols[x])+" ml "+"<br>"

finalhtml+="Temperature : "+str(temp)+" C "+"<br>"
finalhtml+="Wavelength : "+str(wavelength)+" nm "+"<br>"
finalhtml+="Experiment time :"+str(time)+" nm "+"<br>"
finalhtml+="Assay :"+assays[option]+"<br>"

#Format strings to print in the html based on variables

msg_no_aggregration="Results: No significant aggregation observed at any time frame."
msg_aggregration="Aggregration observed at {0} hrs till {1} hours (from the graph)"
sample_description="{0} ml of {1} ran for {2} at {3} degrees using {4} assay ({5} nm)"
msg_summary="Significant aggregation observed in Sample {0}, ({1})"

##Run the python code here  along with parsing and stuffs 
#1st img

aggregration_sample=0
aggrgration_sample_name=""
for x in range(0,numsamples):
        result=calculateaggregration(Xs[x],Ys[x])#callaggregration to get the aggregration results 
        #Add the image first ,based on the sample name 
        finalhtml+='<img src="'+samples[x]+'.png" alt="'+samples[x]+'" class="center" style="display: block;margin-left:auto;margin-right: auto;width: 25%">'
        finalhtml+='<h3 style="text-align: center;">'
        #Add the description of the result based on format string 
        finalhtml+=sample_description.format(vols[x],samples[x],time,temp,assays[option],wavelength)
        #Generate the result explanation based on aggregration found or not 
        if (result[0]==0 and result[1]==0):
            finalhtml=finalhtml+msg_no_aggregration+"</h3>"
        else:
            finalhtml+=msg_aggregration.format(result[0],result[1])+"</h3>"
            aggregration_sample=x
            aggregration_sample_name=samples[x]
#generate the final  aggregrate result 
finalhtml+="""<img src="aggregrate_results.png" alt="first_img" class="center" style="display: block;margin-left:auto;margin-right: auto;width: 25%">
<h3 style="text-align: center;">"""
finalhtml+="Aggregrate Results : "
finalhtml+=msg_summary.format(aggregration_sample,aggregration_sample_name)

finalhtml+="</body></html>"

#write the generated html to a file 
with open("final_output.html","w") as f:
        f.write(finalhtml)


print("The results are in the file final_output.html. I will try to open it for you . If it fails to open , you can also open it manually !")
import os
#Let's try open the HTML file using open command from the shell 
os.system('open final_output.html')
 