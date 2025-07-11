def traducir_emocion(emotion):
    emociones_map = {
        'angry': 'enojado/a',
        'disgust': 'disgustado/a', 
        'fear': 'miedoso/a',
        'happy': 'feliz',
        'sad': 'triste',
        'surprise': 'sorprendido/a',
        'neutral': 'neutral'
    }
    return emociones_map.get(emotion, emotion)

def traducir_raza(race):
    razas_map = {
        'asian': 'asiático/a',
        'indian': 'indio/a',
        'black': 'negro/a',
        'white': 'blanco/a',
        'middle eastern': 'oriente medio',
        'latino hispanic': 'latino/a'
    }
    return razas_map.get(race, race)
