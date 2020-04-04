import os


def prune():
    min_x = int(input("Minimum x to keep?"))
    min_z = int(input("Minimum z to keep?"))
    max_x = int(input("Maximum x to keep?"))
    max_z = int(input("Maximum z to keep?"))

    if not os.path.exists("keep/"):
        os.mkdir("keep/")
    if not os.path.exists("delete/"):
        os.mkdir("delete/")
    num_deleted = 0
    num_kept = 0
    size_deleted = 0
    size_kept = 0
    num_total = 0
    size_total = 0
    for file in os.listdir():
        if ".mca" in file:
            # "r.-1.1.mca"
            x = int(file.split(".")[1])
            z = int(file.split(".")[2])
            coord_x = x * 16 * 32
            coord_z = z * 16 * 32
            size = os.path.getsize(file)
            size_total += size
            num_total += 1
            if min_x < coord_x + 16 * 32 and max_x > coord_x and min_z < coord_z + 16 * 32 and max_z > coord_z:
                # Region is in bounds
                num_kept += 1
                size_kept += size
                # os.rename(file, "keep/" + file)
            else:
                # Region is out of bounds
                num_deleted += 1
                size_deleted += size
                # os.rename(file, "delete/" + file)

    print("Deleted %i/%i files (%2.1f%%)" % (num_deleted, num_total, num_deleted / num_total * 100))
    print("Cleared %.3f/%.3f GB (%2.1f%%) - Reduced size to %.3f GB" %
          (size_deleted / 1024 / 1024 / 1024, size_total / 1024 / 1024 / 1024, size_deleted / size_total * 100,
           size_kept / 1024 ** 3))
    _ = input("Press any key to exit!")


if __name__ == "__main__":
    prune()
