from types import new_class
import numpy as np
import math
import random

def rotate(cut_points, part, theta):
    part = np.array(list(part))
    part = np.transpose(part)
    new_part = np.zeros(part.shape, np.int)
    c = [int((part[0].max()+part[0].min())/2), int((part[1].max()+part[1].min())/2)]
    cos = math.cos(theta/180*math.pi)
    sin = math.sin(theta/180*math.pi)

    new_part[0] = ((part[0]-c[0])*cos - (part[1]-c[1])*sin + c[0]).astype(int)
    new_part[1] = ((part[0]-c[0])*sin + (part[1]-c[1])*cos + c[1]).astype(int)

    new_part = np.transpose(new_part)
    new_set = set()
    for i in range(new_part.shape[0]):
        new_set.add(tuple(new_part[i]))
    new_cut_points = set()
    for cp in cut_points:
        new_cut_points.add((int((cp[0]-c[0])*cos-(cp[1]-c[1])*sin+c[0]), int((cp[0]-c[0])*sin+(cp[1]-c[1])*cos+c[1])))
    new_cut_points = list(new_cut_points)
    return new_cut_points, new_set

def scale(cut_points, part, s1, s2):
    part = np.array(list(part))
    new_part = np.array(part, np.int)
    new_part[:,0] = (part[:,0]-part[:,0].min())*s1+part[:,0].min()
    new_part[:,1] = (part[:,1]-part[:,1].min())*s2+part[:,1].min()
    new_set = set()
    for i in range(new_part.shape[0]):
        new_set.add(tuple(new_part[i]))
    new_cut_points = set()
    for cp in cut_points:
        new_cut_points.add((int(cp[0]*s1), int(cp[1]*s2)))
    new_cut_points = list(new_cut_points)
    return new_cut_points, new_set

def transform(cut_points_list, parts):
    trans_parts = []
    trans_cut_points = []
    theta_range = [-10, 10]
    scale_range = [0.8, 1.2]
    for part in parts:
        cut_points = []
        for cp in cut_points_list:
            if tuple(cp) in part:
                cut_points.append(cp)
        theta = random.uniform(theta_range[0], theta_range[1])
        scale1 = random.uniform(scale_range[0], scale_range[1])
        scale2 = random.uniform(scale_range[0], scale_range[1])
        # theta, scale1, scale2 = 0, 2, 1
        # print(theta, scale1, scale2)
        new_cut_points, new_part = rotate(cut_points, part, theta)
        new_cut_points, new_part = scale(new_cut_points, new_part, scale1, scale2)
        
        trans_parts.append(new_part)
        trans_cut_points.append(new_cut_points)
        return new_cut_points, new_part
    return 
