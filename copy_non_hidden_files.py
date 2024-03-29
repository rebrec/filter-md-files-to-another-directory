from datetime import datetime 
import frontmatter
import os
import shutil

source = os.environ.get("INPUT_SOURCE")
destination = os.environ.get("INPUT_DESTINATION")
debug_enabled = os.environ.get("INPUT_DEBUG")
if debug_enabled in vars(): 
    debug_enabled = False
    print("setting default debug = false")
else: 
    print("debug = {}".format(debug_enabled))

if os.path.isfile('.testenv'):
    lines = open('.testenv').readlines()
    source = lines[0].split('=')[1].strip()
    destination = lines[1].split('=')[1].strip()
    debug_enabled = lines[2].split('=')[1].strip() == "true"

if source.endswith(os.path.sep):
    source = source[:-1]
if destination.endswith(os.path.sep):
    destination = destination[:-1]

def debug(message):
    if debug_enabled: print(message)

debug("*" * 30)
debug("Source      : {}".format(source))
debug("Destination : {}".format(destination))
debug("Debug       : {}".format(debug))
debug("*" * 30)


today = datetime.date(datetime.now())



def copy_files(source, destination):
    for (folder_name, subdirs, files) in os.walk(source, topdown=True):
        relative_folder_name = folder_name.replace(source, "")
        
        for file in files:
            relative_file_path = os.path.join(relative_folder_name, file)
            debug("*" * 30)
            source_full_path = source + os.path.sep + relative_file_path
            destination_full_path = destination + os.path.sep + relative_file_path
            debug("- {}".format(source_full_path))
            debug("        relative_file_path     = {}".format(relative_file_path))
            debug("        source_full_path       = {}".format(source_full_path))
            debug("        destination_full_path  = {}".format(destination_full_path))
            if file.endswith('.md'):
                markdown_file = frontmatter.load(source_full_path)
                if not 'public' in markdown_file.keys(): 
                    debug("    ==> Skipping file ('public' not defined)")
                    continue
                public_prop = markdown_file['public']

                if public_prop == False:
                    debug("    ==> Skipping file ('public' attribute set to false)")
                    continue
                
                if 'notbefore' in markdown_file.keys():
                    not_before_date = markdown_file['notbefore']
                    if not_before_date is None:
                        not_before_date = "<Value not found in document>"
                    if isinstance(not_before_date, str):
                        debug("    ==> Invalid 'notbefore' date found '{}', will be skipped".format(not_before_date))
                        continue
                    debug("    ==> Valid 'notbefore' date found'{}'".format(not_before_date))
                    if today < not_before_date:
                        debug("        - {}(today) < {} : will be skipped for current day".format(today, not_before_date))
                        continue            
            
            print("    copying to {}".format(destination_full_path))
            os.makedirs(os.path.dirname(destination_full_path), exist_ok=True)
            shutil.copyfile(source_full_path, destination_full_path)

def clean_dir(destination):
    if os.path. exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)




if __name__ == "__main__":
    clean_dir(destination)
    copy_files(source, destination)