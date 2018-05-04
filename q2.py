import numpy
from nltk import RegexpTokenizer

def levenshtein(w1, w2, coef=2):
    w1_len = len(w1) + 1
    w2_len = len(w2) + 1
    distance = numpy.zeros(shape=(w1_len, w2_len))
    ptr = numpy.empty(shape=(w1_len, w2_len), dtype=numpy.str)
    #initialize
    for i in range(0, w1_len):
        distance[i][0] = i
    for i in range(0, w2_len):
        distance[0][i] = i
    
    for i in range(1, w1_len):
        for j in range(1, w2_len):
            if( w1[i-1] == w2[j-1]):
                _distance = {
                    'oblique': distance[i-1][j-1],
                    'down': distance[i-1][j] + 1,
                    'left': distance[i][j-1] + 1
                }
                distance[i, j] = min(
                    _distance.values()
                )
                ptr[i,j] = min(_distance, key=_distance.get)
            else:
                _distance = {
                    'oblique': distance[i-1][j-1] + coef,
                    'down': distance[i-1][j] + 1,
                    'left': distance[i][j-1] + 1
                    
                }
                distance[i, j] = min(
                    _distance.values()
                )
                ptr[i,j] = min(_distance, key=_distance.get)
    return {
        'distance': distance,
        'ptr': ptr
    }

with open('Dic.txt', 'r') as content_file:
    myDic = content_file.read()
    
with open('Test.txt', 'r') as content_file:
    myTest = content_file.read()

rt = RegexpTokenizer(r'\w+')

myDic = rt.tokenize(myDic)

myTest = rt.tokenize(myTest)
file = open('output01.txt', 'w+')
data = ""

for coef in [1, 1.5, 2]:
    data += "for "
    data += str(coef)
    data += "\n"
    for test_word in myTest:
        lenght_test = [levenshtein(i, test_word, coef).get('distance')[len(i), len(test_word)] for i in myDic]
        candidate_idx = min( (lenght_test[i], i) for i in range(0, len(lenght_test)) )
    
        print(test_word)
        data += test_word
        data += "\n"
    
        print(myDic[candidate_idx[1]])
        data += myDic[candidate_idx[1]]
        data += "\n"
    
        print("distance")
        data += "distance"
        data += "\n"
    
        print(levenshtein(myDic[candidate_idx[1]], test_word, coef).get('distance'))
        data += numpy.array2string(levenshtein(myDic[candidate_idx[1]], test_word, coef).get('distance'), separator=', ')
        data += "\n"
    
        print("back track pointer")
        data += "back track pointer"
        data += "\n"
    
        print(levenshtein(myDic[candidate_idx[1]], test_word).get('ptr'), coef)
        data += numpy.array2string(levenshtein(myDic[candidate_idx[1]], test_word, coef).get('ptr'), separator=', ')
        data += "\n"
    
        print()
        data += "\n"

file.write(data)
