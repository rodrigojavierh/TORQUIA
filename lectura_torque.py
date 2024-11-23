import serial
import csv
import time
from datetime import datetime

# Configuración del puerto serial
port = 'COM4'  # Reemplaza con el puerto adecuado (e.g., COM3 en Windows o /dev/ttyUSB0 en Linux)
baudrate = 115200  # Debe coincidir con el baudrate usado en la ESP32

# Crear conexión serial
try:
    ser = serial.Serial(port, baudrate, timeout=1)
except serial.SerialException:
    print(f"Error: No se puede abrir el puerto {port}. Asegúrate de que el puerto esté disponible.")
    exit()

# Archivo CSV donde se guardarán los datos
csv_filename = 'lecturas_adc.csv'

# Crear el archivo CSV y escribir el encabezado
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Milliseconds', 'ADC Reading'])

print(f"Leyendo datos desde el puerto serial {port} y guardando en {csv_filename}...")

# Tiempo inicial para calcular milisegundos
start_time = time.time() * 1000  # Tiempo inicial en milisegundos

try:
    while True:
        # Leer línea desde el puerto serial
        line = ser.readline().decode('utf-8').strip()
        
        # Verificar si la línea contiene la lectura del ADC
        if "Lectura Bruta del ADC:" in line:
            adc_reading = line.split(':')[-1].strip()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            elapsed_time_ms = int(time.time() * 1000 - start_time)  # Tiempo transcurrido en milisegundos
            
            # Guardar los datos en el archivo CSV
            with open(csv_filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, elapsed_time_ms, adc_reading])
            
            # Imprimir la lectura y el timestamp
            print(f"{timestamp} - {elapsed_time_ms} ms - ADC Reading: {adc_reading}")
        
        # Esperar un poco antes de leer la siguiente línea
        time.sleep(0.1)

except KeyboardInterrupt:
    # Finalizar la lectura al presionar Ctrl+C
    print("\nLectura finalizada.")
    ser.close()
except Exception as e:
    print(f"Error: {e}")
    ser.close()