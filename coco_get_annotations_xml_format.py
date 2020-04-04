 

import os
import sys
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import pickle
import cv2
import json

def write_to_xml(image_name, image_dict, data_folder, save_folder, xml_template='pascal_voc_template.xml'):
    
    
    # get bboxes
    bboxes = image_dict[image_name]
    
    # read xml file
    tree = ET.parse(xml_template)
    root = tree.getroot()    
    
    # modify
    folder = root.find('folder')
    folder.text = 'Annotations'
    
    fname = root.find('filename')
    fname.text = image_name 
    
    src = root.find('source')
    database = src.find('database')
    database.text = 'COCO2017'
    
    
    # size
    img = cv2.imread(os.path.join(data_folder, image_name))
    h,w,d = img.shape
    
    size = root.find('size')
    width = size.find('width')
    width.text = str(w)
    height = size.find('height')
    height.text = str(h)
    depth = size.find('depth')
    depth.text = str(d)
    
    for box in bboxes:
        # append object
        obj = ET.SubElement(root, 'object')
        
        name = ET.SubElement(obj, 'name')
        name.text = box[0]
        
        pose = ET.SubElement(obj, 'pose')
        pose.text = 'Unspecified'

        truncated = ET.SubElement(obj, 'truncated')
        truncated.text = str(0)

        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = str(0)

        bndbox = ET.SubElement(obj, 'bndbox')
        
        xmin = ET.SubElement(bndbox, 'xmin')
        xmin.text = str(int(box[1]))
        
        ymin = ET.SubElement(bndbox, 'ymin')
        ymin.text = str(int(box[2]))
        
        xmax = ET.SubElement(bndbox, 'xmax')
        xmax.text = str(int(box[3]))
        
        ymax = ET.SubElement(bndbox, 'ymax')
        ymax.text = str(int(box[4]))
    
    # save .xml to anno_path
    anno_path = os.path.join(save_folder, image_name.split('.')[0] + '.xml')
    print(anno_path)
    tree.write(anno_path)
    

# main routine
if __name__=='__main__':
    
    # read annotations file
    annotations_path = 'instances_val2017.json'
    
    # read coco category list
    df = pd.read_csv('coco_categories.csv')
    df.set_index('id', inplace=True)
    
    # specify image locations
    image_folder = 'val2017'
    
    # specify savepath - where to save .xml files
    savepath = 'saved'
    if not os.path.exists(savepath):
        os.makedirs(savepath)
    
    # read in .json format
    with open(annotations_path,'rb') as file:
        doc = json.load(file)
        
    # get annotations
    annotations = doc['annotations']
    
    # iscrowd allowed? 1 for ok, else set to 0
    iscrowd_allowed = 1
    
    # initialize dict to store bboxes for each image
    image_dict = {}
    
    # loop through the annotations in the subset
    for anno in annotations:
        # get annotation for image name
        image_id = anno['image_id']
        image_name = '{0:012d}.jpg'.format(image_id)    
        
        # get category
        category = df.loc[anno['category_id']]['name']
        
        # add as a key to image_dict
        if not image_name in image_dict.keys():
            image_dict[image_name]=[]
        
        # append bounding boxes to it
        box = anno['bbox']
        # since bboxes = [xmin, ymin, width, height]:
        image_dict[image_name].append([category, box[0], box[1], box[0]+box[2], box[1]+box[3]])
        
    # generate .xml files
    for image_name in image_dict.keys():
        write_to_xml(image_name, image_dict, image_folder, savepath)
        print('generated for: ', image_name)