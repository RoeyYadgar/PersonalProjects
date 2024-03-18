import numpy as np

N = 40


def switchStringLanguage(string):
    
    global N 
    
    english_letters = 'qwertyuiop[{]}asdfghjkl;:\'"\\zxcvbnm,<.>/? '
    hebrew_letters = '/\'קראטוןםפ]}[{שדגכעיחלךף:,"\\זסבהנמצת>ץ<.? '
    
    english_trans = [english_letters.find(c.lower()) for c in string[:N]]
    hebrew_trans = [hebrew_letters.find(c.lower()) for c in string[:N]]
    
    if(english_trans.count(-1) <= hebrew_trans.count(-1)):
        trans = english_trans
        letters = hebrew_letters
    else:
        trans = hebrew_trans
        letters = english_letters
        
    l= len(trans)
    
    if(l < N):
        trans[l:N] = [-2 for i in range(N-l)]
        
    return convertArrToString(trans, letters, string)
    
      
def convertStringToArr(string):
    
    global N

    english_letters = 'qwertyuiop[{]}asdfghjkl;:\'"\\zxcvbnm,<.>/? '
    hebrew_letters = '/\'קראטוןםפ]}[{שדגכעיחלךף:,"\\זסבהנמצת>ץ<.? '

    english_trans = [english_letters.find(c.lower()) for c in string[:N]]
    hebrew_trans = [hebrew_letters.find(c.lower()) for c in string[:N]]


    if(english_trans.count(-1) <= hebrew_trans.count(-1)):
        trans = english_trans
    else:
        trans = hebrew_trans
        
    l= len(trans)
    
    if(l < N):
        trans[l:N] = [-2 for i in range(N-l)]


    return np.reshape(np.array(trans),(1,N))

def convertArrToString(arr,letters,original_string):
    global N    
      
    string = ['0' for i in range(N)]
    for i in range(N):
        c = arr[i]
        if(c >= 0):
            string[i] = letters[c]
        elif(c == -1):
            string[i] = original_string[i]
        else:
            string[i] = ""
    
    return ''.join(string)

