# a simple tool to generate apriltag gird

This tool can generate png and svg with a detailed config file

## example pattern

usage

```shell
usage: apriltag_generate.py [-h] -f TAG_FAMILY -s TAG_SIZE -r ROW -c COL -t TAG_SPACING [-o OUTPUT] [-ds] [-di] [-dg]

options:
  -h, --help            show this help message and exit
  -f TAG_FAMILY, --tag_family TAG_FAMILY
  -s TAG_SIZE, --tag_size TAG_SIZE
  -r ROW, --row ROW
  -c COL, --col COL
  -t TAG_SPACING, --tag_spacing TAG_SPACING
  -o OUTPUT, --output OUTPUT
  -ds, --draw_spacing   draw tag spacing
  -di, --draw_id        draw tag id
  -dg, --draw_grid      draw grid
```

parameter TAG_SIZE and TAG_SPACING unit is m.

example

```shell
apriltag_generate.py -f tag36h11 -s 0.0164 -r 6 -c 8 -t 0.0082 -o output/update_test  -di
```

which means generate an 6x8 tag36h11 gird with 0.0164m tagwidth and 0.0082m spacing and draw tag id.

![alt text](./.assert/update_test.png)

## config

```yaml
col: 8
row: 6
tag_family: tag36h11
tag_size: 2.0 # tag size in m
tag_spacing: 1.0 # tag spacing in m
tag_obj_points: # tag corner point in world
  0:# tagid
    center:
    - 2.0
    - 2.0
    corners:
    - - 1.0
      - 1.0
      - 0
    - - 3.0
      - 1.0
      - 0
    - - 3.0
      - 3.0
      - 0
    - - 1.0
      - 3.0
      - 0
      
```
