from munkres import Munkres, print_matrix
import requests
import json
import math

def Hungarian(matrix,i):
    m = Munkres()
    indexes = m.compute(matrix)
    #print_matrix(matrix, msg='Minimum distance through this matrix:')
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        y=cnos[column]
        z=i[row][column]
        print ('Agent %d will go to the customer %d at address no. %d and have to travel %d kms' % (row, y ,z, value))
        lax[row] = lcxs[column][i[row][column]]
        lay[row] = lcys[column][i[row][column]]
    print ('Minimum distance: %d kms' % total)
def URL(a,b,c,d): #https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=40.6655101,-73.89188969999998&destinations=40.6905615%2C-73.9976592&key=
    basic_link ='https://maps.googleapis.com/maps/api/distancematrix/'
    file_type='json?'  #can use xml also
    units='units=metric&'   #can also be imperial
    start_point='origins=%s,%s'%(a,b)
    end_point='&destinations=%s,%s&key='% (c,d)
    key=input("please enter your unique key")
    URL= '%s%s%s%s%s%s'%(basic_link,file_type,units,start_point,end_point,key)
    return URL
def location():
    '''locationax= [float(x) for x in input("Please provide x coordinates of the agents:\n").split()]
    locationay=[float(x) for x in input("Please provide y coordinates of the agents:\n").split()]
    no_of_customers=int(input("How many customers do we have?\n"))
    locationcx=[]
    locationcy=[]
    rank=[]'''
    cno=[]
    locationax = [12.9716, 26.9124, 18.960]
    locationay = [77.5946, 75.7873, 72.820]

    locationcx = [[13.090, 23.030, 17.4, 18.53], [19.95, 28.6353, 22.570, 13.090],
                  [19.95, 28.6353, 22.570, 13.090, 23.030, 17.4, 18.53], [19.076, 19.95]]
    locationcy = [[80.270, 72.580, 78.480, 73.840], [79.3, 77.225, 88.360, 80.270],
                  [79.3, 77.225, 88.360, 80.270, 72.580, 78.480, 73.840], [72.8777, 79.3]]
    no_of_customers=4
    rank=[3,2,4,1]
    for x in range(no_of_customers):
        '''r = int(input("What is the priority of customer %d?\n" %(x)))
        lx = [float(x) for x in input("Please provide x coordinates of customer %d:\n" % (x)).split()]
        ly = [float(x) for x in input("Please provide y coordinates of customer %d:\n" % (x)).split()]
        rank.append(r)
        locationcx.append(lx)
        locationcy.append(ly)'''
        cno.append(x)

    return locationax,locationay,locationcx,locationcy, no_of_customers,rank,cno
def distance(i, j):
    l=[]
    for k in range(len(lcxs[j])):
        link=URL(lax[i],lay[i],lcxs[j][k],lcys[j][k])
        result = requests.get(link)
        data = (result.json())
        dist = data["rows"][0]["elements"][0]["distance"]["text"]
        k = dist.split()
        m=float(k[0].replace(',', ''))
        l.append(m)
    #print(l)
    #print(min(l))
    return min(l), l.index(min(l))
def ordered(lcx, lcy,cno, rank):
    sorted_y_idx_list = sorted(range(len(rank)), key=lambda x: rank[x])
    lcxs = [lcx[i] for i in sorted_y_idx_list]
    lcys = [lcy[i] for i in sorted_y_idx_list]
    cnos=[cno[i] for i in sorted_y_idx_list]
    #print(lcxs)
    #print(lcys)
    #print(cnos)
    return lcxs, lcys, cnos
def update_everything():
    for j in range(len(lax)):
        del lcxs[0]
        del lcys[0]
        del cnos[0]

lax, lay, lcx, lcy, noc, rank,cno= location()
lcxs, lcys, cnos = ordered(lcx, lcy, cno, rank)

def run():
    Matrix = []
    shortest_address = []
    for f in range(len(lax)):
        r=[]
        i=[]
        for j in range(len(lax)):
            u,v=distance(f,j)
            k=float(u)
            r.append(k)
            i.append(v)
        Matrix.append(r)
        shortest_address.append(i)
    print (Matrix)
    Hungarian(Matrix,shortest_address)

while len(lax)<len(lcxs):
    run()
    update_everything()
Matrix = []
shortest_address = []
for f in range(len(lax)):
        r=[]
        i=[]
        for j in range(len(lcxs)):
            u,v=distance(f,j)
            k=float(u)
            r.append(k)
            i.append(v)
        Matrix.append(r)
        shortest_address.append(i)
print (Matrix)
Hungarian(Matrix,shortest_address)