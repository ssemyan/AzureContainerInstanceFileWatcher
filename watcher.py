# Python 3.x
import time
import os

# code inspired by from https://askubuntu.com/questions/893019/monitor-folder-and-run-command-if-there-is-a-file-there

source = "/tmp/watch"
target = "/tmp/processed"
extensionToProcess = ".txt"

# Get initial list of files. Files are deemed new if not in this list (thus will ignore any existing files)
files1 = os.listdir(source)
print (f"Starting watcher on {source} with target {target}")

while True:
    time.sleep(2)
    files2 = os.listdir(source)
    # see if there are new files with the file extension we are looking for
    new = [f for f in files2 if all([not f in files1, f.endswith(extensionToProcess)])]

    # if so:
    for f in new:
        # combine paths and files
        src = os.path.join(source, f)
        
        # Normally we would do some sort of work to process the file, instead just mark the file as processed by adding '.processed' to the end of the filename
        trg = os.path.join(target, f) + ".processed"
        
        # move the file to target using mv command
        os.system("mv " + src + " " + trg)

        # write out to the console
        print(f"Processed file: {f}")
    
    files1 = files2