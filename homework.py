class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type,
                 duration,
                 distance,
                 speed,
                 calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {Training.__name__}; '
                f'Длительность: {"%.3f" % (self.duration)} ч.; '
                f'Дистанция: {"%.3f" % (self.distance)} км; '
                f'Ср. скорость: {"%.3f" % (self.speed)} км/ч; '
                f'Потрачено ккал: {"%.3f" % (self.calories)}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    M_IN_HR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage.get_message(self)


class Running(Training):
    """Тренировка: бег."""
    RUN_1_KONST = 18
    RUN_2_KONST = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        return super().get_distance()

    def get_spent_calories(self
                           ):

        return ((self.RUN_1_KONST * self.get_mean_speed()
                + self.RUN_2_KONST) * self.weight / self.M_IN_KM
                * (self.duration * self.M_IN_HR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WLK_1_KONST = 0.035
    WLK_2_KONST = 0.029
    WLK_3_KONST = 0.278
    WLK_4_KONST = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self
                           ):

        return ((self.WLK_1_KONST * self.weight
                + ((self.get_mean_speed() * self.WLK_3_KONST)**2
                 / (self.height / self.WLK_4_KONST))
                * self.WLK_2_KONST * self.weight)
                * (self.duration * self.M_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""
    SWM_1_KONST = 1.1
    SWM_2_KONST = 2
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self,
                     ):
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self
                       ):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self
                           ):
        return ((self.get_mean_speed() + self.SWM_1_KONST)
                * self.SWM_2_KONST * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    classes = {'RUN': Running,
               'WLK': SportsWalking,
               'SWM': Swimming}

    if workout_type in classes:
        training_class: Training = classes[workout_type](*data)
        return training_class


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())
