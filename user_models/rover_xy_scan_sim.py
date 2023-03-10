from pathlib import Path
from time import time

import os
import sys

import math
import gprMax
from user_libs.GPRAntennaModels.GSSI import antenna_like_GSSI_1500

fn = Path(__file__)

x_range = 0.6985
y_range = 0.3000
z_range = 0.3

sim_resolution = 0.001

x_profile_step_size = 0.005
y_profile_step_size = 0.005
antenna_height_from_halfspace = 0

free_space_in_z = 0.1

output_scene_geometry = False

antenna_size_x = 0.17
antenna_size_y = 0.108
antenna_size_z = 0.045

antenna_padding_x = 0.005
antenna_padding_y = 0.005

target_count = 8

x_profile_count = math.floor((x_range - (antenna_padding_x * 2) - antenna_size_x) / x_profile_step_size)
y_profile_count = math.floor((y_range - (antenna_padding_y * 2) - antenna_size_y) / y_profile_step_size)

print("Number of x profiles", x_profile_count)
print("Number of y profiles", y_profile_count)

print("Max antenna center x position", x_profile_count * x_profile_step_size)
print("Max antenna center y position", y_profile_count * y_profile_step_size)

print("Total profiles", x_profile_count * y_profile_count)

suffix = sys.argv[1]

for y_profile in range(y_profile_count):
    for x_profile in range(x_profile_count):
        output_path_data = fn.parent / ('rover_sim_' + suffix) / (fn.stem + '-x' + str(x_profile) + '-y' + str(y_profile))
        output_path_geometry = fn.parent / ('rover_sim_' + suffix) / (fn.stem + '-x' + str(x_profile) + '-y' + str(y_profile) + '-geometry')

        if(os.path.isdir(output_path_data)):
            continue

        Path(output_path_data).mkdir(parents=True, exist_ok=True)

        scene = gprMax.Scene()
        title = gprMax.Title(name=fn.with_suffix('').name + '-x' + str(x_profile) + '-y' + str(y_profile))
        domain = gprMax.Domain(p1=(x_range, y_range, z_range))
        dxdydz = gprMax.Discretisation(p1=(sim_resolution, sim_resolution, sim_resolution))
        time_window = gprMax.TimeWindow(time=6e-9)

        scene.add(title)
        scene.add(domain)
        scene.add(dxdydz)
        scene.add(time_window)

        gssi_objects = antenna_like_GSSI_1500((antenna_size_x / 2) + (x_profile * x_profile_step_size) + antenna_padding_x, (antenna_size_y / 2) + (y_profile * y_profile_step_size) + antenna_padding_y, (z_range - free_space_in_z) + antenna_height_from_halfspace, resolution=sim_resolution)
        for obj in gssi_objects:
            print(obj)
            scene.add(obj)

        halfspace_m = gprMax.Material(er=5, se=0.001, mr=1, sm=0, id='concrete')
        scene.add(halfspace_m)

        halfspace = gprMax.Box(p1=(0, 0, 0), p2=(x_range, y_range, z_range - free_space_in_z), material_id='concrete')
        scene.add(halfspace)

        target_x_spacing = ((x_range - 0.1) / target_count)
        print("target x", target_x_spacing)
        for x in range(target_count):
            x = x + 1
            target = gprMax.Cylinder(p1=(target_x_spacing * x, 0, 0.1), p2=(target_x_spacing * x, y_range, 0.1), r=0.010, material_id='pec');
            scene.add(target)

        gv = gprMax.GeometryView(p1=(0, 0, 0),
                                 p2=(x_range, y_range, z_range),
                                 dl=(0.002, 0.002, 0.002),
                                 filename=output_path_geometry,
                                 output_type='n')

        if(output_scene_geometry):
            scene.add(gv)

        try:
            gprMax.run(scenes=[scene], n=1, gpu=True, geometry_only=False, outputfile=output_path_data)
        except Exception as e:
            print("Unable to generate profile for x, y", x_profile, y_profile)
            print(e)
