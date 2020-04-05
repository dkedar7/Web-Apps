import numpy as np
import string
from nltk import word_tokenize
import onnxruntime as nxrun

def preprocess(text):
   tokens = word_tokenize(text)
   # split into lower-case word tokens, in numpy array with shape of (seq, 1)
   words = np.asarray([w.lower() for w in tokens]).reshape(-1, 1)
   # split words into chars, in numpy array with shape of (seq, 1, 1, 16)
   chars = [[c for c in t][:16] for t in tokens]
   chars = [cs+['']*(16-len(cs)) for cs in chars]
   chars = np.asarray(chars).reshape(-1, 1, 1, 16)
   return words, chars


sess = nxrun.InferenceSession("./bidaf.onnx")


def answer(context, query):

    cw, cc = preprocess(context)
    qw, qc = preprocess(query)
    
    answer = sess.run(None, 
                  {'context_word': cw,
                   'context_char': cc,
                   'query_word': qw,
                   'query_char': qc})
    
    answer = sess.run(None, 
                  {'context_word': cw,
                   'context_char': cc,
                   'query_word': qw,
                   'query_char': qc})
    
    # assuming answer contains the np arrays for start_pos/end_pos
    start = np.asscalar(answer[0])
    end = np.asscalar(answer[1])
    return (" ".join([w for w in cw[start:end+1].reshape(-1)]))