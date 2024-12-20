# When parsing the PDF's into text using LlamaParse, I concatenated all slides from a module into a file, as we initially planned for each document to be one module. 
# This script was used to split the slides into individual lectures, as we later decided that each document should be one lecture. 
# We read from the Parsed_Slides folder and writes to the Parsed_Lectures folder. 
# The script uses different delimiters to split the slides into lectures, as the format of output txt from all the slides varies between courses. 

import os 
from textacy import preprocessing

num_modules = 0

for filename in os.listdir('../../Dataset/Parsed_Slides'):

    course = filename.split(".")[0]
    
    # These could be split into lectures using " 1 ---" as a delimiter
    if course in ["DATA530", "DATA532", "DATA533", "DATA540", "DATA541", "DATA542", "DATA552", "DATA553", "DATA581", "DATA583", "DATA585", "DATA589"]:
       continue

    # This could be split into lectures using "Shan Du ---" as a delimiter
    if course in ["DATA572", "DATA586"]:
        continue

    # This could be split into lectures using " Lec " as a delimiter
    if course in ["DATA551"]:
        continue

    # These could be split into lectures using "UBCO MDS" as a delimiter
    if course in ["DATA543", "DATA570", "DATA571", "DATA573", "DATA582"]:
        continue

    # These could be split into lectures using "--- Lecture" as a delimiter
    if course in ["DATA531", "DATA534"]:
        continue

    # This could be split into lectures using " UBC " as a delimiter after manually adding "UBC" to lecture 1
    if course in ["DATA580"]:
        continue

    num_modules += 1
    print(course, ":")

    # Read from Parsed_Slides and write to Parsed_Lectures
    with open (f'../../Dataset/Parsed_Slides/{filename}', 'r', encoding="UTF-8") as file:

        content = file.read().replace('\n', ' ')    # Replace newlines with spaces, since pagebreaks are denoted by \n---\n in llamaparse output
        slides = content.split("Shan Du ---")       # Test different splitters   
        num_slides = 0

        for i in range(len(slides)):
            if len(slides[i]) < 200:        # Means that whatever was split probably wasn't a whole lecture 
                continue
            else:
                with open(f"../../Dataset/Parsed_Lectures/{course}_{num_slides}.txt", "w", encoding="UTF-8") as slide_file:
                    slide_file.write(slides[i])

                num_slides += 1
                # print(i, ":", slides[i][:50])     # Used to check if the delimiter worked for splitting
        print(num_slides, "slides")         # Expect a number like 6-8, if not then the delimiter probably didn't work

print("Number of modules: ", num_modules)