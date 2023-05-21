# import K_map_gui_tk;

import time

Allminterms=dict()


def checks2ins1(s1,s2):
    i1=int(0)
    i2=int(0)
    sz1=int(len(s1))
    sz2=int(len(s2))
    pos=True
    while(i1<sz1 and i2<sz2):
        if(s1[i1]==s2[i2]):
            if(i2<sz2-1 and s2[i2+1]=="'"):
                if(i1<sz1-1 and s1[i1+1]!="'"):
                    pos=False
                    break
                elif(i1==sz1-1):
                    pos=False
                    break
                else:
                    i1+=2
                    i2+=2
            else:
                if(i1<sz1-1 and s1[i1+1]=="'"):
                    pos=False
                    break
                else:
                    i1+=1
                    i2+=1
        else:
            i1+=1
        if(i2==sz2):
            break


    if(i1>=sz1 and i2<sz2):
        pos=False
    return pos


def helperFunction(func_TRUE,func_DC,Tchecker1,AllMappings):
    d = len(Tchecker1);
    func_TRUE = [];

    for j in Tchecker1:
        func_TRUE.append(j);

    if(d == 0):
        return AllMappings;

    Tchecker2 = dict();

    for i in range(0,d):
        j = 0;
        while(j < len(func_TRUE[i])):
            if(j == len(func_TRUE[i])-1):
                keyToCheck = func_TRUE[i] + "'";
                if keyToCheck in Tchecker1:
                    Tchecker2[func_TRUE[i][0:len(func_TRUE[i])-1]] = True;  #remove last element and set to true in the Tchecker2
                    Allminterms[func_TRUE[i][0:len(func_TRUE[i])-1]]=Allminterms[keyToCheck]+Allminterms[func_TRUE[i]]
                j+=1; #or equivalently, break
            else:
                #if we are not at the last element, we can check if the next string element is '
                if(func_TRUE[i][j+1] == "'"):
                    keyToCheck = func_TRUE[i][0:j+1] + func_TRUE[i][j+2:len(func_TRUE[i])];
                    if keyToCheck in  Tchecker1:
                        keynew = func_TRUE[i][0:j] + func_TRUE[i][j+2:len(func_TRUE[i])];
                        Tchecker2[keynew] = True;
                        Allminterms[keynew]=Allminterms[keyToCheck]+Allminterms[func_TRUE[i]]
                    j+=2;
                else:
                    keyToCheck = func_TRUE[i][0:j+1] + "'" + func_TRUE[i][j+1:len(func_TRUE[i])];
                    if keyToCheck in Tchecker1:
                        keynew = func_TRUE[i][0:j] + func_TRUE[i][j+1:len(func_TRUE[i])];
                        Tchecker2[keynew] = True;
                        Allminterms[keynew]=Allminterms[keyToCheck]+Allminterms[func_TRUE[i]]
                    j+=1;

    AllMappings.append(func_TRUE);
    return helperFunction(func_TRUE,func_DC,Tchecker2,AllMappings);



def comb_function_expansion(func_TRUE,func_DC):
    d = len(func_TRUE);#number of values that are true.
    if(d == 0):
        return [];
    func_TRUE = func_TRUE + func_DC; #we're combining the 2 lists, but since we have length of func_True=d, we are only using the loop till d
    n = len(func_TRUE[0]); #number of variables that we have.
    for i in range(0,len(func_TRUE[0])):
        if(func_TRUE[0][i] == "'"):
            n -= 1; #setting th number of values correctly, by not considering '; #verified that it's working correctly
    Tchecker1 = dict();

    for i in range(0,len(func_TRUE)):
        Tchecker1[func_TRUE[i]] = 1;
        lis=[]
        lis.append(func_TRUE[i])
        Allminterms[func_TRUE[i]]=lis

    Tchecker2 = dict(); # a level 2 checker, should store keys with string containing n-1 variables
    for i in range(0,d):
        j = 0;
        while(j < len(func_TRUE[i])):
            if(j == len(func_TRUE[i])-1):
                keyToCheck = func_TRUE[i] + "'";
                if keyToCheck in Tchecker1:
                    Tchecker2[func_TRUE[i][0:len(func_TRUE[i])-1]] = True; #remove last element and set to true in the Tchecker2
                    Allminterms[func_TRUE[i][0:len(func_TRUE[i])-1]]=Allminterms[keyToCheck]+Allminterms[func_TRUE[i]]
                j+=1; #or equivalently, break
            else:
                #if we are not at the last element, we can check if the next string element is '
                if(func_TRUE[i][j+1] == "'"):
                    keyToCheck = func_TRUE[i][0:j+1] + func_TRUE[i][j+2:len(func_TRUE[i])];
                    if keyToCheck in  Tchecker1:
                        keynew = func_TRUE[i][0:j] + func_TRUE[i][j+2:len(func_TRUE[i])];
                        Tchecker2[keynew] = True;
                        Allminterms[keynew]=Allminterms[keyToCheck]+Allminterms[func_TRUE[i]]
                    j+=2;
                else:
                    keyToCheck = func_TRUE[i][0:j+1] + "'" + func_TRUE[i][j+1:len(func_TRUE[i])];
                    if keyToCheck in Tchecker1:
                        keynew = func_TRUE[i][0:j] + func_TRUE[i][j+1:len(func_TRUE[i])];
                        Tchecker2[keynew] = True;
                        Allminterms[keynew]=Allminterms[keyToCheck]+Allminterms[func_TRUE[i]]
                    j+=1;
    AllMappings = [];

    T =  helperFunction([],func_DC,Tchecker2,AllMappings); #now T is the list.
    #now we check for each string if a particular element is a superstring of it
    answer = [];
    for i in range(0,d):
        termFound = False;
        for j in range(len(T)-1,-1,-1):
            for k in range(len(T[j])):
                #now check if it is a subset or not.
                
                if(checks2ins1(func_TRUE[i],T[j][k])):
                    termFound = True;
                    answer.append(T[j][k]);
                    break;
                
                    #if its not a substring, then a middle element must've been removed from
            if(termFound):
                break;
        if(termFound == False):
            answer.append(func_TRUE[i]); #since no minimization possible

    return answer;



# func_TRUE = ["a'b'c'd'e'", "a'b'cd'e", "a'b'cde'", "a'bc'd'e'",
# "a'bc'd'e", "a'bc'de", "a'bc'de'", "ab'c'd'e'", "ab'cd'e'"]
# func_DC = ["abc'd'e'", "abc'd'e", "abc'de", "abc'de'"]

# start=time.time()

# T = comb_function_expansion(func_TRUE,func_DC);

#DEMO
#For each of the answer our demo would give all the minterms which have formed it, so suppose the answer is ab then minterms that would 
#be outputted would be abcd, abcd',abc'd,abc'd'.

#print(T)

# inp=input("Enter an answer:")
# print(Allminterms[inp])

# end=time.time()
# print(end-start)


