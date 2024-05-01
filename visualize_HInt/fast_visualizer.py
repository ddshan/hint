# Copyright (c) OpenMMLab. All rights reserved.
import cv2


class FastVisualizer:
    """MMPose Fast Visualizer.

    A simple yet fast visualizer for video/webcam inference.

    Args:
        metainfo (dict): pose meta information
        radius (int, optional)): Keypoint radius for visualization.
            Defaults to 6.
        line_width (int, optional): Link width for visualization.
            Defaults to 3.
        kpt_thr (float, optional): Threshold for keypoints' confidence score,
            keypoints with score below this value will not be drawn.
            Defaults to 0.3.
    """

    def __init__(self, metainfo, radius=2, line_width=3, kpt_thr=0.05):
        self.radius = radius
        self.line_width = line_width
        self.kpt_thr = kpt_thr

        self.keypoint_id2name = metainfo['keypoint_id2name']
        self.keypoint_name2id = metainfo['keypoint_name2id']
        self.keypoint_colors = metainfo['keypoint_colors']
        self.skeleton_links = metainfo['skeleton_links']
        self.skeleton_link_colors = metainfo['skeleton_link_colors']


    def draw_pose_new(self, img, instances):
        if instances is None:
            print('no instance detected')
            return

        if hasattr(instances, "keypoints"):
            keypoints = instances.keypoints
            scores = instances.keypoint_scores
            bbox = instances.bbox
          
        else:
            keypoints = instances["keypoints"]
            scores = instances["keypoint_scores"]
            bbox = instances["bbox"]
           
        h, w, c = img.shape
        scale =  max(1, h // 500)    

        bbox = bbox[0][0]
        bbox_w = int(bbox[3] - bbox[1])
        bbox_h = int(bbox[2] - bbox[0])
        scale  = max((max(bbox_h, bbox_w) // 125), 1)

        scale = min(max(scale, 1), 3)
       

        for kpts, score in zip(keypoints, scores):
            for sk_id, sk in enumerate(self.skeleton_links):
                # if score[sk[0]] < self.kpt_thr or score[sk[1]] < self.kpt_thr:
                #     pass
                pos1 = (int(kpts[sk[0], 0]), int(kpts[sk[0], 1]))
                pos2 = (int(kpts[sk[1], 0]), int(kpts[sk[1], 1]))
                color = self.skeleton_link_colors[sk_id].tolist()
                color.reverse()
                cv2.line(img, pos1, pos2, color, thickness=int(self.line_width*scale))

            for kid, kpt in enumerate(kpts):
                x_coord, y_coord = int(kpt[0]), int(kpt[1])

                jpont_color = self.keypoint_colors[kid].tolist()
                jpont_color.reverse()

                if score[kid] < self.kpt_thr:
                    color = [0, 0, 0]
                    # cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, color, -1)
                    # cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, (255, 255, 255), thickness=int(scale))
                    cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, color, -1)
                    cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, jpont_color, thickness=int(scale*2))

                else:
                    
                    
                    cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, (255, 255, 255), -1)
                    cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, jpont_color, thickness=int(scale*2))
       


    def draw_pose(self, img, instances):
        """Draw pose estimations on the given image.

        This method draws keypoints and skeleton links on the input image
        using the provided instances.

        Args:
            img (numpy.ndarray): The input image on which to
                draw the pose estimations.
            instances (object): An object containing detected instances'
                information, including keypoints and keypoint_scores.

        Returns:
            None: The input image will be modified in place.
        """

        if instances is None:
            print('no instance detected')
            return
        

        if hasattr(instances, "keypoints"):
            keypoints = instances.keypoints
            scores = instances.keypoint_scores
            bbox = instances.bbox
            # ajds = instances.keypoint_ajds
            # if hasattr(instances, "gbs"):
            #     gbs = instances.keypoint_gbs
            # else:
            #     gbs = [None] * len(instances.keypoints)
        else:
            keypoints = instances["keypoints"]
            scores = instances["keypoint_scores"]
            bbox = instances["bbox"]
            # ajds = instances["keypoint_ajds"]
            # if "keypoint_gbs" in instances:
            #     gbs = instances["keypoint_gbs"]
            # else:
            #     gbs = [None] * len(keypoints)

        # keypoints = instances.keypoints
        # scores = instances.keypoint_scores

        # set the scale more intelligently
        h, w, c = img.shape
        scale =  max(1, h // 500)    

        bbox = bbox[0][0]
        bbox_w = int(bbox[3] - bbox[1])
        bbox_h = int(bbox[2] - bbox[0])
        scale  = max((max(bbox_h, bbox_w) // 150), 1)
        # print(scale)

        for kpts, score in zip(keypoints, scores):
            for sk_id, sk in enumerate(self.skeleton_links):
                if score[sk[0]] < self.kpt_thr or score[sk[1]] < self.kpt_thr:
                    # skip the link that should not be drawn
                    continue

                pos1 = (int(kpts[sk[0], 0]), int(kpts[sk[0], 1]))
                pos2 = (int(kpts[sk[1], 0]), int(kpts[sk[1], 1]))

                color = self.skeleton_link_colors[sk_id].tolist()
                color.reverse()
                cv2.line(img, pos1, pos2, color, thickness=int(self.line_width*scale))

            for kid, kpt in enumerate(kpts):
                if score[kid] < self.kpt_thr:
                    # skip the point that should not be drawn
                    continue

                x_coord, y_coord = int(kpt[0]), int(kpt[1])

                color = self.keypoint_colors[kid].tolist()
                color.reverse()
                cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, color, -1)
                cv2.circle(img, (int(x_coord), int(y_coord)), self.radius*scale, (255, 255, 255), thickness=int(scale))
       
        # draw bbox
        # cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color=(255, 255, 255), thickness=int(scale))