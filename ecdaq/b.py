from a  import x,l

def f(v):
    global x,l
    l['1']='abc'
    x=100

f(11)    
print x  
print l['1']  