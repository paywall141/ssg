import os
import shutil

def recursive_copy(curr_dir, tar_dir):
    # check both exist here
    if not os.path.exists(curr_dir):
        raise ValueError(f"Provided directory {curr_dir} does not exist. Please double check input")
    if not os.path.exists(tar_dir):
        raise ValueError(f"Target directory {tar_dir} does not exist. Please double check purge_directory() is firing")
    for item in os.listdir(curr_dir):
        src_path = os.path.join(curr_dir, item)
        dest_path = os.path.join(tar_dir, item)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} -> {dest_path}")
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            # print(f"Creating {dest_path}")
            os.mkdir(dest_path)
            recursive_copy(src_path, dest_path)        

def purge_directory(tar_dir):
    if os.path.exists(tar_dir):
        print(f"Deleting {tar_dir} directory...no children will be spared.")
        shutil.rmtree(tar_dir)
    os.mkdir(tar_dir)

def copy_fs(curr_dir, tar_dir):
    purge_directory(tar_dir)
    recursive_copy(curr_dir, tar_dir)