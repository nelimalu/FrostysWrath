class WavePart:
    def __init__(self, snowman_level, amount, first_introduction, delay_between_spawn):
        self.snowman_level = snowman_level
        self.amount = amount
        self.first_introduction = first_introduction
        self.delay_between_spawn = delay_between_spawn


waves = [
    [WavePart(1, 10, 0, 0.5)],
    [WavePart(1, 20, 0, 0.1), WavePart(2, 5, 10, 10)]
]