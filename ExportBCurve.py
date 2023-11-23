import bpy
import os

currPath = os.path.splitext(bpy.data.filepath)[0]+".txt"
file = open(currPath, "w") 
print('\n'*10)
print("file written.")

#objects = bpy.data.objects
curves = bpy.data.curves

### Young: WIP. find curve object automatically
#for object in objects:
#    print(object.name)
curve_obj = bpy.data.objects.get('Curve', None)

### Young: find curves
for curve in curves:
    print(curve.asset_data)
    for spline in curve.splines:
        for x in range(len(spline.bezier_points)):
            file.write("p ")
            
            print(curve_obj.matrix_world)
            print(spline.bezier_points[x].handle_left)
            
#            handle_left = curve_obj.matrix_world * spline.bezier_points[x].handle_left
#            handle_left *= 11
            
#            co = curve_obj.matrix_world * spline.bezier_points[x].co
#            co *= 11
            co = spline.bezier_points[x].co
            
#            handle_right = curve_obj.matrix_world * spline.bezier_points[x].handle_right
#            handle_right *= 11
            
#            file.write("%.3f " % (handle_left.y))
#            file.write("%.3f " % (-handle_left.x))
#            file.write("%.3f " % (handle_left.z)) 
            file.write("%.3f " % (co.y)) 
            file.write("%.3f " % (-co.x)) 
            file.write("%.3f " % (co.z))
#            file.write("%.3f " % (handle_right.y))
#            file.write("%.3f " % (-handle_right.x)) 
#            file.write("%.3f " % (handle_right.z))
            file.write("\n")
    file.write("n\n")
file.close()















'''

# Specify the name of the child curve object
child_curve_name = 'BezierCircle.002'

# Get the current scene
current_scene = bpy.context.scene

# Iterate through all objects in the scene
for obj in current_scene.objects:
    print(obj)
    # Check if the object is a curve and has the specified name
    if obj.type == 'CURVE':
        print("Object Curve Found")
        if obj.children:
            print(f"Found child curve object: {obj.name}")
        else:
            print(f"CANNOT FIND")
else:
    print(f"Child curve object with name '{child_curve_name}' not found.")
print("done")





bc_name = 'BezierCircle.002'

# Try to find the curve object by name in the active scene
curve_obj = bpy.data.objects.get('Curve', None)

if curve_obj:
    # Find the child curve object recursively
    child_curve_object = find_child_by_name(curve_obj, bc_name)

    # Check if the child curve object is found
    if child_curve_object:
        print(f"Found child curve object: {curve_obj.name}")
    else:
        print(f"Child curve object with name '{bc_name}' not found.")
else:
    print("Parent object 'Curve' not found.")

for child_obj in curve_obj.children:
    print(child_obj)


#bc_name = 'Curve to mesh(XYZ)'

ob = bpy.data.objects.get(bc_name, None)
ob = bpy.data.objects.get(bc_name)

print(ob)
b_c = getChildren(ob)
print(b_c)


'''