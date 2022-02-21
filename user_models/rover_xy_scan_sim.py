from pathlib import Path
from time import time

import math
import gprMax
from user_libs.GPRAntennaModels.GSSI import antenna_like_GSSI_1500

fn = Path(__file__)

x_range = 0.6985
y_range = 0.6985
z_range = 0.3

sim_resolution = 0.002

x_profile_step_size = 0.005
y_profile_step_size = 0.005
antenna_height_from_halfspace = 0.005

antenna_padding = 0.1
free_space_in_z = 0.1

x_profile_count = math.floor((x_range - (antenna_padding)) / x_profile_step_size)
y_profile_count = math.floor((y_range - (antenna_padding)) / y_profile_step_size)

print("Total profiles", x_profile_count * y_profile_count)

for x_profile in range(x_profile_count):
    for y_profile in range(y_profile_count):
        output_path_data = fn.parent / ('rover_sim_' + str(int(time()))) / (fn.stem + '-x' + str(x_profile) + '-y' + str(y_profile))
        output_path_geometry = fn.parent / ('rover_sim_' + str(int(time()))) / (fn.stem + '-x' + str(x_profile) + '-y' + str(y_profile) + '-geometry')

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

        gssi_objects = antenna_like_GSSI_1500(antenna_padding + (x_profile * x_profile_step_size), antenna_padding + (y_profile * y_profile_step_size), (z_range - free_space_in_z) + antenna_height_from_halfspace, resolution=sim_resolution)
        for obj in gssi_objects:
            scene.add(obj)

        halfspace_m = gprMax.Material(er=5, se=0.001, mr=1, sm=0, id='concrete')
        scene.add(halfspace_m)

        halfspace = gprMax.Box(p1=(0, 0, 0), p2=(x_range, y_range, z_range - free_space_in_z), material_id='concrete')
        scene.add(halfspace)

        target_x_spacing = 0.1
        for x in range(6):
            x = x + 1
            target = gprMax.Cylinder(p1=(target_x_spacing * x, 0, 0.1), p2=(target_x_spacing * x, y_range, 0.1), r=0.010, material_id='pec');
            scene.add(target)

        gv = gprMax.GeometryView(p1=(0, 0, 0),
                                 p2=(x_range, y_range, z_range),
                                 dl=(sim_resolution, sim_resolution, sim_resolution),
                                 filename=output_path_geometry,
                                 output_type='n')


        scene.add(gv)

        gprMax.run(scenes=[scene], n=1, gpu=True, geometry_only=False, outputfile=output_path_data, autotranslate=True)
