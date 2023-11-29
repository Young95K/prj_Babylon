import bpy
import os
import json
from collections import OrderedDict
import copy

print('\n'*10)
curve_name = 'BezierCircle.002'
frames = 480
scale_size = 10
dec_round = 3
print(curve_name, frames, scale_size)

currPath = os.path.splitext(bpy.data.filepath)[0]+".json"
with open(currPath, 'w', encoding="utf-8") as make_file:
    keys_ = [] # this is where coordinates goes in
        
    #objects = bpy.data.objects
    curves = bpy.data.curves

    ### Young: WIP. find curve object automatically
    #for object in objects:
    #    print(object.name)
    curve_obj = bpy.data.objects.get('Curve', None)

    ### Young: find curves
    for curve in curves:
        if curve.name == curve_name: # for one spline
            for spline in curve.splines:
                point_numbers = len(spline.bezier_points)
                print("the number of points are: ", point_numbers)
                
                for x in range(point_numbers):
                    
                    fr = frames/point_numbers * x
                    
                    # Young: The bezier curve actually starts at where it ends.
                    x = (x+point_numbers-1) % point_numbers
                    
                    # Young: make dict of coordinates and handles at each frame
                    inside_keys = OrderedDict()
                    inside_keys["frame"] = fr
                    
                    handle_left_array = []
                    handle_left = copy.deepcopy(spline.bezier_points[x].handle_left)
                    handle_left *= scale_size
                    handle_left_array += [round(handle_left.x, dec_round), round(handle_left.z, dec_round), round(handle_left.y, dec_round)]
                    inside_keys["l_handle"] = handle_left_array
                    
                    co_array = []
                    co = copy.deepcopy(spline.bezier_points[x].co)
                    co *= scale_size
                    co_array += [round(co.x, dec_round), round(co.z, dec_round), round(co.y, dec_round)]
                    inside_keys["values"] = co_array
                    
                    handle_right_array = []
                    handle_right = copy.deepcopy(spline.bezier_points[x].handle_right)
                    handle_right *= scale_size
                    handle_right_array += [round(handle_right.x, dec_round), round(handle_right.z, dec_round), round(handle_right.y, dec_round)]
                    inside_keys["r_handle"] = handle_right_array
                    
                    keys_.append(inside_keys)    
                    
        
    ordered_dict = OrderedDict()
    ordered_dict['keys'] = keys_
    
    json.dump(ordered_dict, make_file, ensure_ascii=False, indent="\t")
    print("JSON writing completed")
    
                    
                    
                    







