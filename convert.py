#coding:utf-8
import argparse
from copy import deepcopy
BASE_NUM=7

class unit():
    def __init__(self,name="None",symbol="",unit_symbol="",dim=[0]*BASE_NUM,sign="*"):
        self.name=name
        self.dim=dim
        self.unit_symbol=unit_symbol
        self.symbol=symbol
        self.sign=sign
    def minus(self):
        return unit(self.name,self.symbol,self.unit_symbol,sub([0]*BASE_NUM,self.dim),"-")
def summarize_lists(lists):
    ret=[0 for _ in range(BASE_NUM)]
    for l in lists:
        for i in range(len(l)):
            ret[i]+=l[i]
    return ret

def sub(a,b):
    return [i-j for i,j in zip(a[:],b[:])]
class search():
    def __init__(self,limit_max,limit_min):
        self.limit_max=limit_max
        self.limit_min=limit_min
        self.index=self.limit_min[:] # don't forget putting [:] last (make deepcopy)
        self.space={repr([0]*BASE_NUM):[]}

    def next_index(self): # this function returns if index was resetted.
        for i in range(BASE_NUM):
            self.index[i]+=1
            if self.index[i]>self.limit_max[i]:
                self.index[i]=self.limit_min[i]
            else :
                break
        else:
            return False # index was resetted.
        return True # nope.
    def update_space(self,try_unit):
        is_counting=True
        is_updated=False
        while is_counting:
            key=repr(sub(self.index,try_unit.dim))
            if key in self.space and ( repr(self.index) not in self.space or key==[0]*BASE_NUM ):
                self.space.update({repr(self.index):self.space[key]+[try_unit]})
                is_updated=True
            is_counting=self.next_index()
        return is_updated
def find_cmb(targets,inputs):
    minused=[unit(i.name,i.symbol,i.unit_symbol,sub([0]*BASE_NUM,i.dim),"/") for i in inputs[:]]
    inputs+=minused
    target_list=summarize_lists([t.dim for t in targets[:]])
    limit_max=[max([i.dim for i in inputs[:]]+[target_list],key=lambda x: x[i])[i] for i in range(BASE_NUM)]
    limit_min=[min([i.dim for i in inputs[:]]+[target_list],key=lambda x: x[i])[i] for i in range(BASE_NUM)]
    s=search(limit_max,limit_min)

    is_updated_once=True
    while is_updated_once:
        is_updated_once=False
        for try_unit in inputs:
            if s.update_space(try_unit):
                is_updated_once=True

    if repr(target_list) in s.space:
        return [targets,s.space[repr(target_list)]]
    else:
        return False


def show_cmb(formula_data):
    targets,parts=formula_data
    formula=False
    left_side="".join([x.unit_symbol if formula else x.symbol for x in targets])
    times=dict()
    divs=dict()
    for part in parts:
        if part.sign=="*":
            if part.unit_symbol if formula else part.symbol  not in times:
                times.update({part.unit_symbol if formula else part.symbol:1})
            else:
                times[part.unit_symbol if formula else part.symbol]+=1
        else:
            if part.unit_symbol if formula else part.symbol not in divs:
                divs.update({part.unit_symbol if formula else part.symbol:1})
            else:
                divs[part.unit_symbol if formula else part.symbol]+=1
    time_str="*".join(["%s%s"%(t[0],"" if t[1]==1 else "^"+str(t[1])) for t in times.items()])
    div_str="*".join(["%s%s"%(d[0], "^"+str(-d[1])) for d in divs.items()])
    print(time_str+("*" if time_str!="" and div_str!="" else "") +div_str)
def main():

    parser=argparse.ArgumentParser()
    parser.add_argument("target_unit")
    parser.add_argument("use_units")

    args=parser.parse_args()
    ##[meter,kilogram,second,ampere,kelvin,candera,mole]
    units={
    "m":unit("meter","m","l",[1,0,0,0,0,0,0]),
    "kg":unit("kilogram","kg","m",[0,1,0,0,0,0,0]),
    "s":unit("second","s","t",[0,0,1,0,0,0,0]),
    "A":unit("ampere","A","I",[0,0,0,1,0,0,0]),
    "K":unit("kelvin","K","T",[0,0,0,0,1,0,0]),
    "cd":unit("candera","cd","Iv",[0,0,0,0,0,1,0]),
    "mol":unit("mole","mol","n",[0,0,0,0,0,0,1]),
    "v":unit("velocity","v","v",[1,0,-1,0,0,0,0]),
    "a":unit("accerelation","a","a",[1,0,-2,0,0,0,0]),
    "N":unit("newtom","N","F",[1,1,-2,0,0,0,0]),
    "J":unit("joule","J","Q",[2,1,-2,0,0,0,0]),
    "W":unit("watt","W",u"φ",[2,1,-3,0,0,0,0]),
    "C":unit("coulomb","C","q",[0,0,1,1,0,0,0]),
    "Pa":unit("pascal","Pa","p",[-1,1,-2,0,0,0,0]),
    "V":unit("volt","V","V",[2,1,-3,-1,0,0,0]),
    "F":unit("farad","F","C",[-2,1,4,2,0,0,0])
    }
    inputs=[]
    targets=[]
    tokens=args.target_unit.split("*")
    for token in tokens:
        if "^" in token:
            symbol,exp=token.split("^")
        else:
            symbol,exp=token,1
        unt=units[symbol]
        if int(exp) <0:
            unt=unt.minus()
        for _ in range(abs(int(exp))):
            targets.append(deepcopy(unt))



    ins=args.use_units.split(",")
    for symbol in units:
        if symbol in ins:
            inputs.append(units[symbol])
    f=find_cmb(targets,inputs)
    if f:
        show_cmb(f)
    else:
        print("Combination not found.")
    #show_formula([N],f)
if __name__ == '__main__':
    main()
