from pathlib import Path

import gprMax
from user_libs.GPRAntennaModels.GSSI import antenna_like_GSSI_1500

fn = Path(__file__)

x_profile_step_size = 0.005
antenna_height_from_halfspace = 0.005

for x_profile in range(10):

    output_path_data = fn.parent / (fn.stem + '-x' + str(x_profile))
    output_path_geometry = fn.parent / (fn.stem + '-x' + str(x_profile) + '-geometry')

    scene = gprMax.Scene()
    title = gprMax.Title(name=fn.with_suffix('').name + '-x' + str(x_profile))
    domain = gprMax.Domain(p1=(0.6985, 0.6985, 0.3))
    dxdydz = gprMax.Discretisation(p1=(0.002, 0.002, 0.002))
    time_window = gprMax.TimeWindow(time=6e-9)

    scene.add(title)
    scene.add(domain)
    scene.add(dxdydz)
    scene.add(time_window)

    gssi_objects = antenna_like_GSSI_1500(0.1 + (x_profile * x_profile_step_size), 0.1, 0.2 + antenna_height_from_halfspace, resolution=0.002)
    for obj in gssi_objects:
        scene.add(obj)

    halfspace_m = gprMax.Material(er=5, se=0.001, mr=1, sm=0, id='concrete')
    scene.add(halfspace_m)

    halfspace = gprMax.Box(p1=(0, 0, 0), p2=(0.6985, 0.6985, 0.2), material_id='concrete')
    scene.add(halfspace)

    target_x_spacing = 0.1
    for x in range(6):
        x = x + 1
        target = gprMax.Cylinder(p1=(target_x_spacing * x, 0, 0.1), p2=(target_x_spacing * x, 0.6985, 0.1), r=0.010, material_id='pec');
        scene.add(target)

    gv = gprMax.GeometryView(p1=(0, 0, 0),
                             p2=(0.6985, 0.6985, 0.3),
                             dl=(0.002, 0.002, 0.002),
                             filename=output_path_geometry,
                             output_type='n')


    scene.add(gv)

    gprMax.run(scenes=[scene], n=1, gpu=True, geometry_only=False, outputfile=output_path_data, autotranslate=True)
