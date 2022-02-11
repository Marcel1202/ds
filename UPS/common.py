from matplotlib import image
import numpy as np
import pickle

#database=[[Names],[[username,password]],[[vector images for first one],[vector images for second one]],[drinks]]
#            0              1                                           2                                   3



def read_pickle_to_database(file_path):
    with open(file_path,'r') as f:
        database=pickle.load(f)
    return database

def compare_image_to_database(database,image_vector_list):
    images_vectors=np.array(database[2])
    image_vector=np.array(image_vector_list)

    min_distances=np.zeros((len(database[0]),))


    for i,array in enumerate(images_vectors):
        min_distances[i]=np.min(np.sqrt(np.sum((array-image_vector)**2,axis=1)))
    min_distance=np.min(min_distances)
    pos=np.argmin(min_distances)

    if min_distance<0.45:
        return database[0][pos],database[3][pos]
        #name, drink
    else:
        return 0

    

def compare_user_pass_to_database(database,username,password):
    list_user_pass=database[1]
    try:
        pos=list_user_pass.index([username,password])
        return database[0][pos],database[3][pos]
    except ValueError:
        return 0



#database=[['Albi','Geri'],[['albi','pass'],['geri','pass']],[[[1,2,3],[4,5,6],[7,8,9]],[[1,0,1],[0,1,0],[1,0,0]]],['water','beer']]
#c=[0,1,0]


#ret=compare_user_pass_to_database(database,'albi','pass')
#print(ret)

#ret=compare_image_to_database(database,c)
#print(ret)