import os, shutil, copy, sys, logging, m_hash
from tkinter import *

import gui


"""
Contains logic for checking, copying files.
"""

# TODO: Unit testing of checkPaths?
# TODO: Need to find way to compare two list of sets. There seem to be lots of resources but I need to learn how set or comprehensions work.
# TODO: Better check for file method. currently only checking names but I can do size (os.path.getsize) or some sort of hash algorithm to make it more fool proof)

# TODO: If it's same name but different size it knows it's different file now. However it will just copy and overwrite I suspect!!! For now it make it sys.exit() and terminate.


#V03: Main sync seems to work. Does need more testing for sure. I'll touch up input and all the other functions to be more easier to use now.
    #Issue. Empty folder it throws errors. Gotta fix this!
    #Also need same structure because of way loop works?!?. Yep, it does otherwise nonetype is returned from try catch and erorr is thrown in next part.
        #Should it make structure first or can code be smarter to not run into this error?

#Hard core for now but make it possible to choose later
#V04: Haven't changed much. But once folder structure's same it seems to be working?
#V06: Added condition for syncing. E.g no new files, don't even run copying, instead just exit.

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# ospath way of doing input... some sort of parasing. split method?
original_folder = r'C:/3 test file/3 programming/4 dance folder skelton - test 01/3 dance sync test - source'
copy_folder = r'C:/3 test file/3 programming/4 dance folder skelton - test 01/3 destination'

