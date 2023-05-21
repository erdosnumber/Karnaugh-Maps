# import K_map_gui_tk;

# from operator import truediv
# import time


Allminterms=dict()
StringToInt=dict()


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


def stringtoint(s):

    n=len(s)
    pw=int(1)
    num=int(0)
    i=int(0)
    while(i<n):
        num+=pw
        if(i+1<n and s[i+1]=="'"):
            num-=pw
            i+=1
        pw*=2
        i+=1

    StringToInt[s]=num

def FrequencyOfMinterms(l,collected_minterms,contains_x):
    for i in range(len(l)):
        for j in range(len(Allminterms[l[i]])):
            mint=Allminterms[l[i]][j]
            if(not (mint in StringToInt)):
                stringtoint(mint)

            z=StringToInt[mint]
            if(contains_x[z]):
                continue
            else:
                collected_minterms[z]+=1


    

def RemoveCovered(l,allowed,collected_minterms,contains_x):
#l is the list of the answers from which we would get rid of some terms for optimal answer
#freq stores whether a minterm has been covered previously or not
    for i in range(len(l)):
        flag=False
        for j in range(len(Allminterms[l[i]])):
            z=StringToInt[Allminterms[l[i]][j]]

            if(contains_x[z]):
                continue
            elif(collected_minterms[z]==1):
                flag=True
                break
    
        allowed[i]=flag
        if(not flag):
            for j in range(len(Allminterms[l[i]])):
                z=StringToInt[Allminterms[l[i]][j]]
                if(contains_x[z]):
                    continue
                collected_minterms[z]-=1


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

    Allminterms.clear()
    StringToInt.clear()

    d = len(func_TRUE);#number of values that are true.
    if(d == 0):
        return [];
    func_TRUE = func_TRUE + func_DC; #we're combining the 2 lists, but since we have length of func_True=d, we are only using the loop till d
    n = len(func_TRUE[0]); #number of variables that we have. 

    # while(exp<n):
    #     pw*=2
    #     exp+=1

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
    for i in range(0,len(func_TRUE)):
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

    # print(answer)
    
    ans=set()
    for i in range(len(answer)):
        ans.add(answer[i])
 
    answer.clear()
    answer=list(ans)

    collectedMinterms = [int(0)]*(2**n);
    containsX = [False]*(2**n);
    for minterm in func_DC:
        stringtoint(minterm)
        containsX[StringToInt[minterm]] = True;
    Allowed = [True]*(len(answer));

    FrequencyOfMinterms(answer,collectedMinterms,containsX)
    RemoveCovered(answer,Allowed,collectedMinterms,containsX);
    finalList = [];
    removed=[]
    for i in range(0,len(answer)): 
        if(Allowed[i] == True):
            finalList.append(answer[i]);
        else:
            removed.append(answer[i])


 #DEMO STARTS FROM HERE
 #DEMO STARTS FROM HERE
 #DEMO STARTS FROM HERE  

    # print(answer)
    # for i in range(len(removed)):
    #     print("Term Removed: ",removed[i])
    #     print("It contains the following minterms:")
    #     for j in range(len(Allminterms[removed[i]])):
    #         minn=Allminterms[removed[i]][j]
    #         if(containsX[StringToInt[minn]]):
    #             print("Non-essential:",minn)

    #         for k in range(len(finalList)):
    #             if(checks2ins1(minn,finalList[k])):
    #                 print("Essential:",minn,"is already covered by:",finalList[k])
    #                 break
    #     print("\n")

#DEMO ENDS HERE
#DEMO ENDS HERE
#DEMO ENDS HERE


    return finalList


func_TRUE=["a'b'c'd'","a'b'cd'","ab'c'd","ab'cd"]
func_DC=["a'b'c'd","a'bc'd'","a'bc'd","abcd","abcd'","ab'cd'"]


print(comb_function_expansion(func_TRUE,func_DC))

#Testcases for Assignment 3 report

#testcases in which we are having func_DC as none and rejection of a term happens if it is covered entirely by other terms
# func_TRUE = ["abc'd'","abc'd","ab'c'd'","ab'c'd","abcd","abcd'","a'bcd","a'bcd'"]
# func_TRUE = ["a'b'c'd","a'b'cd","a'bc'd","a'bcd","abc'd'","abc'd"]
# func_TRUE = ["a'b'c'd","a'b'cd","a'bc'd","a'bcd","abc'd'","abc'd","a'b'c'd'","a'bc'd'","ab'c'd'"]

#testcases in which rejection of a term happens if it is not covered entirely by other terms but the the uncovered minterms contain x

# func_TRUE=["abc'd'","abc'd","ab'c'd'","ab'c'd","a'bcd'","abcd'"]
# func_DC=["abcd"]

# func_TRUE=["a'bc'd","a'bcd","a'bcd'","a'b'c'd"]
# func_DC=["abc'd","abcd"]

#func_TRUE=["a'b'c'd'","a'b'cd'","ab'c'd","ab'cd"]
#func_DC=["a'b'c'd","a'bc'd'","a'bc'd","abcd","abcd'","ab'cd'"]

