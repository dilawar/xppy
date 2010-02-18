'''
Created on 22 Jul 2009

@author: Jakub Nowacki
'''
import os
import numpy as np

tmp_name = '__tmp__'
tmp_ode  = tmp_name+'.ode'
tmp_set  = tmp_name+'.set'

def change_ode(ode_file=tmp_ode, new_pars=[]):
    '''
    Function changes the parameters and initial conditions specified in
    new_pars in given ode_file. 
    '''
    print 'Warning! Function is obsolete, use changeOde instead!'
    changeOde(new_pars, ode_file)

def changeOde(new_pars, ode_file=tmp_ode):
    '''
    Function changes the parameters, initial conditions and options specified in
    new_pars in given ode_file. 
    '''
    # Copy the new_pars list
    pars = list(new_pars)
    # Check if the pars is a single list or list of lists
    if type(pars[0]) is not list:
        pars = [pars] # Make list of lists (for for loop below)
    # Reading the file
    # If file doesn't exist, Python throws exception by itself
    f = open(ode_file, 'r')
    lines = f.readlines()
    f.close()
    
    for line in lines[:]:
        # Check the type of the current line
        if line.find('par') == 0 or line.find('p ') == 0:
            tp = 'par'
        elif line.find('init') == 0 or line.find('i ') == 0:
            tp = 'init'
        elif line.find('@ ') == 0:
            tp = '@'
        # If it's not par, init or opt read next line
        else:
            continue
        
        # Go through the parameter array    
        for p in pars: 
            # Check only if the type of parameter matches the type of the line
            if p[0] == tp:
                i = line.find(p[1]+'=') # Find exact name followed by =
                if i == -1: # Parameter doesn't exist
                    continue
                t1 = line[:i+len(p[1])+1] # Read string up to =
                t2 = line[i+len(p[1])+1:] # Read string after =
                t2 = t2[t2.find(','):]    # Get rid of the old value
                # Adding the new line
                lines[lines.index(line)] = t1+str(p[2])+t2
                line = t1+str(p[2])+t2
                pars.pop(pars.index(p)) # Delete the changed parameter
    
    # Write file with new lines                    
    f = open(ode_file, 'w')
    f.writelines(lines)
    f.close()
            
def readOdePars(ode_file=tmp_ode, read_par=True, read_init=True, read_opt=True):
    '''
    Function reads the parameters and initial conditions  and options 
    from ode_file and returns parameters list. By default all the values 
    are read; the read of a specific type can be suppressed by changing
    the appropriate flag to False.
    '''
    # Reading the file
    # If file doesn't exist, Python throws exception by itself
    f = open(ode_file, 'r')
    lines = f.readlines()
    f.close()
    
    pars = []
    for line in lines[:]:
        # Check the type of the current line
        if read_par and (line.find('par') == 0 or line.find('p ') == 0):
            type = 'par'
        elif read_init and (line.find('init') == 0 or line.find('i ') == 0):
            type = 'init'
        elif read_opt and line.find('@ ') == 0:
            type = '@'
        # If it's not par or init read next line
        else:
            continue
        
        # For each parameter or initial condition
        for s in line[line.find(' ')+1:].split(','):
            s = s.strip()    # Get rid of spaces
            v = s.split('=') 
            # Save type, name and value
            pars.append([type, v[0], v[1]])
            
    return pars

def readOdeVars(ode_file=tmp_ode):
    '''
    Function reads the variables names from ode_file (including auxiliary 
    variables) and returns a data descriptor dictionary; the numbers represent
    columns in the output.dat file.
    '''
    # Reading the file
    # If file doesn't exist, Python throws exception by itself
    f = open(ode_file, 'r')
    lines = f.readlines()
    f.close()
    
    desc = [['time', 0], ['t', 0], [0, 'time']]; i = 1
    for line in lines[:]:
        # Check the type of the current line
        # skip comments
        if line.find('#') == 0:
            continue
        # dname/dt
        elif line.find('/dt') > 0:
            n = line[1:line.find('/dt')]
            desc.append([n,i]); desc.append([i,n]);  i += 1
        # name' or name(t+1)
        elif line.find("'") > 0:
            n = line[0:line.find("'")]
            desc.append([n,i]); desc.append([i,n]);  i += 1
        elif line.find('(t+1)') > 0:
            n = line[0:line.find('(t+1)')]
            desc.append([n,i]); desc.append([i,n]); i += 1
        # Auxiliary vars
        elif line.find('a') == 0:
            n = line[line.find(' ')+1:].split('=')[0].strip()
            desc.append([n,i]); desc.append([i,n]); i += 1
        else:
            continue
    
    return dict(desc)


