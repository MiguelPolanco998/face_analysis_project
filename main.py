import cv2
import mediapipe as mp
from utils.image_loader import cargar_overlay
from utils.analysis import analizar_rostro

# Cargar imagen
img = cargar_overlay()

# MediaPipe
detros = mp.solutions.face_detection
rostros = detros.FaceDetection(min_detection_confidence=0.8, model_selection=0)

# Cámara
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Cámara 1 no disponible, intentando cámara 0...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: No se puede abrir ninguna cámara")
        exit()

print("✓ Cámara iniciada correctamente")
print("Presiona ESC para salir")

frame_count = 0
process_every_n_frames = 15
last_analysis = {}

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: No se puede leer el frame")
        break

    frame_count += 1
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resrostros = rostros.process(rgb)

    if resrostros.detections:
        for rostro in resrostros.detections:
            al, an, _ = frame.shape
            box = rostro.location_data.relative_bounding_box
            xi, yi = int(box.xmin * an), int(box.ymin * al)
            xf, yf = xi + int(box.width * an), yi + int(box.height * al)

            cv2.rectangle(frame, (xi, yi), (xf, yf), (255, 255, 0), 2)

            if img is not None:
                ani, ali, _ = img.shape
                if frame.shape[0] > ani + 10 and frame.shape[1] > ali + 10:
                    frame[10:ani+10, 10:ali+10] = img

            if frame_count % process_every_n_frames == 0:
                face_region = frame[max(0, yi):min(al, yf), max(0, xi):min(an, xf)]
                if face_region.size > 0:
                    last_analysis = analizar_rostro(face_region)
                    if last_analysis:
                        print(f"Análisis: {last_analysis['genero']} de {last_analysis['edad']} años, {last_analysis['emocion']}, {last_analysis['raza']}")

            if last_analysis:
                y_offset = 30
                for i, key in enumerate(['genero', 'edad', 'emocion', 'raza']):
                    texto = f"{key.capitalize()}: {last_analysis.get(key, 'N/A')}"
                    cv2.putText(frame, texto, (10, y_offset + 30*i), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Frame: {frame_count}", (frame.shape[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.imshow("Detección Facial", frame)

    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break
    elif key == ord('r'):
        last_analysis = {}
        print("Análisis reseteado")

cap.release()
cv2.destroyAllWindows()
print("¡Aplicación cerrada correctamente!")
