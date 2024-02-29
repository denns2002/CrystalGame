t = 'green_tree'
_ = ""
g = 'green_grass_with_tales'
p = 'player'
w = 'wall'
MAP = [
    [
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*20,
    ]*20,
    [
        [_,t,_,_,_,t,_,_,_,t,]*20,
        [t,_,_,_,t,_,_,t,_,t,]*20,
        [_,_,p,_,_,t,_,_,_,_,],
        [_,t,_,_,t,_,_,t,_,t,]*20,
        [_,_,t,_,t,t,_,_,_,t,]*20,
        [_,t,_,_,t,_,_,t,_,t,]*20,
        [t,_,_,_,t,_,_,t,_,t,]*20,
    ]*20,
    [[],[],[_,_,_,_,_,_,g]]
]
FIRST_FLOOR = [
    [_,_,_,_,_,],
    [_,_,_,_,_,],
    [_,_,p,_,_,],
    [_,_,_,_,_,],
    [_,_,_,_,_,],
]

# MAP = [
#     [],
# ]