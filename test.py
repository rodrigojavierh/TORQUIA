import threading
import time

# Función 1: Primer bucle while
def task1():
    while True:
        print("Task 1 is running")
        time.sleep(1)  # Simula una tarea con espera

# Función 2: Segundo bucle while
def task2():
    while True:
        print("Task 2 is running")
        time.sleep(2)  # Simula una tarea con espera diferente

# Crear y ejecutar los hilos
thread1 = threading.Thread(target=task1)
thread2 = threading.Thread(target=task2)

# Iniciar los hilos
thread1.start()
thread2.start()

# Esperar a que los hilos terminen (opcional, no necesario si el programa es infinito)
thread1.join()
thread2.join()
