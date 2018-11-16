import zipfile
import os
from shutil import copy2
from shutil import copyfileobj
import tarfile
import gzip
import zlib
import untangle
import xml.etree.ElementTree as ET
from MidiTrack import *


class ALS_Reader:

    def __init__(self):
        self.tree = None
        self.als_root = None #Type: xml Tree
        self.als_list = None
        self.temp = []
        self.adress = None #folder of .file
        self.filename = None
        self.xml_data = None


    def scan(self, filepath):
        path = filepath[:-(len(filename)+4)]
        filename = filepath.split("/")[-1].split(".")[0]
        self.filename = filename
        self.adress =path

        #Renaming .als file
        gz_file = path + "/" + filename + ".gz"
        copy2(filepath, gz_file)



        #Extracting file
        xml_file = path + "/" + filename + ".xml" #new destination of xml file

        with gzip.open(gz_file, 'rb') as f_in:
            with open(xml_file, 'wb') as f_out:
                copyfileobj(f_in, f_out)
                self.xml_data = f_out

        os.remove(gz_file)        #Deleting gz


        tree = ET.parse(xml_file)
        os.remove(xml_file)        #Deleting xml

        self.tree = tree

        self.als_root = tree.getroot()



    def write(self, tree = None):
        if (tree == None):
            tree = self.tree

        xml_file = self.adress + self.filename + "_re.xml"

        tree.write(xml_file , encoding='utf-8', xml_declaration=True) # writing xml file to adress

        #Compressing .xml file

        with open(xml_file, 'rb') as f_in:
            with gzip.open(self.adress+ self.filename +".gz", 'wb') as f_out:
                copyfileobj(f_in, f_out)



        #Renaming .gz file

        copy2(self.adress + self.filename + ".gz", self.adress + self.filename + "_re.als")
        os.remove(self.adress + self.filename + ".gz")
        #os.remove(self.adress + self.filename + "_re.xml")


    def add_midi_track(self, pos, root = None ):
        if (root == None):
            root = self.als_root
        for child in root:
            if (child.tag == "Tracks"):

                track = MidiTrack()
                child.insert(pos, track.tree)
            else:
                self.add_midi_track(pos, root = child)






    def to_list(self, root):
        list = []
        for child in root:
            list.append(child) # .append(self.to_list(child))
            list.extend(self.to_list(child))

        return list







if __name__=="__main__":
    als_r = ALS_Reader()
    als_r.scan("/windows/Users/Nicolas Schilling/Ableton Live/Testing/test.als")
    als_r.add_midi_track(pos = 2)
    als_r.write()

