import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы
G = 6.67430e-11  # гравитационная постоянная, м^3/(кг*с^2)
M_Earth = 5.972e24  # масса Земли, кг
R_Earth = 6371e3  # радиус Земли, м
rho0 = 1.225  # плотность воздуха на уровне моря, кг/м^3
H = 8500  # масштаб высоты атмосферы, м

# Параметры ракеты Луна-2
stages = [
    {  # Первая ступень
        "engines": 4,
        "thrust": 4 * 994e3,  # тяга в вакууме, Н
        "fuel_mass": 4 * 43400,  # масса топлива, кг
        "dry_mass": 4 * 3750,  # сухая масса, кг
        "burn_time": 118,  # время работы, с
        "isp": 315  # удельный импульс, с
    },
    {  # Вторая ступень
        "engines": 1,
        "thrust": 990e3,  # тяга в вакууме, Н
        "fuel_mass": 86200,  # масса топлива, кг
        "dry_mass": 7150,  # сухая масса, кг
        "burn_time": 310,  # время работы, с
        "isp": 315  # удельный импульс, с
    },
    {  # Третья ступень
        "engines": 1,
        "thrust": 54e3,  # тяга в вакууме, Н
        "fuel_mass": 5000,  # масса топлива, кг
        "dry_mass": 355,  # сухая масса, кг
        "burn_time": 240,  # время работы, с
        "isp": 326  # удельный импульс, с
    }
]

def air_density(h):
    """Расчет плотности воздуха."""
    return rho0 * np.exp(-h / H)

def gravitational_force(m, h):
    """Гравитационная сила."""
    return G * M_Earth * m / (R_Earth + h) ** 2

def dynamics(t, y, stages):
    """Функция для solve_ivp, описывающая динамику системы."""
    h, v, m = y  # Высота, скорость, масса

    if m <= sum(stage['dry_mass'] for stage in stages):
        thrust = 0  # Если топливо закончилось, тяги нет
        dm_dt = 0
    else:
        for stage in stages:
            stage_fuel_mass = stage['fuel_mass']
            stage_dry_mass = stage['dry_mass']

            if m > stage_dry_mass:
                thrust = stage['thrust']
                isp = stage['isp']
                mdot = thrust / (isp * 9.81)
                dm_dt = -mdot
                break

    F_gravity = gravitational_force(m, h)
    F_drag = 0.5 * air_density(h) * v**2 * 0.3 * 10
    a = (thrust - F_gravity - F_drag) / m

    return [v, a, dm_dt]

# Начальные условия
h0 = 0  # Начальная высота, м
v0 = 0  # Начальная скорость, м/с
m0 = sum(stage["fuel_mass"] + stage["dry_mass"] for stage in stages)  # Общая начальная масса, кг

# Время моделирования
dt = 0.1  # Шаг времени
simulation_time = 60  # секунд

t_span = (0, simulation_time)  # Временной интервал, сек
t_eval = np.arange(0, simulation_time, dt)  # Точки времени для вывода результата

y0 = [h0, v0, m0]

# Численное решение
solution = solve_ivp(dynamics, t_span, y0, t_eval=t_eval, args=(stages,))

# Извлечение решения
height = solution.y[0]
velocity = solution.y[1]
mass = solution.y[2]

# Построение графиков
plt.figure(figsize=(15, 10))

# График скорости от времени
plt.subplot(3, 1, 1)
plt.plot(solution.t, velocity, label="Скорость", color="blue")
plt.title("Зависимость скорости от времени")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.grid(True)
plt.legend()

# График массы от времени
plt.subplot(3, 1, 2)
plt.plot(solution.t, mass, label="Масса", color="green")
plt.title("Зависимость массы от времени")
plt.xlabel("Время (с)")
plt.ylabel("Масса (кг)")
plt.grid(True)
plt.legend()

# График высоты от времени
plt.subplot(3, 1, 3)
plt.plot(solution.t, height, label="Высота", color="red")
plt.title("Зависимость высоты от времени")
plt.xlabel("Время (с)")
plt.ylabel("Высота (м)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
