# coco-annotations-to-xml
Convert COCO annotations to xml format 

 
COCO is a well-known detection dataset:
http://cocodataset.org/

Overview:
*********

Annotation files are provided for train and validation images for COCO. These are in the form of .json files - 'JavaScript Object Notation' format- the information is in the form of key-value pairs, and if you are familiar with Python, you might recognize this as having a similar format to that of a Python dictionary.

Procedure:
**********

Annotations are read after the .json file is loaded. 
There are several annotations present, and it is important to note that each annotation doesn't correspond necessarily to one image, but to one object. This object again could be a single object, or an amalgamation of objects (in this case, the attribute 'iscrowd' is set to one). 
This code is agnostic to the 'iscrowd' parameter- but you might want to change this depending on your use-case.
Xml files are generated for each image, after the annotations are pooled. 

Why is this useful:
*******************

Several reasons.
-> You might want to train a detector like Yolov2, which uses .xml files
-> You might want to visualize annotations using tools like labelImg, which use .xml files
-> You might just want to do this for fun, and improve your Python skills :-)
