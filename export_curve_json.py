import bpy
import os
import json
from collections import OrderedDict
import copy
import math
import numpy as np


print('\n'*10)
# Set the name of curve
curve_name = 'BezierCircle.002'
scale_size = 10
dec_round = 3

# Set the name of camera
camera_name = "Camera"
camera = bpy.data.objects.get(camera_name)

# Set the frame range
start_frame = 0
end_frame = bpy.context.scene.frame_end
print(camera_name, start_frame, end_frame)

# Set the json name
currPath = os.path.splitext(bpy.data.filepath)[0]+".json"

with open(currPath, 'w', encoding="utf-8") as make_file:   
    #objects = bpy.data.objects
    curves = bpy.data.curves

    '''
    Young: WIP. find curve object automatically
    Change the name 'Curve' -> into ?????
    '''
    #for object in objects:
    #    print(object.name)
    curve_obj = bpy.data.objects.get('Curve', None)

    ### Young: find curves
    path_handle_pairs = [] # this is where coordinates goes in
    for curve in curves:
        if curve.name == curve_name: # for one spline
            for spline in curve.splines:
                point_numbers = len(spline.bezier_points)
                print("the number of points are: ", point_numbers)
                
                for x in range(point_numbers):
                    
                    fr = end_frame/point_numbers * x
                    
                    # Young: The bezier curve actually starts at where it ends.
                    x = (x+point_numbers-1) % point_numbers
                    
                    # Young: make dict of coordinates and handles at each frame
                    cam_path_key = OrderedDict()
                    cam_path_key["frame"] = fr
                    
                    cam_path_handle_left_array = []
                    cam_path_handle_left = copy.deepcopy(spline.bezier_points[x].handle_left)
                    cam_path_handle_left *= scale_size
                    cam_path_handle_left_array += [np.round(cam_path_handle_left.x, dec_round), np.round(cam_path_handle_left.z, dec_round), np.round(cam_path_handle_left.y, dec_round)]
                    cam_path_key["l_handle"] = list(cam_path_handle_left_array)
                    
                    cam_path_co_array = []
                    cam_path_co = copy.deepcopy(spline.bezier_points[x].co)
                    cam_path_co *= scale_size
                    cam_path_co_array += [np.round(cam_path_co.x, dec_round), np.round(cam_path_co.z, dec_round), np.round(cam_path_co.y, dec_round)]
                    cam_path_key["values"] = list(cam_path_co_array)
                    
                    cam_path_handle_right_array = []
                    cam_path_handle_right = copy.deepcopy(spline.bezier_points[x].handle_right)
                    cam_path_handle_right *= scale_size
                    cam_path_handle_right_array += [np.round(cam_path_handle_right.x, dec_round), np.round(cam_path_handle_right.z, dec_round), np.round(cam_path_handle_right.y, dec_round)]
                    cam_path_key["r_handle"] = list(cam_path_handle_right_array)
                    
                    path_handle_pairs.append(cam_path_key)    
    ###-------------------------------------------------------------------------------------------###
    
    ### Young: find fovs (deprecated)
    '''
    # Create a list to store frame and fov pairs
    frame_fov_pairs = []

    # Iterate through the frames and extract the focal length
    for frame in range(start_frame, end_frame + 1):
        bpy.context.scene.frame_set(frame)

        if camera is not None and camera.type == 'CAMERA':
            fov_radians = camera.data.lens
            # sensor_width = camera.data.sensor_width
            # focal_length = camera.data.lens

            # # Calculate FOV using the formula
            # fov_radians = 2 * math.atan((sensor_width / 2) / focal_length)
            
            # Young: make dict of coordinates and handles at each frame
            fov_key = OrderedDict()
            fov_key["frame"] = frame
            fov_key["value"] = np.round(fov_radians, dec_round)
            
            frame_fov_pairs.append(fov_key)  
    '''
    ###-------------------------------------------------------------------------------------------###
    
    ### Young: find fovs more elegant way
    frame_fov_pairs = []
    action = camera.data.animation_data.action
    fl_curve = action.fcurves.find('lens')
    # Check if fl_curve exists
    if fl_curve is not None:
        # Extract keyframe points
        fl_keyframe_points = fl_curve.keyframe_points

        # Iterate through keyframe points
        for keyframe_point in fl_keyframe_points:
            frame = keyframe_point.co.x
            fl_key = OrderedDict()
            fl_key["frame"] = frame

            # If you want to get Bezier handles:
            fl_handle_left_array = [keyframe_point.handle_left.x, keyframe_point.handle_left.y]
            fl_handle_left_array = np.round(fl_handle_left_array, dec_round)
            fl_key["l_handle"] = list(fl_handle_left_array)
            
            value = keyframe_point.co.y
            fl_co_array = [frame, keyframe_point.co.y]
            fl_co_array = np.round(fl_co_array, dec_round)
            fl_key["values"] = list(fl_co_array)

            fl_handle_right_array = [keyframe_point.handle_right.x, keyframe_point.handle_right.y]
            fl_handle_right_array = np.round(fl_handle_right_array, dec_round)
            fl_key["r_handle"] = list(fl_handle_right_array)
            
            frame_fov_pairs.append(fl_key)
            
            ####
            '''
            Young:
            TRANSLATE FOCAL LENGTH INTO FOV
            This should be better conducted in the babylon process after drawing the bezier curve.
            '''
            ###
            
    ###-------------------------------------------------------------------------------------------###
    
    ### Young: find offset
    frame_offset_pairs = []
    action = camera.animation_data.action
    off_curve = action.fcurves.find('constraints["Follow Path"].offset')
    # Check if fl_curve exists
    if off_curve is not None:
        # Extract keyframe points
        off_keyframe_points = off_curve.keyframe_points

        # Iterate through keyframe points
        for keyframe_point in off_keyframe_points:
            frame = keyframe_point.co.x
            off_key = OrderedDict()
            off_key["frame"] = round(frame, dec_round)
            
            off_handle_left_array = [keyframe_point.handle_left.x, keyframe_point.handle_left.y]
            off_handle_left_array = np.round(off_handle_left_array, dec_round)
            off_key["l_handle"] = list(off_handle_left_array)
            
            value = keyframe_point.co.y
            off_co_array = [frame, keyframe_point.co.y]
            off_co_array = np.round(off_co_array, dec_round)
            off_key["values"] = list(off_co_array)

            off_handle_right_array = [keyframe_point.handle_right.x, keyframe_point.handle_right.y]
            off_handle_right_array = np.round(off_handle_right_array, dec_round)
            off_key["r_handle"] = list(off_handle_right_array)
            
            frame_offset_pairs.append(off_key)
  
    ###-------------------------------------------------------------------------------------------###
                    
        
    ordered_dict = OrderedDict()
    ordered_dict['cam_path_keys'] = path_handle_pairs
    ordered_dict['fov_keys'] = frame_fov_pairs
    ordered_dict['offset_keys'] = frame_offset_pairs
    
    
    
    json.dump(ordered_dict, make_file, ensure_ascii=False, indent="\t")
    print("JSON writing completed")