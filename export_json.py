import bpy
import os
import json
from collections import OrderedDict
import copy

print('\n'*10)
curve_name = 'BezierCircle.002'
frames = 480
print(curve_name, frames)

currPath = os.path.splitext(bpy.data.filepath)[0]+".json"
with open(currPath, 'w', encoding="utf-8") as make_file:

    blending_speed = 0.01
    data_type = 1
    frame_per_second  = 60
    keys_ = [] # this is where coordinates goes in
    loop_behavior = 1
    name_ = 'move'
    property_ = 'position'
    ranges_ = []
        
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
                    
                    inside_keys = OrderedDict()
                    inside_keys["frame"] = fr
                    
                    co_array = []
                    co = copy.deepcopy(spline.bezier_points[x].co)
                    co *= 10
                    print("%.3f " % (co.y)) 
                    print("%.3f " % (-co.x)) 
                    print("%.3f " % (co.z))
                    co_array += [-co.x, co.z, co.y]
                    co_array += [[0, 0, 0]]
                    
                    inside_keys["values"] = co_array
                    
                    keys_.append(inside_keys)
                # last frame
                fr = frames
                    
                inside_keys = OrderedDict()
                inside_keys["frame"] = fr
                
                co_array = []
                co = copy.deepcopy(spline.bezier_points[0].co)
                co *= 10
                print("%.3f " % (co.y)) 
                print("%.3f " % (-co.x)) 
                print("%.3f " % (co.z))
                co_array += [-co.x, co.z, co.y]
                co_array += [[0, 0, 0]]
                
                inside_keys["values"] = co_array
                
                keys_.append(inside_keys)
    
                    
        
    ordered_dict = OrderedDict()
    ordered_dict['blendingSpeed'] = blending_speed
    ordered_dict['dataType'] = data_type
    ordered_dict['framePerSecond'] = frame_per_second
    ordered_dict['keys'] = keys_
    ordered_dict['loopBehavior'] = loop_behavior
    ordered_dict['name'] = name_
    ordered_dict['property'] = property_
    ordered_dict['ranges'] = ranges_
    
    animation_dict = {"animations":[ordered_dict]}
    
    json.dump(animation_dict, make_file, ensure_ascii=False, indent="\t")
    
                    
                    
                    







