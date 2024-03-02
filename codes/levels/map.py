t = 'green_tree'
_ = ""
g = 'green_grass_with_tales'
p = 'player'
w = 'wall'
MAP = [
    [
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
        [g,g,g,g,g,g,g,g,g,g,g,g,]*5,
    ]*5,
    [
        [_,t,_,_,_,t,_,_,_,t,]*5,
        [t,_,_,_,t,_,_,t,_,t,]*5,
        [_,_,p,_,_,t,_,_,_,_,],
        [_,t,_,_,t,_,_,t,_,t,]*5,
        [_,_,t,_,t,t,_,_,_,t,]*5,
        [_,t,_,_,t,_,_,t,_,t,]*5,
        [t,_,_,_,t,_,_,t,_,t,]*5,
    ]*5,
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