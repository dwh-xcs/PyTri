import cv2
import tensorflow as tf
import tensorflow_hub as hub
import pyttsx3
import time

# Dicionário de tradução das classes (nomes de objetos)
CLASSES = {
    1: 'Pessoa', 2: 'Bicicleta', 3: 'Carro', 4: 'Motocicleta', 5: 'Avião',
    6: 'Ônibus', 7: 'Trem', 8: 'Caminhão', 9: 'Barco', 10: 'Semáforo',
    11: 'Hidrante', 13: 'Placa de Pare', 14: 'Parquímetro', 15: 'Banco',
    16: 'Pássaro', 17: 'Gato', 18: 'Cachorro', 19: 'Cavalo', 20: 'Ovelha',
    21: 'Vaca', 22: 'Elefante', 23: 'Urso', 24: 'Zebra', 25: 'Girafa',
    27: 'Mochila', 28: 'Guarda-chuva', 31: 'Bolsa', 32: 'Gravata', 33: 'Mala',
    34: 'Frisbee', 35: 'Esqui', 36: 'Snowboard', 37: 'Bola esportiva',
    38: 'Pipa', 39: 'Taco de beisebol', 40: 'Luva de beisebol', 41: 'Skate',
    42: 'Prancha de surfe', 43: 'Raquete de tênis', 44: 'Garrafa',
    46: 'Cálice de vinho', 47: 'Xícara', 48: 'Garfo', 49: 'Faca', 50: 'Colher',
    51: 'Tigela', 52: 'Banana', 53: 'Maçã', 54: 'Sanduíche', 55: 'Laranja',
    56: 'Brócolis', 57: 'Cenoura', 58: 'Cachorro-quente', 59: 'Pizza',
    60: 'Donut', 61: 'Bolo', 62: 'Cadeira', 63: 'Sofá', 64: 'Vaso de planta',
    65: 'Cama', 66: 'Mesa de jantar', 67: 'Vaso sanitário', 69: 'TV',
    70: 'Laptop', 71: 'Mouse', 72: 'Controle remoto', 73: 'Teclado',
    74: 'Celular', 75: 'Micro-ondas', 76: 'Forno', 77: 'Torradeira',
    78: 'Pia', 79: 'Geladeira', 81: 'Relógio', 82: 'Vaso', 84: 'Tesoura',
    85: 'Ursinho de pelúcia', 86: 'Secador de cabelo', 87: 'Escova de dentes'
}

# Carregar o modelo de detecção de objetos do TensorFlow Hub
model = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")

# Inicializar o motor de fala
try:
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
except Exception as e:
    print(f"Erro ao inicializar o motor de voz: {e}. A funcionalidade de voz será desativada.")
    engine = None

last_spoken_sentence = ""
last_spoken_time = 0
cooldown_period = 1

# Abrir a câmera
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

# frame_count = 0
# memory_clear_interval = 100

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # Otimização: Limpar a memória periodicamente
#     if frame_count % memory_clear_interval == 0:
#         tf.keras.backend.clear_session()
#         print("Memória do TensorFlow liberada.")
    
#     # Otimização: Redimensionar o frame para o tamanho de entrada do modelo
#     h_original, w_original, _ = frame.shape
#     frame_resized = cv2.resize(frame, (320, 320))
    
#     input_tensor = tf.convert_to_tensor(frame_resized)
#     input_tensor = tf.image.convert_image_dtype(input_tensor, tf.uint8)
#     input_tensor = input_tensor[tf.newaxis, ...]
    
#     detections = model(input_tensor)

#     num_detections = int(detections.pop('num_detections'))
#     detections = {key: value[0, :num_detections].numpy()
#                   for key, value in detections.items()}
#     detections['num_detections'] = num_detections

#     detection_classes = detections['detection_classes'].astype(int)
#     detection_scores = detections['detection_scores']
#     detection_boxes = detections['detection_boxes']
    
#     detected_objects = []

#     # Percorrer todas as detecções e coletar os nomes
#     for i in range(len(detection_classes)):
#         score = detection_scores[i]
#         class_id = detection_classes[i]
        
#         # Otimização: Aumentar o limiar de confiança para 0.7
#         if score > 0.7 and class_id in CLASSES:
#             object_name = CLASSES[class_id]
#             detected_objects.append(object_name)

#             # Desenhar na imagem original
#             ymin, xmin, ymax, xmax = detection_boxes[i]
            
#             # Ajustar as coordenadas para o tamanho do frame original
#             (left, right, top, bottom) = (int(xmin * w_original), int(xmax * w_original),
#                                           int(ymin * h_original), int(ymax * h_original))

#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#             cv2.putText(frame, f'{object_name}: {score:.2f}', (left, top - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#     # Lógica de fala
#     detected_objects_unique = list(set(detected_objects))
#     if detected_objects_unique and engine:
#         current_sentence = "Eu vejo " + ", ".join(detected_objects_unique) + "."
        
#     #     current_time = time.time()
#     #     if current_sentence != last_spoken_sentence or (current_time - last_spoken_time) > cooldown_period:
#     #         engine.say(current_sentence)
#     #         engine.runAndWait()
#     #         last_spoken_sentence = current_sentence
#     #         last_spoken_time = current_time

#         # Mude a lógica de fala para algo assim:
#         if current_sentence != last_spoken_sentence:
#             engine.say(current_sentence)
#             engine.runAndWait()
#             last_spoken_sentence = current_sentence

#     cv2.imshow('Detector de Objetos', frame)
    
#     frame_count += 1
    
    # Correção para o erro de saída
    key = cv2.waitKey(1)
    if key != -1:
        if chr(key & 0xFF) == 'q':
            break

cap.release()
cv2.destroyAllWindows()