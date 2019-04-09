import numpy as np



def embedding_matrix(path_to_embedding : str,embedding_dim: int, word_index : dict) -> np.array:
    """
    This function creates an embedding matrix.
    
    Inputs:
    path_to_embedding - path to text file of word embeddings
    embedding_dim - dimension of word embeddings
    word_index - dictionary mapping words to indices
    
    Outputs:
    embedding_matrix - numpy matrix containing the embeddings
    
    """
    embeddings_index = {}
    f = open(path_to_embedding, encoding='utf-8')
    for line in f:
        try:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        except:
            pass
        
    f.close()

    embedding_matrix = np.zeros((len(word_index) + 1,embedding_dim))
    found = 0
    for word, i in word_index.items():
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            # words not found in embedding index will be all-zeros.
            found +=1
            embedding_matrix[i] = embedding_vector

    return embedding_matrix

