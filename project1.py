#Atomic mass needed captured into dictionary 
ATOMIC_MASS={'O':15.999,'N':14.007,'C':12.011,'S':32.06}
xx=open("2FA9noend.pdb.txt")
#all_atoms is our dict of dict 
all_atoms=[]
cc=0
for x in xx:
    x=x.rstrip()
    rcdname=x[0:5]
    serial=x[7:11]
    name=x[13:16]
    altLoc=x[16]
    resName=x[17:20]
    chainId=x[21]
    resSeq=x[23:26]
    iCode=x[26:29]
    xcoord=float(x[32:38])
    ycoord=float(x[39:46])
    zcoord=float(x[48:54])
    occupancy=x[56:60]
    tempFactor=x[61:66]
    element="" # Missing in input file 
    charge=x[77:78] 
    dat=[rcdname,serial,name,altLoc,resName,chainId,resSeq,iCode,xcoord,ycoord,zcoord,occupancy,tempFactor,element,charge]  
    all_atoms.append(dat)

#Center all the atoms given teh centeringf actor
def center(center_by):
    for atom in all_atoms:
       atom[8]=atom[8]-center_by[0]
       atom[9]=atom[9]-center_by[1]
       atom[10]=atom[10]-center_by[2]

#Write the output file
def write_centered(file):
    outfile=open(file,"w")
    for atom in all_atoms:
        o1=atom[0].ljust(6)
        o2=atom[1].rjust(5)
        o3=atom[2].center(4)
       #o4=atom[3]
        o5=atom[4].ljust(3)#resname
        o6=atom[5].rjust(1)#chain identifier
        o7=atom[6].rjust(4)#residue sequence number
        o8=atom[7].rjust(1)#code for insetion of residues
        o9=str('%8.3f' % (float(atom[8]))).rjust(8) # x coord
        o10=str('%8.3f' % (float(atom[9]))).rjust(8)
        o11=str('%8.3f' % (float(atom[10]))).rjust(8)
        o12=str('%6.2f'%(float(atom[11]))).rjust(6) #occupancy
        o13=str('%6.2f'%(float(atom[12]))).rjust(6) #tempf
        o14=atom[-1].rjust(12)#element name
        outfile.write("%s %s  %s %s %s %s %s %s %s %s %s %s %s\n"%(o1,o2,o3,o5,o6,o7,o8,o9,o10,o11,o12,o13,o14)) 
    outfile.close()

#Calculating geometric center and returns a tuple of (X,Y,Z) 
 
def geometric_center():
    xsum=0
    ysum=0
    zsum=0
    for atom in all_atoms:
        xsum+=atom[8]
        ysum+=atom[9]
        zsum+=atom[10]
    xsum=xsum/len(all_atoms)
    ysum=ysum/len(all_atoms)
    zsum=zsum/len(all_atoms)
    return (xsum,ysum,zsum)
#Calculating center of mass and returns a tuple of (X,Y,Z) 
def center_of_mass():
    xsum=0
    ysum=0
    zsum=0
    sum_masses=0
    #Calculate total mass ( the denominator part )  first 
    for atom in all_atoms:
        mass=ATOMIC_MASS[atom[-1].rstrip()]
        xsum+=(atom[8]*mass)
        ysum+=(atom[9]*mass)
        zsum+=(atom[10]*mass)
        sum_masses+=mass    
    xcenter=xsum/sum_masses
    ycenter=ysum/sum_masses
    zcenter=zsum/sum_masses
    return (xcenter,ycenter,zcenter)


#Main program 
print("Do you want the centering to be done by geometric center or by center of mass ?")
file_name=""
while(1):
    val=input("Enter G for Geometric center and M for Center of Mass \n")
    if (val.lower()=="g"):
        print("Centering by Geometric Center")
        file_name="geometric_centered.pdb"
        center(geometric_center())  
        break
    elif (val.lower()=="m"):
        print("Centering by Center of Mass")
        center(center_of_mass())
        file_name="mass_centered.pdb"
        break
    else:
        print("Invalid Input. Try Again")
write_centered(file_name)
print("See file %s for output "%file_name)