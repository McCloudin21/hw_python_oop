from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: tuple
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {"%.3f" % (self.duration)} ч.; '
                f'Дистанция: {"%.3f" % (self.distance)} км; '
                f'Ср. скорость: {"%.3f" % (self.speed)} км/ч; '
                f'Потрачено ккал: {"%.3f" % (self.calories)}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000  # Meters per kilometer
    LEN_STEP: float = 0.65  # Step Length
    M_IN_HR: int = 60  # Minutes per hour

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
        raise NotImplementedError(f'{self.get_spent_calories.__name__}'
                                  f'должен быть определен у '
                                  f'{self.__class__.__name__}!')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.get_trainig_type(),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())

    def get_trainig_type(self):
        return type(self).__name__


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * (self.duration * self.M_IN_HR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    SEC_IN_MIN: float = 0.278  # Seconds per minute
    HEIGHT_IN_METERS: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.SEC_IN_MIN)**2
                 / (self.height / self.HEIGHT_IN_METERS))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * (self.duration * self.M_IN_HR))


class Swimming(Training):
    """Тренировка: плавание."""
    SWM_SPEED_MULTIPLIER: float = 1.1
    SWM_SPEED_SHIFT: int = 2
    LEN_STEP: float = 1.38  # Step Length

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

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWM_SPEED_MULTIPLIER)
                * self.SWM_SPEED_SHIFT * self.weight * self.duration)


def read_package(workout_type: str, data: list[float]) -> type[Training]:
    """Прочитать данные полученные от датчиков."""
    classes: dict[str, object] = {'RUN': Running,
                                  'WLK': SportsWalking,
                                  'SWM': Swimming}

    class_type = None
    for class_type in classes:
        if workout_type == class_type:
            return classes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
