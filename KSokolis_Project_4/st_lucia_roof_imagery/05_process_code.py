
# coding: utf-8

# In[18]:


# setting paths
source_image_path = input('Copy in file path for St. Lucia tif file')
buildings_shapefile_path = input('Copy in file path for St. Lucia buildings shapefile')
buildings_csv_path = input('Copy in file path for St. Lucia buildings csv')


# In[19]:


import numpy as np
import pandas as pd
import json

import rasterio as rio
from rasterio.plot import show
from rasterio.mask import mask
import geopandas as gpd
import pysal as ps
import shapely
from shapely.geometry import *
import pyproj
from fiona.crs import from_epsg

from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping
from keras.models import load_model
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score


# In[20]:


img = rio.open(source_image_path)


# In[21]:


img_bbox = box(img.bounds.left, img.bounds.bottom, img.bounds.right, img.bounds.top)


# In[22]:


# loading in building data as a shapefile
buildings_shp = ps.open(buildings_shapefile_path)
buildings_df = pd.read_csv(buildings_csv_path)


# In[23]:


# p converts lat long coordinates to UTM 20 xy coordinates (meters)
p = pyproj.Proj(proj='utm', zone=20)


# In[24]:


# converting all building bounding boxes in the Dennery district into a format that can
# be by rasterio to cut out buildings (). The result is an iterable list

# initalizing the building list
bbox_list = []
OID_list = []

for i in range(len(buildings_shp)):
    #setting coords equal to the bounding box of each building
    coords = buildings_shp[i].bbox
    
    # converting the corrdinates of the bounding box to UTM 20 xy coordinates
    bbox = box(p(coords[0], coords[1])[0],
               p(coords[0], coords[1])[1],
               p(coords[2], coords[3])[0],
               p(coords[2], coords[3])[1])
    
    # using images bounding box as a filter
    if img_bbox.contains(bbox.centroid):
        # coverting the bounding box to a dataframe with the bounding box as the geometry
        gdf = gpd.GeoDataFrame({'geometry': bbox},
                                index = [0],
                                crs=from_epsg(32620))
        
        OID_list.append(buildings_df.iloc[i].OID_)
        
    
        # appending the bounding box in a json format that can be easily used by rasterio
        bbox_list.append([json.loads(gdf.to_json())['features'][0]['geometry']])


# In[25]:


get_ipython().system('rm -r roof_dump; mkdir roof_dump')
get_ipython().system('mkdir roof_dump/images')


# In[26]:


# iterating through all the bounding boxes for buildings within the filter and cropping
# the drone data with those bounding boxes and saving the images to a specified folder

for i in range(len(bbox_list)):
    # using try accept in case the centroid of a building is in the specified filter but 
    # at least one vertice is out of bounds 
    try:
        # this will error if part of the bounding box is out of bounds
        out_img, out_transform = mask(dataset=img, shapes=bbox_list[i], crop=True)
        # copying meta data from original raster and seting epsg code
        out_meta = img.meta.copy()
        epsg_code = int(img.crs.data['init'][5:])
        # updating the meta data
        out_meta.update({"driver": "jpeg",
                     "height": out_img.shape[1],
                     "width": out_img.shape[2],
                     "transform": out_transform}
                   )
        # writing images to file path with the OIR in the image name
        with rio.open(f"roof_dump/images/building_{OID_list[i]}.jpeg", "w", **out_meta) as dest:
            dest.write(out_img)  
            
    except:
        # prints the OID for any image that errors
        print(f"bounding box {OID_list[i]} produced an error")
        # skipping over the bounding box
        pass


# In[27]:


get_ipython().system('rm ./roof_dump/images/*.xml')


# In[28]:


cnn = load_model('./pickled_models/categorical_model.h5')


# In[29]:


trial_generator = ImageDataGenerator(rescale=1/255)

trial_set =  trial_generator.flow_from_directory('./roof_dump/',
                                                 target_size=(150, 150),
                                                 shuffle = False)


# In[30]:


y_pred = cnn.predict_generator(trial_set, len(trial_set)) > .5
y_pred = [1 if i[0] else 0 for i in y_pred]


# In[31]:


oid_filters = []

for i in range(len(y_pred)):
    if y_pred[i] == 0:
        oid_filters.append(trial_set.filenames[i].split('_')[-1].split('.')[0])


# In[32]:


index_lst = []

for i in range(len(buildings_df.OID_)):
    if str(buildings_df.OID_[i]) in oid_filters:
        index_lst.append(i)


# In[33]:


poor_buildings = buildings_df.iloc[index_lst, :]


# In[34]:


poor_buildings.to_csv('./poor_quality_roofs.csv')

