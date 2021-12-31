import time
import Snowman


class WavePart:
    def __init__(self, snowman_level, amount, first_introduction, delay_between_spawn):
        self.snowman_level = snowman_level
        self.amount = amount
        self.first_introduction = first_introduction
        self.delay_between_spawn = delay_between_spawn
        self.last_spawn = time.time()
        self.spawned = 0
        self.started = False


class Wave:
    def __init__(self, *args):
        self.waveparts = args
        self.time_started = time.time()
        self.alive = 0

    def update(self, width, height, campfire):
        new_snowmen_1 = []
        new_snowmen_2 = []
        new_snowmen_3 = []
        for part in self.waveparts:
            if not part.started and part.last_spawn >= part.first_introduction:
                part.started = True

            if time.time() - part.last_spawn >= part.delay_between_spawn:
                part.last_spawn = time.time()
                part.spawned += 1

                if part.spawned <= part.amount:
                    if part.snowman_level == 1:
                        new_snowmen_1.append(Snowman.spawn_firstsnowman(width, height, campfire))
                    if part.snowman_level == 2:
                        new_snowmen_2.append(Snowman.spawn_secondsnowman(width, height, campfire))
                    if part.snowman_level == 3:
                        new_snowmen_3.append(Snowman.spawn_thirdsnowman(width, height, campfire))

        self.alive += len(new_snowmen_1) + len(new_snowmen_2) + len(new_snowmen_3)
        return new_snowmen_1, new_snowmen_2, new_snowmen_3


# todo add a way to specify music for a wave

# Wave -> level, amount, first introduction, time_between_spawn
waves = [
    # Wave(WavePart(1, 10, 0, 0.5)),
    # Wave(WavePart(1, 15, 10, 0.3), WavePart(2, 5, 20, 10)),
    Wave(WavePart(1, 12, 10, 0.3), WavePart(2, 5, 20, 10), WavePart(3, 2, 10, 10)),
    Wave(WavePart(1, 40, 10, 0.5)),
    Wave(WavePart(1, 15, 10, 0.3), WavePart(2, 5, 20, 10), WavePart(3, 2, 10, 10))
]
