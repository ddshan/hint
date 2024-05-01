import pickle, os, glob, json, cv2, sys, random, shutil, argparse
random.seed(0)
import numpy as np
from tqdm import tqdm

from utils import parse_pose_metainfo
from coco_wholebody_hand import dataset_info
from fast_visualizer import FastVisualizer


def get_dataset_meta():
    sys.path.append('.')
    metainfo = parse_pose_metainfo(dataset_info)
    return metainfo


def draw_hand_skeleton_new(image_path, keypoint_ls):
    '''Draw one hand per image
    '''
    if len(keypoint_ls) == 1: 
        im = cv2.imread(image_path)
        bbox = keypoint_ls[0]['bbox'][0]
        instance = {}
        instance['keypoints'] = []
        instance['keypoint_scores'] = []
        instance['bbox'] = []
        instance['keypoints'].append( np.array(keypoint_ls[0]['keypoints']) )
        instance['bbox'].append( np.array(keypoint_ls[0]['bbox'])  )
        instance['keypoint_scores'].append( 1-np.array(keypoint_ls[0]['occlusion']) )
      
        fv = FastVisualizer(metainfo=get_dataset_meta(), radius=5, line_width=2, kpt_thr=0.5)
        fv.draw_pose_new(im, instance)

    else:
        print(len(keypoint_ls))

    return im, bbox



if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("--hint_root",  default='/path/to/HInt_annotation')
    args = parser.parse_args()
    print(args)

    vid_dir  = f'{args.hint_root}/TEST_ego4d_img' # choose a subset to visualize
    save_dir = './vis_HInt'
    os.makedirs(save_dir, exist_ok=True)
    
    frame_ls = glob.glob(f'{vid_dir}/*.jpg') 
    print(len(frame_ls))
    for frame_path in frame_ls:
        frame_name = os.path.split(frame_path)[-1]
        json_path = frame_path[:-4]+'.json'
        if os.path.exists(json_path):
            kp = json.load(open(json_path, 'r'))
            im, _ = draw_hand_skeleton_new(frame_path, kp)
            
            save_path = os.path.join(save_dir, frame_name[:-4]+'_plot.jpg')
            cv2.imwrite(save_path, im)
            print(save_path)
            