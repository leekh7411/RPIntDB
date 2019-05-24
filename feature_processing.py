#!/usr/bin/python3 
from hyperparams import *
from rawdata_preprocessing import read_RPI_pairSeq, read_NPInter_pairSeq
from copy import deepcopy
import numpy as np

isPrint = True

# Reduced Protein letters(7 letters)
def get_reduced_protein_letter_dict():
    rpdict = {}
    reduced_letters = [["A","G","V"],
                       ["I","L","F","P"],
                       ["Y","M","T","S"],
                       ["H","N","Q","W"],
                       ["R","K"],
                       ["D","E"],
                       ["C"]]
    changed_letter = ["A","B","C","D","E","F","G"]
    for class_idx, class_letters in enumerate(reduced_letters):
        for letter in class_letters:
            rpdict[letter] = changed_letter[class_idx]
    
    return rpdict

# Improved CTF 
class improvedCTF:
    def __init__(self, letters, length):
        self.letters = letters
        self.length = length
        self.dict = {}
        self.generate_feature_dict()
        
    def generate_feature_dict(self):
        def generate(cur_key, depth):
            if depth == self.length:
                return
            for k in self.letters:
                next_key = cur_key + k
                self.dict[next_key] = 0
                generate(next_key, depth+1)
                
        generate(cur_key="",depth=0)
        
        if isPrint:
            print("iterate letters : {}".format(self.letters))
            print("number of keys  : {}".format(len(self.dict.keys())))
        
    
    def get_feature_dict(self):
        for k in self.dict.keys():
            self.dict[k] = 0
            
        return deepcopy(self.dict)

    
# CTF feature processing
def preprocess_feature(x, y, npz_path):
    
    def min_max_norm(a):
        a_min = np.min(a)
        a_max = np.max(a)
        return (a - a_min)/(a_max - a_min)
    
    rpdict = get_reduced_protein_letter_dict()
    feature_x = []
    r_mer = 4
    r_CTF = improvedCTF(letters=["A","C","G","U"],length=r_mer)
    #r_feature_dict = r_CTF.get_feature_dict()
    
    p_mer = 3
    p_CTF = improvedCTF(letters=["A","B","C","D","E","F","G"],length=p_mer)
    #p_feature_dict = p_CTF.get_feature_dict()
    
    x_protein = []
    x_rna = []
        
    for idx, (pseq, rseq) in enumerate(x):
        
        r_feature_dict = r_CTF.get_feature_dict()
        p_feature_dict = p_CTF.get_feature_dict()
        rpseq = []
        for p in pseq:
            if p=="X": 
                rpseq.append(p)
            else:
                rpseq.append(rpdict[p])
                
        pseq = rpseq
        temp_pseq = ""
        for p in pseq:
            temp_pseq += p
        pseq = temp_pseq
        
        for mer in range(1,p_mer+1):
            for i in range(0,len(pseq)-mer):
                pattern = pseq[i:i+mer]
                try:
                    p_feature_dict[pattern] += 1
                except:
                    continue
                #print(pattern)
        
        for mer in range(1,r_mer+1):
            for i in range(0,len(rseq)-mer):
                pattern = rseq[i:i+mer]
                try:
                    r_feature_dict[pattern] += 1
                except:
                    continue
                #print(pattern)
        
        
        
        p_feature = np.array(list(p_feature_dict.values()))
        p_feature = min_max_norm(p_feature)
        
        r_feature = np.array(list(r_feature_dict.values()))
        r_feature = min_max_norm(r_feature)
        
        x_protein.append(p_feature)
        x_rna.append(r_feature)
        
        if isPrint : 
            print("CTF preprocessing ({} / {})".format(idx+1, len(x)))
            #print(r_feature)
            
                
    
    x_protein = np.array(x_protein)
    x_rna = np.array(x_rna)
    y = np.array(y)
    np.savez(npz_path,XP=x_protein, XR=x_rna, Y=y)
    
    if isPrint :
        print("Protein feature : {}".format(x_protein.shape))
        print("RNA feature     : {}".format(x_rna.shape))
        print("Labels          : {}".format(y.shape))
        print("Saved path      : {}".format(npz_path))
    
     
    return x_protein, x_rna, y

def preprocess_and_savez_NPInter():
    X, Y = read_NPInter_pairSeq()
    XP, XR, Y = preprocess_feature(X, Y, NPZ_PATH["NPInter"])
    
def preprocess_and_savez_RPI(size):
    X, Y = read_RPI_pairSeq(size)
    XP, XR, Y = preprocess_feature(X, Y, NPZ_PATH["RPI"][size])

if __name__ == "__main__":
    print("Feature Preprocessing")
    preprocess_and_savez_NPInter()
    preprocess_and_savez_RPI(1807)
    preprocess_and_savez_RPI(2241)
    preprocess_and_savez_RPI(369)
    preprocess_and_savez_RPI(488)
    
    
    
    