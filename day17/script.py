import importlib as imp
import day17.adventure as day17

imp.reload(day17)

# clay_pos = day17.parse_line('x=509, y=13..20')

# ground = day17.Ground(range(0, 30), range(490, 510), clay_pos)


example = day17.from_file_data('day17/example.dat')

# ground = day17.from_file_data('day17/clay.dat')