def change_set(set_file, new_pars):
    '''
    Function changes the parameters and initial conditions specified in
    new_pars in given ode_file. 
    '''
    print 'Warning! Function is obsolete, use changeSet instead!'
    changeSet(new_pars, set_file)
   
def changeSet(new_pars, set_file=tmp_set):
    '''
    Function changes the parameters and initial conditions specified in
    new_pars in given ode_file. 
    '''
    # Copy the new_pars list
    pars = list(new_pars)
    # Check if the pars is a single list or list of lists
    if type(pars[0]) is not list:
        pars = [pars] # Make list of lists (for for loop below)
    # Reading the file
    # If file doesn't exist, Python throws exception by itself
    f = open(set_file, 'r')
    lines = f.readlines()
    f.close()
    
    tp = None
    for line in lines[:]: 
        # Check the type of the current line
        if line.find('# Parameters') == 0 and tp !='par':
            tp = 'par'
            continue
        elif line.find('# Old ICs') == 0 and tp != 'init':
            tp = 'init'
            continue
        # If it's not par or init read next line
        elif line.find('#') == 0 and (tp == 'par' or tp == 'init'): 
            tp = None
            continue
        
        if tp != 'par' and tp != 'init':
            continue     
        
        # Go through the parameter array    
        for p in pars: 
            # Check only if the type of parameter matches the type of the line
            if p[0] == tp:
                i = line.find(p[1]+os.linesep) # Find exact name
                if i == -1: # May be upper case?
                    tmp = p[1].upper()
                    i = line.find(tmp)
                    if i == -1: # Parameter doesn't exist
                        continue
                    p[1] = tmp
                # Adding the new line
                lines[lines.index(line)] = str(p[2])+'  '+p[1]+os.linesep   
                line = str(p[2])+'  '+p[1]+os.linesep  
                pars.pop(pars.index(p)) # Delete the changed parameter
    
    # Write file with new lines                    
    f = open(set_file, 'w')
    f.writelines(lines)
    f.close()
    
def readSetPars(set_file=tmp_set, read_par=True, read_init=True):
    '''
    Function reads the parameters and initial conditions
    from set_file and returns parameters list. By default all the values 
    are read; the read of a specific type can be suppressed by changing
    the appropriate flag to False.
    '''
    # Reading the file
    # If file doesn't exist, Python throws exception by itself
    f = open(set_file, 'r')
    lines = f.readlines()
    f.close()
    
    tp = None; pars = []
    for line in lines[:]: 
        # Check the type of the current line
        if read_par and line.find('# Parameters') == 0 and tp !='par':
            tp = 'par'
            continue
        elif read_init and line.find('# Old ICs') == 0 and tp != 'init':
            tp = 'init'
            continue
        # If it's not par or init read next line
        elif line.find('#') == 0 and (tp == 'par' or tp == 'init'): 
            tp = None
            continue
        
        if tp != 'par' and tp != 'init':
            continue     
        
        # Get rid of additional spaces or 
        l = line.strip(); l = l.strip(os.linesep)
        # Value and name are separated by a space
        v,n = l.split()
        # Initial conditions' var names are written in upper case
        if tp == 'init':
            n = n.lower()
        # Write the outcome
        pars.append([tp,n,v])
        
    return pars
       
def comparePars(pars1, pars2):
    '''
    Function compares two lists of parameters and returns the difference
    '''
    # Copy two lists into arrays
    p1 = np.array(pars1); p2 = np.array(pars2)
    
    dpars = []
    for tp in ['par', 'init']:
        # Create a dictionary with parameters or initial conditions name and value
        d1 = dict(p1[p1[:,0]==tp,1:])
        d2 = dict(p2[p2[:,0]==tp,1:])
        # Creating list of all keys
        keys = list(d1.keys())
        for v in d2.keys():
            try:
                keys.index(v)
            except ValueError:
                keys.append(v)
                
        # Comparing the dictionaries
        for k in keys:
            try:
                v1 = d1[k]
            except KeyError:
                v1 = None
            try:
                v2 = d2[k]
            except KeyError:
                v2 = None
            if v1 != v2:
                dpars.append([tp, k, v1, v2])
        
    return dpars
            
    