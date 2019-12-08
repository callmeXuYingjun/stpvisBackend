import numpy

def summation(number):
    sum=0
    for i in range(number):
        sum+=i
    return 
    

my_matrix = numpy.loadtxt(open("C:\\Users\\Administrator\\Desktop\\industry_two_7\\zhou_0\\补课办班.csv","rb"),delimiter=",",skiprows=1,usecols=[0:3]) 
print(my_matrix) 