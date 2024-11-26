import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Константы
G = 6.67430e-11  # гравитационная постоянная, м^3/(кг*с^2)
M = 5.972e24  # масса Земли, кг
R = 6371000  # радиус Земли, м
rho_0 = 1.225  # плотность воздуха на уровне моря, кг/м^3
T = 288.15  # температура, К
R_air = 287.05  # газовая постоянная для воздуха, Дж/(кг*К)
g0 = 9.81  # ускорение свободного падения на уровне моря, м/с^2

# Параметры ракеты
m0 = 300000  # начальная масса ракеты, кг
dm_dt = 500  # расход топлива, кг/с
F0 = 3.5e6  # тяга на старте, Н
F1 = 4.0e6  # тяга в вакууме, Н
Cf = 0.5  # коэффициент лобового сопротивления
S = 10  # площадь поперечного сечения ракеты, м^2
phi0 = 90  # начальный угол наклона, градусы
beta = -0.1  # изменение угла наклона, градусы/с
burn_time = m0 / dm_dt  # время работы двигателя, с

# Упрощенные уравнения движения
def simplified_equations_fixed(t, y):
    h, x, vy, vx, m, phi_deg = y  # высота, положение, вертикальная скорость, горизонтальная скорость, масса, угол
    phi = np.radians(phi_deg)  # угол в радианах

    # Текущая тяга
    if t <= burn_time:
        F_t = F0 + (F1 - F0) * (t / burn_time)
    else:
        F_t = 0  # после сгорания топлива тяга отсутствует

    # Масса уменьшается только во время работы двигателя
    dm_dt_actual = -dm_dt if t <= burn_time else 0

    # Сила тяжести
    g = G * M / (R + h)**2

    # Ограничение на высоту для избежания переполнения
    h = max(h, 0)

    # Плотность воздуха
    rho = rho_0 * np.exp(-M * g * h / (R_air * T)) if h < 1e5 else 0  # Плотность стремится к нулю на больших высотах

    # Скорость и сила сопротивления
    v = np.sqrt(vx**2 + vy**2)
    F_drag = Cf * S * rho * v**2 / 2 if v != 0 else 0
    F_drag_x = F_drag * (vx / v) if v != 0 else 0
    F_drag_y = F_drag * (vy / v) if v != 0 else 0

    # Проверка на нулевую массу
    if m <= 0:
        return [0, 0, 0, 0, 0, 0]  # Остановка всех изменений

    # Ускорения
    ay = (F_t * np.sin(phi) - m * g - F_drag_y) / m
    ax = (F_t * np.cos(phi) - F_drag_x) / m

    # Угловая скорость
    dphi_dt = beta

    return [vy, vx, ay, ax, dm_dt_actual, dphi_dt]

# Начальные условия
y0 = [0, 0, 0, 0, m0, phi0]  # [h, x, vy, vx, m, phi]

# Время моделирования
t_max = 600  # секунд
t_span = (0, t_max)
t_eval = np.linspace(0, t_max, 1000)

# Решение системы с исправлениями
sol_fixed = solve_ivp(simplified_equations_fixed, t_span, y0, t_eval=t_eval, method='RK45')

# Извлечение данных
h_fixed, x_fixed, vy_fixed, vx_fixed, m_fixed, phi_fixed = sol_fixed.y

# Построение графиков
plt.figure(figsize=(12, 8))

# Высота
plt.subplot(3, 1, 1)
plt.plot(sol_fixed.t, h_fixed / 1000, label="Высота")
plt.xlabel("Время, с")
plt.ylabel("Высота, км")
plt.grid()
plt.legend()

# Скорость
plt.subplot(3, 1, 2)
plt.plot(sol_fixed.t, np.sqrt(vx_fixed**2 + vy_fixed**2), label="Скорость")
plt.xlabel("Время, с")
plt.ylabel("Скорость, м/с")
plt.grid()
plt.legend()

# Угол наклона
plt.subplot(3, 1, 3)
plt.plot(sol_fixed.t, phi_fixed, label="Угол наклона")
plt.xlabel("Время, с")
plt.ylabel("Угол, градусы")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()
