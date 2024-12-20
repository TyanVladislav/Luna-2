import krpc
import time
import json

# Подключаемся к серверу kRPC
conn = krpc.connect(name='Rocket Altitude Logger')
vessel = conn.space_center.active_vessel

# Функция для записи данных в JSON-файл
def write_to_json(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

# Инициализируем список для хранения данных высоты
altitude_data_log = []

# Имя выходного файла для высоты
altitude_output_file = 'rocket_altitude_data.json'

print("Сбор данных о высоте начался. Нажмите Ctrl+C для завершения.")

try:
    while True:
        # Получаем текущую высоту ракеты над уровнем моря
        altitude = vessel.flight().mean_altitude

        # Получаем текущее время миссии
        mission_time = vessel.met

        # Добавляем данные в список
        altitude_data_log.append({
            'time': mission_time,
            'altitude': altitude
        })

        # Печатаем данные в консоль (опционально)
        print(f"Time: {mission_time:.2f} s, Altitude: {altitude:.2f} m")

        # Ждём 1 секунду перед следующей записью
        time.sleep(1)

except KeyboardInterrupt:
    # При завершении записи сохраняем данные в файл
    print("\nСохранение данных в файл...")
    write_to_json(altitude_output_file, altitude_data_log)
    print(f"Данные сохранены в {altitude_output_file}")
