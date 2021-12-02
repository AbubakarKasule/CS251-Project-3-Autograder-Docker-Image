# Author: Abubakar Kasule
# Date: Nov 2021
# Description: Script to copy and process CS251 Project 3 submissions
# Notes: Current working directory for this file is /autograder/source
"""
Requirments: 
1. All modules listed below & Python 3+
2. Java 17+ installed. 
"""

from glob import glob 
import os

# Global Variable to toggle between test and prod
test = False

if test:
    SOURCE_PATH = "."
else:
    SOURCE_PATH = "/autograder/source"


# Global variables used to determine if certain methods were implemented as we expect
bottomOfGrid = True
initializeGrid = True
parseInput = True
sequenceDifference = True
gridToString = True
generateNextTerms = True
pairWiseIterator = True

# Function used to check if certain methods were implemented as we expect
def find_missing_methods_for_unit_testing(files):
    global bottomOfGrid, initializeGrid, parseInput, sequenceDifference, gridToString, generateNextTerms, pairWiseIterator

    # For each java file in the student's submission
    for file_path in files:
        # Open file
        file = open(file_path, 'r')
        lines = file.readlines()

        """
        This toggle allows us to ignore javadocs during processing.
        This is necessary as javadocs could mess with other processing
        procedures such as the handling of curlybraces
        """
        in_javadoc = False

        # For every line in the current file
        for line_dirty in lines:
            # Handle javadocs
            if "/*" in line_dirty: # start of java doc
                in_javadoc = True

            if "*/" in line_dirty: # end of java doc
                in_javadoc = False
                continue
            
            if in_javadoc:         # Middle of javadoc
                continue
            

            # Handle comments. 
            # Take first element in split because everything after first delim is non-functioning
            # This is kinda risky as '//' can be used in strings. Breaking the line will cause issues in those cases
            if "//" in line_dirty:
                line = line_dirty.split("//")[0].strip()

                if len(line) == 0:
                    # entire line is a comment
                    continue
            else:
                line = line_dirty

            # Check if method is implemented as we expected
            if "bottomOfGrid" in line and "Sequence" in line and "boolean" in line and "static" in line:
                bottomOfGrid = False

            if "initializeGrid" in line and "List<Sequence>" in line and "Sequence" in line and "static" in line:
                initializeGrid = False

            if "parseInput" in line and "List<Integer>" in line and "List<String>" in line and "static" in line:
                parseInput = False

            if "sequenceDifference" in line and "Sequence" in line and "static" in line:
                sequenceDifference = False

            if "gridToString" in line and "double" in line and "List<Sequence>" in line and "String" in line and "static" in line:
                gridToString = False

            if "generateNextTerms" in line and "List<Sequence>" in line and "void" in line and "static" in line:
                generateNextTerms = False

            if "pairWiseIterator()" in line and "Iterable<Pair<Integer, Integer>>" in line:
                pairWiseIterator = False

        file.close()


# Function used to identify all declared packages
def find_package_names(files):
    found_packages = []

    # For each java file in the student's submission
    for file_path in files:
        # Open file
        file = open(file_path, 'r')
        lines = file.readlines()

        """
        This toggle allows us to ignore javadocs during processing.
        This is necessary as javadocs could mess with other processing
        procedures such as the handling of curlybraces
        """
        in_javadoc = False

        for line_dirty in lines:
            # Handle javadocs
            if "/*" in line_dirty: # start of java doc
                in_javadoc = True

            if "*/" in line_dirty: # end of java doc
                in_javadoc = False
                continue
            
            if in_javadoc:         # Middle of javadoc
                continue
            

            # Handle comments. 
            # Take first element in split because everything after first delim is non-functioning
            if "//" in line_dirty:
                line = line_dirty.split("//")[0].strip()

                if len(line) == 0:
                    # entire line is a comment
                    continue
            else:
                line = line_dirty

            # If line is a package, remove and save package name to remove from subsequent lines
            if "package" in line:
                package_names = line.replace("package", '').replace(" ", "").split('.')

                for package_name in package_names:
                    found_packages.append(package_name.replace(";", "").replace("\n", ""))

        file.close()

    return found_packages


