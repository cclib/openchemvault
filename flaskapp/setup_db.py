import math
import os
import sys
import json

from pymongo import MongoClient
from cclib.bridge.cclib2openbabel import makeopenbabel
import openbabel as ob
import numpy as np

import flaskapp.config as config
from flaskapp.process.chem_process import parse_file

# Database configuration
db_host = config.mongo_host
db_port = config.mongo_port
db_name = config.mongo_name
db_user = config.mongo_user
db_pass = config.mongo_pass
# Data folder path
default_data_folder_path = config.data_folder
# Store count of processed files
success_count = 0
# Modify database (1) or just loop through files and parse them (0)
insert_mode = 1
# Unbuffered output
# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)


def main(data_folder_path):
    try:
        db_conn = MongoClient(db_host, int(db_port))
        db = db_conn[db_name]
        if db_user != "":
            db.authenticate(db_user, db_pass)
        if data_folder_path == "":
            data_folder_path = default_data_folder_path
        if os.path.isdir(data_folder_path):
            db.molecule.delete_many({})
            db.parsed_file.delete_many({})
            iterate(data_folder_path, db, insert_mode)
            print("\nDone!")
            print("-" * 50)
        else:
            print("This folder was not found")
        find_stats_value(db)
        generate_svgs(db)
    except Exception as e:
        print("\nCannot setup database")
        print("-" * 50)
        print(e.message)
        print("-" * 50)


# Find min and max value for each applicable attribute
def find_stats_value(db):
    try:
        db.stats.delete_many({})
        # This list is also defined in view_routes.py, search.html
        attributes = {
            "charge"      : {"min": 0, "max": 0},
            "enthalpy"    : {"min": 0, "max": 0},
            "entropy"     : {"min": 0, "max": 0},
            "freeenergy"  : {"min": 0, "max": 0},
            "mult"        : {"min": 0, "max": 0},
            "natom"       : {"min": 0, "max": 0},
            "nbasis"      : {"min": 0, "max": 0},
            "nmo"         : {"min": 0, "max": 0},
            "temperature" : {"min": 0, "max": 0}
        }
        for x in attributes:
            key = "attributes." + x
            doc = db.parsed_file.find(
                {key: {"$exists": True}}, {key: 1}
            ).sort(key, 1).limit(1)
            attributes[x]["min"] = (list(doc))[0]["attributes"][x]
            doc = db.parsed_file.find(
                {key: {"$exists": True}}, {key: 1}
            ).sort(key, -1).limit(1)
            attributes[x]["max"] = (list(doc))[0]["attributes"][x]
        db.stats.insert_one(attributes)
    except:
        pass


# Generate SVG file for each inserted document
def generate_svgs(db):
    try:
        docs = db.parsed_file.find({})
    except:
        return
    if docs.count() > 0:
        dir_path = "flaskapp/static/svg/"
        if not os.path.isdir(dir_path):
            os.mkdir(dir_path)
        for x in docs:
            try:
                params = {
                    "atomcoords": np.asarray(x["attributes"]["atomcoords"]),
                    "atomnos": np.asarray(x["attributes"]["atomnos"]),
                    "charge": x["attributes"]["charge"],
                    "mult": x["attributes"]["mult"]
                }
            except:
                continue
            try:
                # Save the SVG file with filename same as mongodb document id
                file_path = dir_path + str(x["_id"]) + ".svg"
                print("Creating SVG : " + file_path)
                mol = makeopenbabel(**params)
                obconversion = ob.OBConversion()
                obconversion.SetOutFormat("svg")
                ob.obErrorLog.StopLogging()
                obconversion.WriteFile(mol, file_path)
            except:
                continue


# Recursively iterate through files in a directory
def iterate(dir_path, db, insert_mode=0):
    if not(dir_path.endswith("/")):
        dir_path = dir_path + "/"
    for file_name in os.listdir(dir_path):
        f = dir_path + file_name
        if os.path.isfile(f):
            add_file_to_database(f, db, insert_mode)
        elif os.path.isdir(f):
            iterate(f, db, insert_mode)


# Process a file and add to database if parsing was successful
def add_file_to_database(file_path, db, insert_mode=0):
    print("Processing file : ", file_path, ". . . ", end="")
    res = parse_file(file_path)
    if res["success"]:
        if "formula_string" not in res:
            print("  Failed: Unable to determine molecular formula")
        else:
            global success_count
            success_count += 1
            print("  Done!")
            if insert_mode == 1:
                insert_data(file_path, db, res)
    else:
        print("  Failed: Unable to parse the file")


# Insert given parsed data in database
def insert_data(file_path, db, data):
    formula = data["formula_string"]
    new_parsed_file_doc = {
        "attributes": data["attributes"],
        "formula_string": formula,
        "formula_dict": data["formula"],
        "file_path": file_path
    }
    if "InChI" in data:
        new_parsed_file_doc["InChI"] = data["InChI"]
    res = db.molecule.find_one({"formula": formula}, {"_id": 1})
    try:
        if res is None:
            temp = formula.split()
            elems = [temp[i] for i in range(len(temp)) if i%2==0]
            elem_counts = [temp[i] for i in range(len(temp)) if i%2==1]
            new_molecule_doc = {
                "formula": formula,
                "elements": elems,
                "element_counts": elem_counts,
                "parsed_files": []
            }
            db.molecule.insert_one(new_molecule_doc)
        res = db.parsed_file.insert_one(new_parsed_file_doc)
        db.molecule.update_one({"formula": formula},
                               {"$push": {"parsed_files": res.inserted_id}})
    except Exception as e:
        print("Error in inserting document")
        print("-" * 50)
        print(e)
        print("-" * 50)
        pass


# Function to get distances between atoms of molecule
def distance_list(atom_coords):
    dist_list = []
    l = len(atom_coords)
    for i in range(l):
        for j in range(l):
            if i != j:
                dist_list.append(distance(atom_coords[i], atom_coords[j]))
    dist_list.sort()
    return dist_list


# Utility function to compute distance between 2 atom coordinates
def distance(p1, p2):
    sq_sum = 0
    for i in range(3):
        sq_sum += (p1[i] - p2[i])**2
    return math.sqrt(sq_sum)
