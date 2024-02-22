import yaml
import drawsvg
from tagdef.tag25h9 import tag25h9
from tagdef.tag36h11 import tag36h11
from tagdef.tag16h5 import tag16h5
import argparse
import os
tag_generator_dict = {
    "tag25h9": tag25h9,
    "tag36h11": tag36h11,
    "tag16h5": tag16h5
}


# get params from comandline params
# tag_family = "tag25h9"
# tag_size = 2
# row = 5
# col = 7
# tag_spacing = 0.5
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--tag_family", required=True,)
ap.add_argument("-s", "--tag_size", required=True,)
ap.add_argument("-r", "--row", required=True,)
ap.add_argument("-c", "--col", required=True,)
ap.add_argument("-t", "--tag_spacing", required=True,)
ap.add_argument("-o", "--output", required=False, default="apriltag_board")
ap.add_argument("-ds", "--draw_spacing", required=False,action='store_true',
                help="draw tag spacing")
ap.add_argument("-di", "--draw_id", required=False,action='store_true',
                help="draw tag id")
ap.add_argument("-dg", "--draw_grid", required=False,action='store_true',
                help="draw grid")


args = ap.parse_args()
draw_spacing = args.draw_spacing
draw_id = args.draw_id
draw_grid = args.draw_grid

tag_family = args.tag_family
tag_size = float(args.tag_size)
row = int(args.row)
col = int(args.col)
tag_spacing = float(args.tag_spacing)
output_path = args.output
svg_path = f"{output_path}.svg"
png_path = f"{output_path}.png"
vis_path = f"{output_path}_vis.png"
yaml_path = f"{output_path}.yaml"

folder=os.path.dirname(output_path)
if not os.path.exists(folder):
    os.makedirs(folder)
    
tag_generator = tag_generator_dict[tag_family]()

apriltag_board_width = col*tag_size+(col+1)*tag_spacing
apriltag_board_height = row*tag_size+(row+1)*tag_spacing
png_width = 1000
pixel_scale = png_width/apriltag_board_width


apriltag_board_svg = drawsvg.Drawing(
    apriltag_board_width, apriltag_board_height)
apriltag_board_svg.append(drawsvg.Rectangle(0, 0, apriltag_board_width,
                                            apriltag_board_height, fill='white'))
apriltag_board_svg.append(drawsvg.Text(f"tag family: {tag_family} row: {row} col: {col}",
                                       x=0.5*tag_spacing,
                                       y=0.5*tag_spacing,
                                       font_size=tag_spacing/5,
                                       fill='black',
                                       text_anchor='left',))

for y in range(row):
    for x in range(col):
        index = y*col+x
        print(f"tag id:{index}")
        tag_svg = tag_generator.get_svg(index, tag_size)
        if draw_id:
            tag_svg.append(drawsvg.Text(f"id: {index}",
                                        x=0.5*tag_size,
                                        y=tag_size+0.5*tag_spacing,
                                        font_size=tag_size/10,
                                        fill='black',
                                        text_anchor='middle',))

        apriltag_board_svg.append(drawsvg.Use(tag_svg,
                                              x*tag_size+(x+1)*tag_spacing,
                                              y*tag_size+(y+1)*tag_spacing,))

center_vis_group = drawsvg.Group(id="center_vis")
corner_vis_group = drawsvg.Group(id="corner_vis")
tag_size_2 = tag_size/2.0
corners = [
    [-tag_size_2, -tag_size_2],
    [tag_size_2, -tag_size_2],
    [tag_size_2, tag_size_2],
    [-tag_size_2, tag_size_2]
]
tag_dict = {}
tag_dict["tag_family"] = tag_family
tag_dict["tag_size"] = tag_size
tag_dict["row"] = row
tag_dict["col"] = col
tag_dict["tag_spacing"] = tag_spacing
tag_dict["tag_obj_points"] = {}
for y in range(row):
    for x in range(col):
        index = y*col+x

        center = [x*tag_size+(x+1)*tag_spacing+tag_size/2,
                  y*tag_size+(y+1)*tag_spacing+tag_size/2]
        corners_i = [[center[0]+c[0], center[1]+c[1], 0] for c in corners]
        center_vis_group.append(
            drawsvg.Circle(center[0], center[1], tag_size/10,
                           stroke="red", fill="none", stroke_width=tag_size/20)
        )
        data = {
            "center": center,
            "corners": corners_i
        }
        tag_dict["tag_obj_points"][index] = data

        for i in range(4):
            c = corners_i[i]
            corner_vis_group.append(
                drawsvg.Text(
                    f"{i}", x=c[0], y=c[1], font_size=tag_size/5, text_anchor="middle")
            )
            corner_vis_group.append(
                drawsvg.Circle(c[0], c[1], tag_size/5, stroke="green",
                               fill="none", stroke_width=tag_size/20)
            )


if draw_spacing:
    for y in range(row+1):
        for x in range(col+1):
            apriltag_board_svg.append(drawsvg.Rectangle(x*tag_size+x*tag_spacing,
                                                        y*tag_size+y*tag_spacing,
                                                        tag_spacing,
                                                        tag_spacing,
                                                        fill='black'))
if draw_grid:
    for y in range(row+1):
        apriltag_board_svg.append(drawsvg.Line(0,
                                               y*tag_size+(y+0.5)*tag_spacing,
                                               apriltag_board_width,
                                               y*tag_size+(y+0.5)*tag_spacing,
                                               stroke='black',
                                               stroke_width=tag_spacing/10))
    for x in range(col+1):
        apriltag_board_svg.append(drawsvg.Line(x*tag_size+(x+0.5)*tag_spacing, 0,
                                               x*tag_size+(x+0.5)*tag_spacing,
                                               apriltag_board_height,
                                               stroke='black',
                                               stroke_width=tag_spacing/10))

apriltag_board_svg.save_svg(svg_path)

apriltag_board_svg.set_pixel_scale(pixel_scale)
apriltag_board_svg.save_png(png_path)

apriltag_board_svg.append(center_vis_group)
apriltag_board_svg.append(corner_vis_group)
apriltag_board_svg.save_png(vis_path)

with open(yaml_path, "w") as f:
    yaml.dump(tag_dict, f)
