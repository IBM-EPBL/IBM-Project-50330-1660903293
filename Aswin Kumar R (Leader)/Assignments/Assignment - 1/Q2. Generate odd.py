# Q2.Write a program to generate odd numbers from m to nusing while loop.

m=int(input ("Enter the number where you want to start: "))
n=int(input ("Enter the number where you want to end: "))

while m<=n:
    if m % 2!=0:
        print("The odd number(s) are",m)
        m+=1
    else:
        m+=1