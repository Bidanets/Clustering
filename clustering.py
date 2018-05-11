from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import os
from parser import Parser
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist
from scipy.cluster import hierarchy
import numpy as np

def hierarchy_draw(Z, labels, level):
        """Рисуем дендрограмму и сохраняем её"""
        plt.figure()
        hierarchy.dendrogram(Z, labels = labels, color_threshold = level,
                             leaf_font_size = 10, count_sort = True)
        plt.rcParams["figure.figsize"] = (20, 25) 
        plt.show()

dir_path = 'Wiki-documents/'

print('Preprocessing of texts...')
        
corpus_of_texts = []

parser = Parser()

directories = [x[0] for x in os.walk(dir_path)]
directories = directories[1:]

file_names = []

y = []
k = 1
for i in range(len(directories)):
    for file in os.listdir(directories[i] + '/'):
        if file.endswith(".txt"):
            file_name = os.path.join(directories[i] + "/", file)
            print(file_name)
            y.append(k)
            file_names.append(file[:-4])
            text = parser.text_preprocessing(file_name)
            corpus_of_texts.append(text)
            
    k += 1
            

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus_of_texts)

lsa = TruncatedSVD(n_components = 2, algorithm = "arpack")

X = lsa.fit_transform(X)

plt.plot(X[:, 0], X[:, 1], 'ro', markersize = 2.0)

plt.show()

dist = pdist(X, 'cosine')
Z = hierarchy.linkage(dist, method='average')

print(Z)
print(len(file_names))
"""
def check(c):
    C = hierarchy.fcluster(Z, t = c)  
    if len(set(C)) <= 3:
        return True
    return False


def bs(l, r, EPS):  
    l = np.float128(l)
    r = np.float128(r)
    
    
    while (l < r):
        c = (l+r)/2
        print(c)
        if check(c) == True:
            r = c
        else:
            l = c + EPS
            
    return l

    
t = bs(1, 1.16, EPS = 1E-18)
"""
C = hierarchy.fcluster(Z, t = 3, criterion = 'maxclust')
hierarchy_draw(Z = Z, labels = file_names, level = 0.1)

Q = 0.0
for i in range(len(y)):
    for j in range(i+1, len(y)):
        if y[i] == y[j] and C[i] == C[j]:
            Q += 1
        if y[i] != y[j] and C[i] != C[j]:
            Q += 1
       
Q /= len(y)*(len(y)-1)/2
        
print('Quality (from 0 to 1):', Q)