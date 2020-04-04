import os
import time
from ftplib import FTP


def prune():
    # Login
    host = input("Server address?")
    user = input("Username?")
    passwd = input("Password?")
    ftp = FTP(host=host, user=user, passwd=passwd)
    # While there are no .mca files in the current directory prompt the user to change directory
    file_list = ftp.nlst()
    while len([True for i in file_list if ".mca" in i]) == 0:
        if len(file_list) == 1:
            # Only one choice, don't wait for the user to make it
            ftp.cwd(file_list[0])
            print("Auto cd to %s" % file_list[0])
        else:
            print(file_list)
            new_dir = input("Please select the directory to change to!")
            try:
                ftp.cwd(new_dir)
            except:
                print("An error occurred!")
        file_list = ftp.nlst()
    print("Reached working directory! Starting!")
    # Timing
    start_time = time.time()
    # Ask for bounds
    min_x = int(input("Minimum x to keep?"))
    min_z = int(input("Minimum z to keep?"))
    max_x = int(input("Maximum x to keep?"))
    max_z = int(input("Maximum z to keep?"))
    # Create directories for moving files (if not already existent)
    if "delete" not in file_list:
        ftp.mkd("delete/")
    # Initialize stats
    num_deleted = 0
    num_kept = 0
    size_deleted = 0
    size_kept = 0
    num_total = 0
    size_total = 0
    # Print some stuff to show this is doing something
    print("Found %i files, starting to work!" % len(file_list))
    # Loop over files, this assumes the names have not been changed
    for file in file_list:
        if ".mca" in file:
            # File names are in the format "r.x.z.mca"  -> Split and extract
            x = int(file.split(".")[1])
            z = int(file.split(".")[2])
            # Convert Region coordinates to game coordinates (Each regions contains 32x32 chunks with 16x16 blocks)
            coord_x = x * 16 * 32
            coord_z = z * 16 * 32
            # Size (for stats)
            try:
                size = ftp.size(file)
            except:
                size = 1
            size_total += size
            num_total += 1
            # Check bounds, addition for min_ is added as the region file x and z coordinate are rounded down
            # Therefor region 0|0 can contain blocks up to 511|511, the addition is to keep these regions
            if min_x < coord_x + 16 * 32 and max_x > coord_x and min_z < coord_z + 16 * 32 and max_z > coord_z:
                # Region is in bounds
                num_kept += 1
                size_kept += size
                # ftp.rename(file, "keep/" + file)
            else:
                # Region is out of bounds
                num_deleted += 1
                size_deleted += size
                ftp.rename(file, "delete/" + file)
            print("Deleted %i, kept %i, %2.1f%% done" % (num_deleted, num_kept, num_total/len(file_list)*100))
    # End FTP connection
    try:
        # Be polite
        ftp.quit()
    except:
        # Skrew the server
        ftp.close()
    # Time stats
    elaped_time = time.time() - start_time
    # Print stats
    print("Deleted %i/%i files (%2.1f%%)" % (num_deleted, num_total, num_deleted / num_total * 100))
    print("Cleared %.3f/%.3f GB (%2.1f%%) - Reduced size to %.3f GB" %
          (size_deleted / 1024 / 1024 / 1024, size_total / 1024 / 1024 / 1024, size_deleted / size_total * 100,
           size_kept / 1024 ** 3))
    print("Took %.1fs" % elaped_time/1000000)
    # Keep console open until the user decides to close it
    _ = input("Press any key to exit!")


if __name__ == "__main__":
    prune()
