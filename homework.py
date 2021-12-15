from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    INFORMATION: str = (
        "Тип тренировки: {}; "
        "Длительность: {:.3f} ч.; "
        "Дистанция: {:.3f} км; "
        "Ср. скорость: {:.3f} км/ч; "
        "Потрачено ккал: {:.3f}."
    )

    def get_message(self) -> str:
        return self.INFORMATION.format(
            self.training_type, self.duration,
            self.distance, self.speed, self.calories
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
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
        message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    CALORIE_COEFF_1 = 18
    CALORIE_COEFF_2 = 20

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        result: float = (
            (self.CALORIE_COEFF_1
                * self.get_mean_speed()
                - self.CALORIE_COEFF_2)
            * self.weight / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIE_COEFF_3 = 0.035
    CALORIE_COEFF_4 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        res: float = (
            (self.CALORIE_COEFF_3
                * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.CALORIE_COEFF_4 * self.weight)
            * (self.duration * self.MIN_IN_H)
        )
        return res


class Swimming(Training):
    """Тренировка: плавание. """
    LEN_STEP: float = 1.38
    CALORIE_COEFF_5: float = 1.1
    CALORIE_COEFF_6: float = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed()
                + self.CALORIE_COEFF_5)
            * self.CALORIE_COEFF_6
            * self.weight
        )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    read_training: dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    if workout_type in read_training.keys():
        return read_training[workout_type](*data)
    raise ValueError("Нет такой тренировки")


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
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
