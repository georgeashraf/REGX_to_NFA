# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 08:20:46 2019

@author: Lenovo
"""

from collections import OrderedDict
import argparse
import os
import pydot
from IPython.display import Image, display

class Stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)
       
def infixToPostfix(infixexpr):
    prec = {}
    
    prec["("]=1
    prec["|"]=2
    prec["."]=3
    prec["?"]=4
    prec["*"]=5
    prec["+"]=6
    prec["^"]=7
    opStack = Stack()
    postfixList = []
    s_infix=''
    i=0
    for i in range(0,len(infixexpr)):
        c1=infixexpr[i]
        if i+1<len(infixexpr):
            c2=infixexpr[i+1]
            s_infix+=c1   
            if c1 is not"(" and c2 is not")" and c2 not in"|?+*^" and c1 not in"^|":
                s_infix+="."
    s_infix+=infixexpr[len(infixexpr)-1]            
    s_spaces=" ".join(s_infix)
    tokenList = s_spaces.split()
    #print(tokenList)

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZε" or token in "abcdefghijklmnopqrstuvwxyz" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)

def Regex2NFA(postfix):
    symbols_stack=Stack()
    exp_list=postfix.split()
    nfas=OrderedDict()
    
    for i in exp_list:
           if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or i in "abcdefghijklmnopqrstuvwxyz" or i in "0123456789" :
               symbols_stack.push(i)
               temp_states=[0,1]
               temp_alpha=[i]
               temp_start_state=0
               temp_final_state=1
               temp_transition=[(temp_start_state,i,temp_final_state)]
               nfas[i]=temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
               temp_states,temp_alpha,temp_transition=[],[],[]
           elif i =='ε':
               symbols_stack.push(i)
               temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition=epsilon_only()
               nfas[i]=temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
               temp_states,temp_alpha,temp_transition=[],[],[]
           elif i is  ".":
               s2=symbols_stack.pop()
               s1=symbols_stack.pop()
               s1_states,s1_alpha,s1_start,s1_final,s1_trans=nfas[s1]
               s2_states,s2_alpha,s2_start,s2_final,s2_trans=nfas[s2]
               temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transitions=concat_only(s1_states,s1_alpha,s1_start,s1_final,s1_trans,s2_states,s2_alpha,s2_start,s2_final,s2_trans)
               symbols_stack.push(s1+"."+s2)
               nfas[s1+"."+s2]=temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transitions
               temp_states,temp_alpha,temp_transition=[],[],[]
               
           elif i is "|":
               s2=symbols_stack.pop()
               s1=symbols_stack.pop() 
               s1_states,s1_alpha,s1_start,s1_final,s1_trans=nfas[s1]
               s2_states,s2_alpha,s2_start,s2_final,s2_trans=nfas[s2]
               temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition= union_only(s1_states,s1_alpha,s1_start,s1_final,s1_trans,s2_states,s2_alpha,s2_start,s2_final,s2_trans)
               symbols_stack.push(s1+"|"+s2)
               nfas[s1+"|"+s2]=temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
               temp_states,temp_alpha,temp_transition=[],[],[]
               
           elif i is "*":
               s1=symbols_stack.pop()
               s1_states,s1_alpha,s1_start,s1_final,s1_trans=nfas[s1]               
               temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition=star_only(s1_states,s1_alpha,s1_start,s1_final,s1_trans)
               symbols_stack.push(s1+"*")
               nfas[s1+"*"]=temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
               temp_states,temp_alpha,temp_transition=[],[],[]
               
           elif i is "+":
               s1=symbols_stack.pop()
               s1_states,s1_alpha,s1_start,s1_final,s1_trans=nfas[s1]
               s2_states,s2_alpha,s2_start,s2_final,s2_trans=s1_states,s1_alpha,s1_start,s1_final,s1_trans
               a,b,c,d,e=star_only(s1_states,s1_alpha,s1_start,s1_final,s1_trans)
               temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition=concat_only(s2_states,s2_alpha,s2_start,s2_final,s2_trans,a,b,c,d,e)
               nfas[s1+"+"]=temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
               symbols_stack.push(s1+"+")
               temp_states,temp_alpha,temp_transition=[],[],[]
               
           elif i is "?":
               s1=symbols_stack.pop()
               s1_states,s1_alpha,s1_start,s1_final,s1_trans=nfas[s1]
               a,b,c,d,e=epsilon_only()
               temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition=union_only(a,b,c,d,e,s1_states,s1_alpha,s1_start,s1_final,s1_trans)
               nfas[s1+"?"]=temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
               symbols_stack.push(s1+"?")
               temp_states,temp_alpha,temp_transition=[],[],[]
               
    return nfas

def write_output_file(nfas):
    output_file=open(args.file[:-4]+" result.txt","w+")
    states,alphabet,start,finish,transitions=(next(reversed(nfas.values()))) 
    print(states,alphabet,start,finish,transitions)
    for indx,val in enumerate(states):
        if indx<len(states)-1:
         output_file.write("q"+str(indx)+","+" ")
        else:
            output_file.write("q"+str(indx))
    output_file.write("\n") 
    
    alphabet=list(set(alphabet))
    for indx,val in enumerate(alphabet):
        if indx<len(alphabet)-1:
            if val!="epsilon":
                output_file.write(val+","+" ")
            else:
               output_file.write(" "+","+" ")
        else:
            if val != "epsilon":
              output_file.write(val)
            else:
               output_file.write(" ") 
    output_file.write("\n")    
    output_file.write('q'+str(start))
    output_file.write("\n")
    output_file.write('q'+str(finish))
    output_file.write("\n")
    for indx,i in enumerate(transitions):
        i=list(i)
        i[2]=['q'+str(i[2])]
        lst1 = map(str, i[2])
        line1 = ",".join(lst1)
        i[2]='['+line1+']'
        i[0]='q'+str(i[0])
        i=tuple(i)
        lst = map(str, i)
        line = ", ".join(lst)        
        if indx<len(transitions)-1:
          output_file.write(str('('+line+')'+','+" "))
        else:
            output_file.write(str('('+line+')'))
            
    return states,alphabet,start,finish,transitions        
            
def star_only(s1_states,s1_alpha,s1_start,s1_final,s1_trans): 
               s1_trans_f=[]
               s1_states_f=[]
               s1_states_f.append(0) 
               for i in s1_trans:
                   i=list(i)
                   i[0]=i[0]+1
                   i[2]=i[2]+1
                   i=tuple(i)
                   s1_trans_f.append(i)
               for i in s1_states:
                   i=i+1
                   s1_states_f.append(i)
               new_final=max(s1_states_f)+1    
               n1_trans=(0," ",s1_start+1)
               s1_trans_f=[n1_trans]+s1_trans_f
               p1_trans=(s1_final+1," ",s1_start+1)
               s1_trans_f=s1_trans_f+[p1_trans]
               f1_trans=(0," ",new_final)
               s1_trans_f=s1_trans_f+[f1_trans]
               l1_trans=(s1_final+1," ",new_final)
               s1_trans_f=s1_trans_f+[l1_trans]
               s1_states_f.append(new_final)
               temp_states=s1_states_f
               temp_alpha=s1_alpha
               temp_alpha.append('epsilon')
               temp_start_state=0
               temp_final_state=new_final
               temp_transition=s1_trans_f
               return temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
           
def concat_only(s1_states,s1_alpha,s1_start,s1_final,s1_trans,s2_states,s2_alpha,s2_start,s2_final,s2_trans):
               s2_trans_f=[]
               s2_states_f=[]
               m=s1_final
               x=s2_trans[0]
               connect_state=(s1_final,x[1],int(x[2])+m)               
               for i in s2_trans:
                   i=list(i)
                   i[0]=i[0]+m
                   i[2]=i[2]+m
                   i=tuple(i)
                   s2_trans_f.append(i)
               for i in s2_states:
                   i=i+m
                   s2_states_f.append(i)
               s2_trans_f[0]=connect_state
               temp_states=list(set().union(s1_states,s2_states_f))
               temp_alpha=list(set().union(s1_alpha,s2_alpha))
               temp_start_state=s1_start
               temp_final_state=s2_final+m
               temp_transition=s1_trans
               temp_transitions=temp_transition+s2_trans_f
               return temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transitions

def epsilon_only():
               temp_states=[0,1]
               temp_alpha=['epsilon']
               temp_start_state=0
               temp_final_state=1
               temp_transition=[(temp_start_state,' ',temp_final_state)] 
               return temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
           
def union_only(s1_states,s1_alpha,s1_start,s1_final,s1_trans,s2_states,s2_alpha,s2_start,s2_final,s2_trans):
               s1_trans_f=[]
               s2_trans_f=[]
               s1_states_f=[]
               s2_states_f=[]
               temp_states=[]
               s1_final=s1_final+1
               s2_final=s1_final+s2_final+1
               for i in s1_states:
                   i=i+1
                   s1_states_f.append(i)
               for i in s2_states:
                   i=i+s1_final+1
                   s2_states_f.append(i)
               new_final=1+len(s2_states)+len(s1_states)
               for i in s1_trans:
                   i=list(i)
                   i[0]=i[0]+1
                   i[2]=i[2]+1
                   i=tuple(i)
                   s1_trans_f.append(i)
               for i in s2_trans:
                   i=list(i)
                   i[0]=i[0]+s1_final+1
                   i[2]=i[2]+s1_final+1
                   i=tuple(i)
                   s2_trans_f.append(i)
               n1_trans=(0," ",s1_start+1)
               s1_trans_f=[n1_trans]+s1_trans_f
               n2_trans=(0," ",s1_final+s2_start+1)
               s2_trans_f=[n2_trans]+s2_trans_f
               f1_trans=(s1_final," ",new_final)
               f2_trans=(s2_final," ",new_final)
               s1_trans_f=s1_trans_f+[f1_trans]
               s2_trans_f=s2_trans_f+[f2_trans]
               temp_states.append(0)
               temp_states=temp_states+list(set().union(s1_states_f,s2_states_f))
               temp_states.append(new_final)
               temp_alpha=list(set().union(s1_alpha,s2_alpha))
               temp_start_state=0
               temp_final_state=new_final
               temp_transition=s1_trans_f+s2_trans_f
               return temp_states,temp_alpha,temp_start_state,temp_final_state,temp_transition
               
    
def visualize(states,alphabet,start,finish,transitions,name):
    G = pydot.Dot(graph_type="digraph")
    node = pydot.Node(start, style="filled", fillcolor="blue")
    G.add_node(node)
    for i in transitions:
        if i[1]==' ':
            label="epsilon"
        else:
            label=i[1]
        if i[2]==finish:
           node = pydot.Node(finish, style="filled", fillcolor="green")
           G.add_node(node)
           edge = pydot.Edge(i[0], node,label=label,labelfontcolor="#009933",fontsize="20.0")
           G.add_edge(edge)
           
        else:
            edge = pydot.Edge(i[0], i[2],label=label,labelfontcolor="#009933",fontsize="20.0")
            G.add_edge(edge)            
    im = Image(G.create_png())
    display(im)
    G.write_png(name[:-4]+".png")
if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')
    
    parser.add_argument('--file', action="store", help="path of file to take as input", nargs="?",
                            metavar="file")
    
    args = parser.parse_args()  
    

        
    post1=""
    with open(args.file, mode='r', encoding='utf-8-sig') as file:
                for line in file:
                    if line.isspace():
                        output_file=open(args.file[:-4]+" result.txt","w+")
                        output_file.write("oohhh what a surprise your input file is empty!!!")
                    else: 
                        post1+=line
                        post1=post1.replace(' ','')
                        post=infixToPostfix(post1)
                        #print(post)            
                        nfa=Regex2NFA(post)
                        states,alphabet,start,finish,transitions=write_output_file(nfa)
                        visualize(states,alphabet,start,finish,transitions,args.file)




