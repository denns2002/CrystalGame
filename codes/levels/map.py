t = 'green_tree'
_ = ""
g = 'green_grass_with_tales'
p = 'player'
w = 'wall'
MAP = [
    [
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
        [g,g,g,g,g,g,g,g,g,g,g,g,],
    ],
    [
        [_,t,_,_,_,t,_,_,_,t,],
        [t,_,_,_,t,_,_,t,_,t,],
        [_,_,p,_,_,t,_,_,_,_,],
        [_,t,_,_,t,_,_,t,_,t,],
        [_,_,t,_,t,t,_,_,_,t,],
        [_,t,_,_,t,_,_,t,_,t,],
        [t,_,_,_,t,_,_,t,_,t,],
    ],
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