class MyCopier(object):

    def __init__(self, sourceFolder, destinationFolder):
        self.sourceFolder = sourceFolder
        self.destinationFolder = destinationFolder
        self.contents_Source = []
        self.contents_destination = []
        self.contents_to_sync_list = None

    def run(self):
        gui.log_box.insert(END, original_folder+'\n')
        gui.log_box.insert(END, "1 way syncing to \n")
        gui.log_box.insert(END, copy_folder+'\n')
        gui.log_box.insert(END, '\n')

        if not self.checkPaths(self.sourceFolder, self.destinationFolder):
            gui.log_box.insert(END, 'Exiting.\n\n')
            sys.exit()

        self.contents_Source = self.get_contents(self.sourceFolder)
        self.contents_destination = self.get_contents(self.destinationFolder)

        #Checking to see if folder structure is the same. If not abort.

        folder_diff = self.check_folder_structure(self.contents_Source, self.contents_destination)
        if folder_diff:
            gui.log_box.insert(END, 'ERROR: Folder structures are different between source and destination. \n Two folder are not compatible or please make structures same.\n\n', "warning")
            sys.exit()
        else:
            gui.log_box.insert(END, 'Great! Folder structures are same. Preceding.\n')
        if gui.combo_check_box.get() == 'Name and Size':
            self.contents_to_sync_list = self.new_contents_bubble_size_check(self.contents_Source, self.contents_destination)
        elif gui.combo_check_box.get() == 'Name and Hash':
            self.contents_to_sync_list = self.new_contents_bubble_hash(self.contents_Source, self.contents_destination)
        #


        if self.number_of_files(self.contents_to_sync_list) == 0:
            gui.log_box.insert(END, "Done! No file needs syncing! :) \n\n")
            sys.exit()
        else:
            self.copy_contents(self.contents_to_sync_list, self.contents_destination)

        self.number_of_files(self.contents_to_sync_list)
        self.number_of_files(self.contents_Source)
        gui.log_box.insert(END, '\n\n')

    #Not sure how I should design this. Maybe make dir if it doesn't exist? For now I'll only copy if two folders are there.
    def checkPaths(self, folder1, folder2):
        if os.path.isdir(folder1) and os.path.isdir(folder2):
            gui.log_box.insert(END, "Great! Source and Destination exists. Lets go ahead. \n")
            return True
        gui.log_box.insert(END, "Error: Source or Destination is missing \n", 'warning')
        return False

    def get_contents(self, an_folder):
        list_of_contents = []
        for folderName, subFolders, fileNames in os.walk(an_folder):
            list_of_contents.append((folderName, subFolders, fileNames))
        return list_of_contents

    def new_contents_bubble_size_check(self, source, destination):
        new_content_list = copy.deepcopy(source) #To make copy of the list
        #logging.info("====== new_content_list ===== \n".center(55) + str(new_content_list) + "\n\n")
        logging.debug((len(source)))
        try:
            for i in range(len(source)):
                logging.debug("i: {}. .".format(i))
                # below is the search algorithm.
                for file_a in source[i][2]:
                    logging.debug("file_a ===== a =====: {}".format(file_a))
                    first = 0
                    last = len(destination[i][2])-1
                    found = False
                    while first <= last and not found:
                        midpoint = (first+last) // 2
                        file_a_full = source[i][0] + '\\' + file_a
                        file_b = destination[i][2][midpoint]
                        file_b_full = destination[i][0] + '\\' + file_b
                        # If name and size are same it takes it out of new_content_list. new_content_list contains all the items to sync
                        if self.check_file_names(file_a, file_b) and self.check_file_size(file_a_full, file_b_full):
                            found = True
                            logging.info("Bubble_sort + name + size checker passed: From list, Removing {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
                        # elif self.check_file_names(file_a, file_b) or self.check_file_size(file_a_full, file_b_full):
                        #     gui.log_box.insert(END, "Error: Uh oh... two file with same name but different size\n", 'warning')
                        #     gui.log_box.insert(END, "or same size but different name! Please check these files\n", 'warning')
                        #     gui.log_box.insert(END, file_a_full+"\n")
                        #     gui.log_box.insert(END, file_b_full+"\n\n")
                        #     sys.exit()
                        else:
                            if file_a < destination[i][2][midpoint]:
                                last = midpoint-1
                            else:
                                first = midpoint+1
            return new_content_list
        except IndexError:
            logging.debug("IndexError. Source or destination is empty. Content_to_sync_list will be none so next part will throw error!")


    def new_contents_bubble_hash(self, source, destination):
        new_content_list = copy.deepcopy(source) #To make copy of the list
        #logging.info("====== new_content_list ===== \n".center(55) + str(new_content_list) + "\n\n")
        logging.debug((len(source)))
        try:
            for i in range(len(source)):
                logging.debug("i: {}. .".format(i))
                # below is the search algorithm.
                for file_a in source[i][2]:
                    logging.debug("file_a ===== a =====: {}".format(file_a))
                    first = 0
                    last = len(destination[i][2])-1
                    found = False
                    while first <= last and not found:
                        midpoint = (first+last) // 2
                        file_a_full = source[i][0] + '\\' + file_a
                        file_b = destination[i][2][midpoint]
                        file_b_full = destination[i][0] + '\\' + file_b
                        # If name and size are same it takes it out of new_content_list. new_content_list contains all the items to sync
                        if m_hash.returnHash(file_a_full) == m_hash.returnHash(file_b_full) and self.check_file_names(file_a, file_b):
                            found = True
                            logging.info("Bubble_sort + hashed {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
                        else:
                            if file_a < destination[i][2][midpoint]:
                                last = midpoint-1
                            else:
                                first = midpoint+1
            return new_content_list
        except IndexError:
            logging.debug("IndexError. Source or destination is empty. Content_to_sync_list will be none so next part will throw error!")

    #if same, returns True
    def check_file_names(self, file_a, file_b):
        if file_a == file_b:
            return True
        else:
            return False

    #if same, returns False
    def check_file_size(self, file_a_full, file_b_full):
        if os.path.getsize(file_a_full) == os.path.getsize(file_b_full):
            return True
        else:
            return False

    # ospath way of doing here
    def copy_contents(self, sync_list, destination):
        try:
            for i in range(len(sync_list)):
                for file_sync in sync_list[i][2]:
                    gui.log_box.insert(END, "Copying...\n")
                    gui.log_box.insert(END, sync_list[i][0] + '\\' + file_sync + "\n")
                    gui.log_box.insert(END, "to\n")
                    gui.log_box.insert(END, destination[i][0] + '\\' + file_sync + "\n")

                    gui.log_box.insert(END, 'Copy Status: ' + str(gui.var_enable_copy.get())+'\n')
                    # if str(gui.var_enable_copy.get()) == "1":
                    if gui.var_enable_copy.get():
                        shutil.copy2((sync_list[i][0] + '\\' + file_sync), (destination[i][0] + '\\' + file_sync))
                    elif not gui.var_enable_copy.get():
                        gui.log_box.insert(END, "Syncing disabled. Please tick 'Enable Copy' to enable syncing."+ "\n")
            gui.log_box.insert(END, "1-Way sync done. All the files are copied."+ "\n")
        except TypeError:
            logging.debug("Hmm Type Error. This shouldn't be showing up")

    # Shows number of files in an folder including all of it's subfolders.
    # INPUT MUST BE OS.WALK LIST (List)
    def number_of_files(self, input_folder):
        try:
            counter = 0
            for folder in range(len(input_folder)):
                for file in input_folder[folder][2]:
                    counter += 1
            logging.debug('"counter turn from "number_of_files": {}'.format(counter))
            return counter
        except TypeError:
            print("Error, NoneType has no len(). Probably empty folder or something")

    # Folder structure checker
    # For now it's very simple. If there's problem it returns True. Otherwise False
    def check_folder_structure(self, source, destination):
        for i in range(len(source)):
            for folder_source in source[i][1]:
                if folder_source not in destination[i][1]:
                    return True # Issue this is returned.
        return False #No issue this is returned

logging.disable(logging.INFO)