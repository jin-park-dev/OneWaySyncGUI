import os, shutil, copy, sys, logging, m_hash

# TODO: Unit testing of checkPaths?
# TODO: Need to find way to compare two list of sets. There seem to be lots of resources but I need to learn how set or comprehensions work.
# TODO: Question. I can't get it to delete element. I tried deleting using list position AND remove method. Both fail in same way where it still leave many of the items inside the list. This happened with all methods of copying list apart from "Deepcopy" or "just copy paste actual data structure into a variable". WHHHHHHHHY??? It looks same when I print them!!!!!!!!!!! (new_content_list = list(self.contents_ori), or copy.copy(self.content_ori) doesn't actually work!!!
# TODO: Better check for file method. currently only checking names but I can do size (os.path.getsize) or some sort of hash algorithm to make it more fool proof)


# TODO: If it's same name but different size it knows it's different file now. However it will just copy and overwrite I suspect!!! For now it make it sys.exit() and terminate.


#V02: It's like 70% WIP
#V03: Main sync seems to work. Does need more testing for sure. I'll touch up input and all the other functions to be more easier to use now.
    #Issue. Empty folder it throws errors. Gotta fix this!
    #Also need same structure because of way loop works?!?. Yep, it does otherwise nonetype is returned from try catch and erorr is thrown in next part.
        #Should it make structure first or can code be smarter to not run into this error?

#Hard core for now but make it possible to choose later
#V04: Haven't changed much. But once folder structure's same it seems to be working?
#V06: Added condition for syncing. E.g no new files, don't even run copying, instead just exit.

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

# ospath way of doing input... some sort of parasing. split method?
original_folder = r'X:\1 Music Vid\1 Dances\1 Lessons\1 Lessons Share'
copy_folder = r'D:\OneDrive\Pictures\4 Sharing with Others\Dances'