def process_java_file(file_path, found_packages):

    file = open(file_path, 'r')
    lines = file.readlines()

    # Array containing the lines were are going to write into our new processed file
    # initialized array with lines that will ensure there are no errors
    processed_lines = ["package com.gradescope.project3.code;\n", "import java.util.*;\n", "import com.gradescope.project3.code.*;\n"]

    """
    This toggle allows us to ignore javadocs during processing.
    This is necessary as javadocs could mess with other processing
    procedures such as the handling of curlybraces
    """
    in_javadoc = False
    closed_parentheses = None

    for line_dirty in lines:
        # Handle javadocs
        if "/*" in line_dirty: # start of java doc
            in_javadoc = True

            processed_lines.append(line_dirty.split("/*")[0])

        if "*/" in line_dirty: # end of java doc
            in_javadoc = False
            processed_lines.append(line_dirty.split("*/")[-1])
            continue

        if in_javadoc:         # Middle of javadoc
            continue

        # Handle comments. 
        # Take first element in split because everything after first delim is non-functioning
        # Removed due to issues differentiating betwen a comment and other uses of "//"
        # might cause some issue if there are curly braces in a comment
        # This is kinda risky as '//' can be used in strings. Breaking the line will cause issues in those cases
        """
        if "//" in line_dirty:
            line = line_dirty.split("//")[0].strip()

            if len(line) == 0:
                # entire line is a comment
                continue
        else:
            line = line_dirty
        """
        line = line_dirty

        

        # Handle imports from non-standard libraries
        if "import" in line:
            _continue = False
            for package_name in found_packages:
                if package_name in line and "java" not in line:
                    _continue = True
            
            if _continue:
                continue    

        # Alter incomplete methods to avoid compile time errors
        if "generateNextTerms" in line and generateNextTerms:
            line = line.replace("generateNextTerms", "generateNextTermsNull")    

        if "bottomOfGrid" in line and bottomOfGrid:
            line = line.replace("bottomOfGrid", "bottomOfGridNull")    

        if "initializeGrid" in line and initializeGrid:
            line = line.replace("initializeGrid", "initializeGridNull")    

        if "parseInput" in line and parseInput:
            line = line.replace("parseInput", "parseInputNull")    

        if "sequenceDifference" in line and sequenceDifference:
            line = line.replace("sequenceDifference", "sequenceDifferenceNull")    

        if "gridToString" in line and gridToString:
            line = line.replace("gridToString", "gridToStringNull")  

 

        # Handle packages and special lines
        # If line is a package, skip
        if "package" in line:
            continue

        # Change non-main name to main
        if "SequencePredictor" in line:
            line = line.replace("SequencePredictor", "Main")
        
        if "SequenceGenerator" in line:
            line = line.replace("SequenceGenerator", "Main")

        # Remove incorrect sequence import
        if "import javax.sound.midi.Sequence;" in line:
            continue

 
        # Beginning of class definition, start keeping track of open/close parentheses
        if "public class" in line:
            closed_parentheses = 1
            processed_lines.append(line)
           
            # Add any missing methods to prevent compile time errors for autograder
            if bottomOfGrid:
                processed_lines.append('\tpublic static boolean bottomOfGrid_missing = true;\n')
            else:
                processed_lines.append('\tpublic static boolean bottomOfGrid_missing = false;\n')
                
            if initializeGrid:
                processed_lines.append('\tpublic static boolean initializeGrid_missing = true;\n')
            else:
                processed_lines.append('\tpublic static boolean initializeGrid_missing = false;\n')

            if parseInput:
                processed_lines.append('\tpublic static boolean parseInput_missing = true;\n')
            else:
                processed_lines.append('\tpublic static boolean parseInput_missing = false;\n')

            if sequenceDifference:
                processed_lines.append('\tpublic static boolean sequenceDifference_missing = true;\n')
            else:
                processed_lines.append('\tpublic static boolean sequenceDifference_missing = false;\n')

            if gridToString:
                processed_lines.append('\tpublic static boolean gridToString_missing = true;\n')
            else:
                processed_lines.append('\tpublic static boolean gridToString_missing = false;\n')

            if generateNextTerms:
                processed_lines.append('\tpublic static boolean generateNextTerms_missing = true;\n')
            else:
                processed_lines.append('\tpublic static boolean generateNextTerms_missing = false;\n')

            if pairWiseIterator:
                processed_lines.append('\tpublic static boolean pairWiseIterator_missing = true;\n')
            else:
                processed_lines.append('\tpublic static boolean pairWiseIterator_missing = false;\n')

            continue


        # Make all methods public so I can do unit testing
        if 'private' in line:
            line = line.replace('private', 'public')

        # Handle parens
        if closed_parentheses is not None:
            # comment bug fix
            try:
                slash = line.index("//")
            except:
                slash = len(line)
            
            # Make sure curly brace is not in a comment
            if "{" in line and line.index("{") < slash:
                closed_parentheses += line.count("{")
            
            if "}" in line and line.index("}") < slash:
                closed_parentheses -= line.count("}")

        # End of class definition
        if closed_parentheses == 0:
            # Add any missing methods to prevent compile time errors for autograder

            if bottomOfGrid and os.path.basename(file_path) == "Main.java":
                processed_lines.append('\tpublic static boolean bottomOfGrid(Sequence sequence) { return false; }\n')
                
            if initializeGrid and os.path.basename(file_path) == "Main.java":
                processed_lines.append('\tpublic static List<Sequence> initializeGrid(Sequence sequence) { return Arrays.asList(sequence); }\n')

            if parseInput and os.path.basename(file_path) == "Main.java":
                processed_lines.append('\tpublic static List<Integer> parseInput(List<String> args) { return Arrays.asList(1, 2); }\n')

            if sequenceDifference and os.path.basename(file_path) == "Main.java":
                processed_lines.append('\tpublic static Sequence sequenceDifference(Sequence sequence) { return sequence; }\n')

            if gridToString and os.path.basename(file_path) == "Main.java":
                processed_lines.append('\tpublic static String gridToString(double spacing, List<Sequence> sequences) { return ""; }\n')

            if generateNextTerms and os.path.basename(file_path) == "Main.java":
                processed_lines.append('\tpublic static void generateNextTerms(List<Sequence> sequences) {  }\n')

            if pairWiseIterator and os.path.basename(file_path) == "Sequence.java":
                processed_lines.append('\tpublic Iterable<Pair<Integer, Integer>> pairWiseIterator() { return null; }\n')

        # Add processed line to file
        processed_lines.append(line)

        # Check if we have traversed the entire class. File is complete if so
        if closed_parentheses == 0:
            break

    # Close student's file
    file.close()

    """
    Write our processed kines into a file
    Consider alternative main files
    """

    # Change non-main to main
    if "SequencePredictor" in os.path.basename(file_path):
        file = open("src/main/java/com/gradescope/project3/code/" + os.path.basename(file_path).replace("SequencePredictor", "Main"), 'w')
        file.writelines(processed_lines)
        file.close()
    elif "SequenceGenerator" in os.path.basename(file_path):
        file = open("src/main/java/com/gradescope/project3/code/" + os.path.basename(file_path).replace("SequenceGenerator", "Main"), 'w')
        file.writelines(processed_lines)
        file.close()
    else:
        file = open("src/main/java/com/gradescope/project3/code/" + os.path.basename(file_path), 'w')
        file.writelines(processed_lines)
        file.close()


"""
Bringing it all together
"""
# Find student's java files
if test:
    java_files = glob('./test_submission' + '/**/'+'*.java', recursive=True)
else:
    java_files = glob('/autograder/submission' + '/**/'+'*.java', recursive=True)

pair_exists = False
sequence_exists = False

# Student could be missing Pair or sequence.
# Replace with functioning pair file and Sequence.java with non-functioning pairwise
for file in java_files:
    if os.path.basename(file) == "Pair.java":
        pair_exists = True
    
    if os.path.basename(file) == "Sequence.java":
        sequence_exists = True

if not pair_exists:
    java_files.append(SOURCE_PATH + '/replacement_code/Pair.java')

if not sequence_exists:
    java_files.append(SOURCE_PATH + '/replacement_code/Sequence.java')

# Find packages used by students
found_packages = find_package_names(java_files)

# Find missing methods and add dummy methods to replace
find_missing_methods_for_unit_testing(java_files)

# Process student files
for file in java_files:
    process_java_file(file, found_packages)

################ EOF ##################
