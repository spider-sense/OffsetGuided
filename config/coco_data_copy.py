"""
Configuration for COCO Dataset: keypoint, skeleton and keypoint jitter sigmas
Copied from openpifpaf
"""
import logging
from config import heatmap_hflip, offset_hflip, vector_hflip, HFLIP


LOG = logging.getLogger(__name__)

ANNOTATIONS_TRAIN = 'data/link2COCO2017/annotations/person_keypoints_train2017.json'
ANNOTATIONS_VAL = 'data/link2COCO2017/annotations/person_keypoints_val2017.json'
IMAGE_DIR_TRAIN = 'data/link2COCO2017/train2017'
IMAGE_DIR_VAL = 'data/link2COCO2017/val2017'

ANNOTATIONS_TESTDEV = 'data/link2COCO2017/annotations_trainval_info/image_info_test-dev2017.json'
ANNOTATIONS_TEST = 'data/link2COCO2017/annotations_trainval_info/image_info_test2017.json'
IMAGE_DIR_TEST = 'data/link2COCO2017/test2017/'

COCO_PERSON_SKELETON = [
    (0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (5, 6), (4, 6), (3, 5),
    (5, 7), (7, 9), (6, 8), (8, 10), (5, 11), (6, 12), (11, 12), (11, 13),
    (13, 15), (12, 14), (14, 16)]

COCO_PERSON_SKELETON_DOWNUP = [  # after simulation, we get the same results as COCO_PERSON_SKELETON
    (15, 13), (13, 11), (16, 14), (14, 12), (11, 12), (5, 11), (6, 12),
    (5, 6), (5, 7), (6, 8), (7, 9), (8, 10), (1, 2),
    (0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6)]

COCO_PERSON_WITH_REDUNDANT_SKELETON = [
    (0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (5, 6), (4, 6), (3, 5),
    (5, 7), (7, 9), (6, 8), (8, 10), (5, 11), (6, 12), (11, 12), (11, 13),
    (13, 15), (12, 14), (14, 16),
    (1, 5), (2, 6), (5, 12), (6, 11), (11, 14), (12, 13),
    (5, 9), (6, 10), (11, 15), (12, 16),
    (5, 0), (6, 0)]

DENSER_COCO_PERSON_SKELETON = [
    (0, 1), (0, 2), (1, 2), (0, 3), (0, 4), (3, 4), (0, 5), (0, 6), (1, 5),
    (2, 6), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6), (5, 11), (6, 12), (5, 12),
    (6, 11), (11, 12), (5, 7), (6, 8), (7, 9), (8, 10), (5, 9), (6, 10), (7, 8),
    (9, 10), (9, 11), (10, 12), (9, 13), (10, 14), (13, 11), (14, 12),
    (11, 14), (12, 13), (11, 15), (12, 16), (15, 13), (16, 14),
    (13, 16), (14, 15), (13, 14), (15, 16)]

REDUNDANT_CONNECTIONS = [
    c
    for c in DENSER_COCO_PERSON_SKELETON
    if c not in COCO_PERSON_SKELETON
]

KINEMATIC_TREE_SKELETON = [
    (0, 1), (1, 3),  # left head
    (0, 2), (2, 4),
    (0, 5),
    (5, 7), (7, 9),  # left arm
    (0, 6),
    (6, 8), (8, 10),  # right arm
    (5, 11), (11, 13), (13, 15),  # left side
    (6, 12), (12, 14), (14, 16),
]


COCO_KEYPOINTS = [
    'nose',  # 0
    'left_eye',  # 1
    'right_eye',  # 2
    'left_ear',  # 3
    'right_ear',  # 4
    'left_shoulder',  # 5
    'right_shoulder',  # 6
    'left_elbow',  # 7
    'right_elbow',  # 8
    'left_wrist',  # 9
    'right_wrist',  # 10
    'left_hip',  # 11
    'right_hip',  # 12
    'left_knee',  # 13
    'right_knee',  # 14
    'left_ankle',  # 15
    'right_ankle',  # 16
]

LEFT_INDEX = [i for i, v in enumerate(COCO_KEYPOINTS) if v.startswith('l')]
RIGHT_INDEX = [i for i, v in enumerate(COCO_KEYPOINTS) if v.startswith('r')]

COCO_PERSON_SIGMAS = [
    0.026,  # nose
    0.025,  # eyes
    0.025,  # eyes
    0.035,  # ears
    0.035,  # ears
    0.079,  # shoulders
    0.079,  # shoulders
    0.072,  # elbows
    0.072,  # elbows
    0.062,  # wrists
    0.062,  # wrists
    0.107,  # hips
    0.107,  # hips
    0.087,  # knees
    0.087,  # knees
    0.089,  # ankles
    0.089,  # ankles
]


def draw_skeletons():
    import numpy as np
    from visualization import show
    coordinates = np.array([[
        [0.0, 9.3, 2.0],  # 'nose',
        [-0.5, 9.7, 2.0],  # 'left_eye',
        [0.5, 9.7, 2.0],  # 'right_eye',
        [-1.0, 9.5, 2.0],  # 'left_ear',
        [1.0, 9.5, 2.0],  # 'right_ear',
        [-2.0, 8.0, 2.0],  # 'left_shoulder',
        [2.0, 8.0, 2.0],  # 'right_shoulder',
        [-2.5, 6.0, 2.0],  # 'left_elbow',
        [2.5, 6.2, 2.0],  # 'right_elbow',
        [-2.5, 4.0, 2.0],  # 'left_wrist',
        [2.5, 4.2, 2.0],  # 'right_wrist',
        [-1.8, 4.0, 2.0],  # 'left_hip',
        [1.8, 4.0, 2.0],  # 'right_hip',
        [-2.0, 2.0, 2.0],  # 'left_knee',
        [2.0, 2.1, 2.0],  # 'right_knee',
        [-2.0, 0.0, 2.0],  # 'left_ankle',
        [2.0, 0.1, 2.0],  # 'right_ankle',
    ]])

    keypoint_painter = show.KeypointPainter(show_box=False, color_connections=True,
                                            markersize=1, linewidth=6)

    with show.canvas('../docs/skeleton_coco.png', figsize=(2, 5)) as ax:
        ax.set_axis_off()
        keypoint_painter.keypoints(ax, coordinates, skeleton=COCO_PERSON_SKELETON)

    with show.canvas('../docs/skeleton_kinematic_tree.png', figsize=(2, 5)) as ax:
        ax.set_axis_off()
        keypoint_painter.keypoints(ax, coordinates, skeleton=KINEMATIC_TREE_SKELETON)

    with show.canvas('../docs/skeleton_coco_redundant.png', figsize=(2, 5)) as ax:
        ax.set_axis_off()
        keypoint_painter.keypoints(ax, coordinates, skeleton=COCO_PERSON_WITH_REDUNDANT_SKELETON)


def print_associations():
    print('number of limb connections: ', len(COCO_PERSON_SKELETON))
    for j1, j2 in COCO_PERSON_SKELETON:
        print(COCO_KEYPOINTS[j1], '-', COCO_KEYPOINTS[j2])


if __name__ == '__main__':
    # for examination
    print(LEFT_INDEX)
    print(RIGHT_INDEX)
    print_associations()
    draw_skeletons()

    print(f'hflip indices of keypoints: {heatmap_hflip(COCO_KEYPOINTS, HFLIP)} \n')
    vector_hflip(COCO_KEYPOINTS, COCO_PERSON_SKELETON, HFLIP)
    print(REDUNDANT_CONNECTIONS)
    vector_hflip(COCO_KEYPOINTS, COCO_PERSON_WITH_REDUNDANT_SKELETON, HFLIP)
