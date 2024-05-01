
import os, glob, random, cv2, pdb, imageio, json, multiprocessing, shutil, sys, argparse, hashlib, zipfile, time
import numpy as np
from PIL import Image
from tqdm import tqdm
random.seed(0)


def decode_video(video_path, save_dir, video_name):
    os.makedirs(save_dir, exist_ok=True)
    cmd = f"ffmpeg -loglevel error -i {video_path} -qscale:v 1 '{save_dir}/{video_name}_%10d.jpg'"

    os.system(cmd)
    print(f"{video_path}, #frames={len(os.listdir(save_dir))}")



def get_md5(file_path):
    filehash = hashlib.md5()
    filehash.update(open(file_path, 'rb').read())
    md5 = filehash.hexdigest()
    print(f'md5 for {file_path}: {md5}')
    return md5


def compare_md5_with_origin(file_path):
    origin_md5 = '4c47fc4e3657274713db7aaf3a890037'
    new_md5   = get_md5(file_path)

    if origin_md5 == new_md5:
        print(f'origin mds: {origin_md5}')
        print(f'{file_path  }: {new_md5}')
        print("MD5 verified successfully! Now, you can use HInt for your tasks.")
    else:
        print("MD5 verification failed! Please check in detail for possible issues. Before you use HInt, make sure you pass the verification first.")


def create_deterministic_zip(folder_to_zip, output_zip_file):
    with zipfile.ZipFile(output_zip_file, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in sorted(os.walk(folder_to_zip)):
            # Sort files to ensure consistent order
            files.sort()
            print(f'{root}, files len = {len(files)},')
            for file in files:
                file_path = os.path.join(root, file)
                
                # Ensure consistent permissions
                os.chmod(file_path, 0o644)

                # Ensure consistent timestamps
                t = "24 Apr 2024 10:10:10"
                t_obj = time.strptime(t, "%d %b %Y %H:%M:%S") 
                file_timestamp = int(time.mktime(t_obj))
                os.utime(file_path, (file_timestamp, file_timestamp))
                
                # Add file to zip with relative path under dataset folder
                relative_path = os.path.relpath(file_path, folder_to_zip)
                archive_path = os.path.join('HInt_annotation', relative_path)
                zipf.write(file_path, archive_path)
    


def check_number_of_files(hint_dir):
    folder_ls = os.listdir(hint_dir)
    folder_ls.sort()
    folder_dict = {'TEST_ego4d_img': 3428, 'TEST_ego4d_seq': 13906, 'TEST_epick_img': 3812, 'TEST_newdays_img': 3508,\
        'TRAIN_ego4d_img': 23304, 'TRAIN_epick_img': 5560, 'TRAIN_newdays_img': 19332,\
        'VAL_ego4d_img': 1028, 'VAL_ego4d_seq': 4640, 'VAL_epick_img': 1250, 'VAL_newdays_img': 1100}
    
    for folder in folder_ls:
        cur_num = len(glob.glob(f'{hint_dir}/{folder}/*.jpg') + glob.glob(f'{hint_dir}/{folder}/*.json'))
        if cur_num != folder_dict[folder]:
            print(f'The mumber of files under {folder} does not match! Current is {cur_num}, should be {folder_dict[folder]}')
            return False

    print(f'The mumber of files all match with original HInt!')
    return True



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, required=True)
    parser.add_argument("--ego4d_root", default='/path/to/ego4d_data/v1')
    parser.add_argument("--hint_root",  default='/path/to/HInt_annotation_partial')
    args = parser.parse_args()
    print(args)
    assert args.task in ['decode_clips', 'retrieve_frames', 'verify_hint'], f"Error: not recognize task called, {args.task}. Choose one task in ['decode_clips', 'retrieve_frames', 'verify_hint']"
    
    clips_dir = f'{args.ego4d_root}/clips'
    frames_dir = f'{args.ego4d_root}/clips_decode'
    hint_root_partial = args.hint_root
    hint_root_full = hint_root_partial.replace('HInt_annotation_partial', 'HInt_annotation')

    if args.task == 'decode_clips':

        clip_ls = glob.glob(f'{clips_dir}/*.mp4')
        os.makedirs(frames_dir, exist_ok=True)

        # used clips in HInt
        clip_names_path = 'ego4d_clip_names.json'
        with open(clip_names_path, 'r') as f:
            used_clip_ls = json.load(f)
        print('used clips: ', len(used_clip_ls))
    
        # only keep used clips 
        clip_ls = [item for item in clip_ls if os.path.split(item)[-1] in used_clip_ls]
        print(f'clip_ls : ', len(clip_ls))

        for clip_path in tqdm(clip_ls):
            clip_name = clip_path.split('/')[-1][:-4]
            save_dir = os.path.join(frames_dir, clip_name)
            decode_video(clip_path, save_dir, clip_name) 

        ## if you find the for loop is too slow, you can uncomment and use multiprocessing to decode videos
        # def handle(clip_path):
        #     clip_name = clip_path.split('/')[-1][:-4]
        #     save_dir = os.path.join(frames_dir, clip_name)
        #     decode_video(clip_path, save_dir, clip_name)
        # P = multiprocessing.Pool(24)
        # P.map(handle, clip_ls)      



    elif args.task == 'retrieve_frames':

        if not os.path.exists(frames_dir):
            print(f'Decoded Ego4D frames dir not exist: {frames_dir}')
            breakpoint()

        folder_ls = ['TRAIN_ego4d_img', 'VAL_ego4d_img', 'VAL_ego4d_seq', 'TEST_ego4d_img', 'TEST_ego4d_seq']
        with open('ego4d_frame_names.json', 'r') as f:
            ego4d_frame_names = json.load(f)
            for subset in folder_ls:
                frame_ls = ego4d_frame_names[subset]
                dst_dir = os.path.join(hint_root_partial, subset)
                os.makedirs(dst_dir, exist_ok=True)

                for frame_name in tqdm(frame_ls):
                    clip_id, action_id, clip_frame_num, frame_type_part1, frame_type_part2, hand_side = frame_name.split('_')
                    src = os.path.join(frames_dir, clip_id, f'{clip_id}_{int(clip_frame_num)+1:0>10}.jpg')
                    dst =  os.path.join(hint_root_partial, subset, frame_name)

                    if os.path.exists(src):
                        shutil.copy(src, dst)

                    else:
                        print(f'src frame not exist: {src}')
                        breakpoint()

        # checking if number of files match with with originl HInt
        if check_number_of_files(hint_root_partial):

            # update folder name from "HInt_annotation_partial" to "HInt_annotation"
            print(f"Update folder name from {hint_root_partial} -> {hint_root_full} !")
            os.rename(hint_root_partial, hint_root_full)
        
        else:
            print(f'The number of files does not match with original HInt.')

                    

    elif args.task == 'verify_hint':

        folder_to_zip = hint_root_full
        output_zip    = hint_root_full+'.zip'
        print(f'create zip file for {folder_to_zip}')
        create_deterministic_zip(folder_to_zip, output_zip)
        print(f'saved zip file  at {output_zip}')
        compare_md5_with_origin(output_zip)



        
    



        


    
        

