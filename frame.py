import cv2
import os

def capture_frames(video_path, output_dir, frame_interval=10):
    """
    Captura frames de un video y los guarda como imágenes.
    
    Parámetros:
    - video_path: Ruta del archivo de video.
    - output_dir: Carpeta donde se guardarán las imágenes capturadas.
    - frame_interval: Intervalo de frames para capturar imágenes (por defecto, cada 30 frames).
    """
    # Verifica si la carpeta de salida existe, si no, la crea
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Cargar el video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"No se puede abrir el video: {video_path}")
        return

    frame_count = 0
    saved_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Fin del video

        # Guardar el frame si cumple con el intervalo
        if frame_count % frame_interval == 0:
            filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
            cv2.imwrite(filename, frame)
            saved_count += 1
            print(f"Guardado: {filename}")

        frame_count += 1

    # Liberar el video
    cap.release()
    print(f"Capturas completadas. Se guardaron {saved_count} imágenes en '{output_dir}'.")

# Ejemplo de uso
video_path = "C:/Users/rodri/OneDrive/Escritorio/PDM/DOCKER/20241119_210533.mp4"  # Cambia esto a la ruta de tu video
output_dir = "capturas"           # Carpeta donde se guardarán las imágenes
frame_interval = 10           # Capturar cada 30 frames (ajusta según lo necesites)

capture_frames(video_path, output_dir, frame_interval)
