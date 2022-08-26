# -*- coding: utf-8 -*-
# @Time    : 8/22/22 7:42 PM
# @FileName: ScienceCaptcha.py
# @Software: PyCharm
# @Github    ：sudoskys
import math
import random
import time


class Importer(object):
    def __init__(self, s=time.time()):
        self.samples = s
        import time
        # self.items = [{"diff": parabola_2(s).difficulty, "obj": parabola_2(s)},
        #               {"diff": radius(s).difficulty, "obj": parabola(s)},
        #               {"diff": find_volume_cone(s).difficulty, "obj": find_volume_cone(s)},
        #               {"diff": find_ball_cone(s).difficulty, "obj": find_ball_cone(s)},
        #               {"diff": gravity_work(s).difficulty, "obj": gravity_work(s)},
        #               {"diff": binary_first_equation(s).difficulty, "obj": binary_first_equation(s)},
        #               {"diff": biological_gene(s).difficulty, "obj": biological_gene(s)},
        #               ]

    def pull(self, difficulty_min=1, difficulty_limit=5):
        from random import choice
        if difficulty_limit < 1 or difficulty_limit < difficulty_min:
            if difficulty_limit < 0:
                difficulty_limit = 9
            if difficulty_min >= 9:
                difficulty_min = 1
        verify_papaer = [i for i in self.items if difficulty_min <= i.get("diff") <= difficulty_limit]
        verify = (choice(verify_papaer))
        return verify.get("obj")