class MyCopier(object):

    def __init__(self, sourceFolder, destinationFolder):
        self.sourceFolder = sourceFolder
        self.destinationFolder = destinationFolder
        self.contents_Source = []
        self.contents_destination = []

    def run(self):
        print("==================================")
        print(original_folder)
        print("1 way syncing to ")
        print(copy_folder)
        print("==================================")

        if not self.checkPaths(self.sourceFolder, self.destinationFolder):
            print("Exiting")
            sys.exit()

        self.contents_Source = self.get_contents(self.sourceFolder)
        self.contents_destination = self.get_contents(self.destinationFolder)

        #Checking to see if folder structure is the same. If not abort.

        folder_diff = self.check_folder_structure(self.contents_Source, self.contents_destination)
        if folder_diff:
            print("Folder structures are different between source and destination. Manually fix.")
            sys.exit()
        else:
            print("Great! Folder structures are same. Preceding.")


        #logging.info("====== self.contents_Source ===== \n".center(55) + str(self.contents_Source) + "\n\n")
        #logging.info("====== self.contents_destination ===== \n".center(55) + str(self.contents_destination) + "\n\n")

        #contents_to_sync_list = self.new_contents(self.contents_Source, self.contents_destination)
        #contents_to_sync_list = self.new_contents_hash(self.contents_Source, self.contents_destination) #better updated way of copmaring files. #Hash is so slow.
        #contents_to_sync_list = self.new_contents_bubble_hash(self.contents_Source, self.contents_destination)
        contents_to_sync_list = self.new_contents_bubble_size_check(self.contents_Source, self.contents_destination)


        #print(contents_to_sync_list)

        if self.number_of_files(contents_to_sync_list) == 0:
            print("Done! No file needs syncing! :) ")
            sys.exit()
        else:
            print("disabled copy content for dev purposes")
            self.copy_contents(contents_to_sync_list, self.contents_destination)

        self.number_of_files(contents_to_sync_list)
        self.number_of_files(self.contents_Source)

    """
    # Used for testing purpose only.
    def run_test_check_folder_structure(self):
        self.contents_Source = self.get_contents(self.sourceFolder)
        self.contents_destination = self.get_contents(self.destinationFolder)

        folder_diff = self.check_folder_structure(self.contents_Source, self.contents_destination)
        print(folder_diff)
    """

    #Not sure how I should design this. Maybe make dir if it doesn't exist? For now I'll only copy if two folders are there.
    def checkPaths(self, folder1, folder2):
        if os.path.isdir(folder1) and os.path.isdir(folder2):
            print("Great! Source and Destination exists. Lets go ahead.")
            return True
        print("Error! Source or Destination is missing")
        return False

    def get_contents(self, an_folder):
        list_of_contents = []
        for folderName, subFolders, fileNames in os.walk(an_folder):
            list_of_contents.append((folderName, subFolders, fileNames))
        return list_of_contents

    #For now lets keep it simple
    #And assume user isn't going to create extra folder and other issues in backup folder.
    #This method simply looks for missing content in destination folder
    #aka
    #What the new files to add.
    def new_contents(self, source, destination):
        new_content_list = copy.deepcopy(source) #To make copy of the list
        #logging.info("====== new_content_list ===== \n".center(55) + str(new_content_list) + "\n\n")
        logging.debug((len(source)))
        try:
            for i in range(len(source)):
                logging.debug("i: {}. .".format(i))
                for file_a in source[i][2]:

                    # *** file_a_full_path = first part + \\ +file_a (use os.path to put it into list?) aka source[i][0] + "\\" + file_a


                    logging.debug("file_a ===== a =====: {}".format(file_a))
                    #logging.debug("source[i][2]: {}".format(source[i][2]))
                    for file_b in destination[i][2]:

                        # *** file_b_full_path = first part + \\ +file_b (use os.path to put it into list?)

                        logging.debug("file_b xxxxxx b xxxxxx: {}".format(file_b))
                        #logging.debug("destination[i][2]: {}".format(destination[i][2]))

                        # replace if with...
                        # *** if m_hash.returnHash(file_a_full_path) == m_hash.returnHash(file_b_full_path):


                        if file_a == file_b:
                            logging.info("From list, Removing {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
            return new_content_list
        except IndexError:
            logging.debug("IndexError. Source or destination is empty. Content_to_sync_list will be none so next part will throw error!")

    #fuuuck takes so long. Maybe crc-32 check instead?
    def new_contents_hash(self, source, destination):
        new_content_list = copy.deepcopy(source)  # To make copy of the list
        # logging.info("====== new_content_list ===== \n".center(55) + str(new_content_list) + "\n\n")
        logging.debug((len(source)))
        try:
            for i in range(len(source)):
                logging.debug("i: {}. .".format(i))
                for file_a in source[i][2]:
                    file_a_full_path = source[i][0] + '\\' + file_a
                    #print(file_a_full_path) #This is looking correct, del later
                    logging.debug("file_a ===== a =====: {}".format(file_a))
                    # logging.debug("source[i][2]: {}".format(source[i][2]))
                    for file_b in destination[i][2]:

                        file_b_full_path = destination[i][0] + '\\' + file_b
                        print(file_b_full_path)

                        logging.debug("file_b xxxxxx b xxxxxx: {}".format(file_b))
                        # logging.debug("destination[i][2]: {}".format(destination[i][2]))

                        # replace if with...
                        # *** if m_hash.returnHash(file_a_full_path) == m_hash.returnHash(file_b_full_path):


                        if m_hash.returnHash(file_a_full_path) == m_hash.returnHash(file_b_full_path):
                            logging.info("From list, Removing {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
            return new_content_list
        except IndexError:
            logging.debug(
                "IndexError. Source or destination is empty. Content_to_sync_list will be none so next part will throw error!")

    def new_contents_bubble(self, source, destination):
        new_content_list = copy.deepcopy(source) #To make copy of the list
        #logging.info("====== new_content_list ===== \n".center(55) + str(new_content_list) + "\n\n")
        logging.debug((len(source)))
        try:
            for i in range(len(source)):
                logging.debug("i: {}. .".format(i))
                #below is the search algorithm.
                for file_a in source[i][2]:
                    logging.debug("file_a ===== a =====: {}".format(file_a))
                    #logging.debug("source[i][2]: {}".format(source[i][2]))
                    first = 0
                    last = len(destination[i][2])-1
                    found = False
                    while first <= last and not found:
                        midpoint = (first+last)//2
                        if destination[i][2][midpoint] == file_a:
                            found = True
                            logging.info("Bubble_sort: From list, Removing {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
                        else:
                            if file_a < destination[i][2][midpoint]:
                                last = midpoint-1
                            else:
                                first = midpoint+1
            return new_content_list
        except IndexError:
            logging.debug(
                "IndexError. Source or destination is empty. Content_to_sync_list will be none so next part will throw error!")

    def new_contents_bubble_size_check(self, source, destination):
        new_content_list = copy.deepcopy(source) #To make copy of the list
        #logging.info("====== new_content_list ===== \n".center(55) + str(new_content_list) + "\n\n")
        logging.debug((len(source)))
        try:
            for i in range(len(source)):
                logging.debug("i: {}. .".format(i))
                #below is the search algorithm.
                for file_a in source[i][2]:
                    logging.debug("file_a ===== a =====: {}".format(file_a))
                    #logging.debug("source[i][2]: {}".format(source[i][2]))
                    first = 0
                    last = len(destination[i][2])-1
                    found = False

                    while first <= last and not found:
                        midpoint = (first+last)//2

                        file_a_full = source[i][0] + '\\' + file_a
                        file_b = destination[i][2][midpoint]
                        file_b_full = destination[i][0] + '\\' + file_b

                        # print("self.check_file_names(file_a, file_b): " + str(self.check_file_names(file_a, file_b)))
                        # print("self.check_file_size(file_a_full, file_b_full): " + str(self.check_file_size(file_a_full, file_b_full)))
                        # print("")

                        #If name and size are same it takes it out of new_content_list. new_content_list contains all the items to sync
                        if self.check_file_names(file_a, file_b) and self.check_file_size(file_a_full, file_b_full):
                            found = True
                            # print("removing: " + file_a)
                            logging.info("Bubble_sort + name + size checker passed: From list, Removing {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
                        elif  self.check_file_names(file_a, file_b) or self.check_file_size(file_a_full, file_b_full):
                            print("Uh oh... two file with same name but different size")
                            print("or same size but different name! Please check these files")
                            print(file_a_full)
                            print(file_b_full)
                            sys.exit()
                        else:
                            if file_a < destination[i][2][midpoint]:
                                last = midpoint-1
                            else:
                                first = midpoint+1
            return new_content_list
        except IndexError:
            logging.debug(
                "IndexError. Source or destination is empty. Content_to_sync_list will be none so next part will throw error!")

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

    def new_contents_bubble_hash(self, source, destination):
        new_content_list = copy.deepcopy(source)  # To make copy of the list
        # logging.info("====== new_content_list ===== \n".center(55) + str(new_content_list) + "\n\n")
        logging.debug((len(source)))
        try:
            for i in range(len(source)):
                logging.debug("i: {}. .".format(i))
                # below is the search algorithm.
                for file_a in source[i][2]:
                    logging.debug("file_a ===== a =====: {}".format(file_a))
                    # logging.debug("source[i][2]: {}".format(source[i][2]))
                    file_a_full_path = source[i][0] + '\\' + file_a

                    first = 0
                    last = len(destination[i][2]) - 1
                    found = False

                    while first <= last and not found:
                        midpoint = (first + last) // 2
                        file_b_full_path = destination[i][0] + '\\' + destination[i][2][midpoint]
                        if m_hash.returnHash(file_a_full_path) == m_hash.returnHash(file_b_full_path):
                            found = True
                            logging.info(
                                "Bubble_sort: From list, Removing {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
                        else:
                            if file_a < destination[i][2][midpoint]:
                                last = midpoint - 1
                            else:
                                first = midpoint + 1

                    """
                    for file_b in destination[i][2]:
                        logging.debug("file_b xxxxxx b xxxxxx: {}".format(file_b))
                        #logging.debug("destination[i][2]: {}".format(destination[i][2]))
                        if file_a == file_b:
                            logging.info("From list, Removing {}\\{}".format(source[i][0], file_a))
                            new_content_list[i][2].remove(file_a)
                    """
            return new_content_list
        except IndexError:
            logging.debug("IndexError. Source or destination is empty. Content_to_sync_list will be none so next part will throw error!")

    # ospath way of doing here
    def copy_contents(self, sync_list, destination):
        try:
            for i in range(len(sync_list)):
                for file_sync in sync_list[i][2]:
                    print("Copying...")
                    print(sync_list[i][0] + '\\' + file_sync)
                    print("to")
                    print(destination[i][0] + '\\' + file_sync)
                    print()
                    #shutil.copy2((sync_list[i][0] + '\\' + file_sync), (destination[i][0] + '\\' + file_sync))
                    print("DISABLED FOR DEV (Enable line above to activate copying: shutil.copy2((sync_list[i][0] + '\/' + file_sync), (destination[i][0] + '\/' + file_sync))")
            print("1-Way sync done. All the files are copied.")
        except TypeError:
            print("Hmm Type Error. This shouldn't be showing up")

    # Shows number of files in an folder including all of it's subfolders.
    # INPUT MUST BE OS.WALK LIST (List)
    def number_of_files(self, input_folder):
        counter = 0
        for folder in range(len(input_folder)):
            for file in input_folder[folder][2]:
                counter += 1
        logging.debug('"counter turn from "number_of_files": {}'.format(counter))
        return counter

    # Folder structure checker
    # For now it's very simple. If there's problem it returns True. Otherwise False
    def check_folder_structure(self, source, destination):
        #folder_diff = []
        for i in range(len(source)):
            for folder_source in source[i][1]:
                if folder_source not in destination[i][1]:
                    return True # Issue this is returned.
        return False #No issue this is returned


"""
#For GUI, disable everything below or it'll duplicate.
test_obj = MyCopier(original_folder, copy_folder)
#logging.disable(logging.INFO)
test_obj.run()
"""

logging.disable(logging.INFO)