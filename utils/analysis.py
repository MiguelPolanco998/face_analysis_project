import cv2
from deepface import DeepFace
from .translations import traducir_emocion, traducir_raza

def analizar_rostro(face_region):
    try:
        face_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)
        info = DeepFace.analyze(face_rgb, actions=['age', 'gender', 'race', 'emotion'], enforce_detection=False)
        
        if isinstance(info, list) and len(info) > 0:
            info = info[0]
        
        edad = info.get('age', 'N/A')
        emocion = info.get('dominant_emotion', 'N/A')
        raza = info.get('dominant_race', 'N/A')

        gender_info = info.get('gender', {})
        if isinstance(gender_info, dict):
            gen = max(gender_info, key=gender_info.get)
        else:
            gen = str(gender_info)

        return {
            'edad': edad,
            'genero': 'Hombre' if gen.lower() in ['man', 'male'] else 'Mujer',
            'emocion': traducir_emocion(emocion),
            'raza': traducir_raza(raza)
        }

    except Exception as e:
        print(f"Error en análisis DeepFace: {e}")
        return {}
