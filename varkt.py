import numpy as np
import matplotlib.pyplot as plt

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

def simulate_trajectory(stages, dt=0.1, t_max=60):
    """Моделирование полета ракеты."""
    # Временные параметры
    time = np.arange(0, t_max, dt)

    # Инициализация массивов
    h = np.zeros_like(time)  # высота
    v = np.zeros_like(time)  # скорость
    m = np.zeros_like(time)  # масса

    # Начальные условия
    h[0] = 0
    v[0] = 0
    m[0] = sum(stage["fuel_mass"] + stage["dry_mass"] for stage in stages)

    current_stage = 0
    fuel_remaining = stages[current_stage]["fuel_mass"]

    for i in range(1, len(time)):
        if current_stage < len(stages):
            stage = stages[current_stage]

            if fuel_remaining > 0:
                F_thrust = stage["thrust"]
                mdot = F_thrust / (stage["isp"] * 9.81)  # Расход топлива, кг/с
                fuel_consumed = mdot * dt
                fuel_remaining -= fuel_consumed

                if fuel_remaining < 0:
                    fuel_consumed += fuel_remaining  # Уточнение на последнем шаге
                    fuel_remaining = 0

                m[i] = m[i-1] - fuel_consumed
            else:
                current_stage += 1
                if current_stage < len(stages):
                    fuel_remaining = stages[current_stage]["fuel_mass"]
                F_thrust = 0
                m[i] = m[i-1]
        else:
            F_thrust = 0
            m[i] = m[i-1]

        F_gravity = gravitational_force(m[i-1], h[i-1])
        F_drag = 0.5 * air_density(h[i-1]) * v[i-1]**2 * 0.3 * 10

        a = (F_thrust - F_gravity - F_drag) / m[i-1]
        v[i] = v[i-1] + a * dt
        h[i] = h[i-1] + v[i-1] * dt

    return time, h, v, m

# Моделирование
dt = 0.1
simulation_time = 60  # секунд
time, height, velocity, mass = simulate_trajectory(stages, dt, simulation_time)

# Построение графиков
plt.figure(figsize=(15, 10))

# График скорости от времени
plt.subplot(3, 1, 1)
plt.plot(time, velocity, label="Скорость", color="blue")
plt.title("Зависимость скорости от времени")
plt.xlabel("Время (с)")
plt.ylabel("Скорость (м/с)")
plt.grid(True)
plt.legend()

# График массы от времени
plt.subplot(3, 1, 2)
plt.plot(time, mass, label="Масса", color="green")
plt.title("Зависимость массы от времени")
plt.xlabel("Время (с)")
plt.ylabel("Масса (кг)")
plt.grid(True)
plt.legend()

# График высоты от времени
plt.subplot(3, 1, 3)
plt.plot(time, height, label="Высота", color="red")
plt.title("Зависимость высоты от времени")
plt.xlabel("Время (с)")
plt.ylabel("Высота (м)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
