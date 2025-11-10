import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import matplotlib.pyplot as plt

# 1. Configuração e Importação
print("Versão do TF:", tf.__version__)
print("Versão do TF Hub:", hub.__version__)

# --- PARÂMETROS GLOBAIS ---
# URL do modelo Feature Vector (MobileNet V2 pré-treinado em ImageNet)
# Este modelo extrai características, mas não tem a camada final de classificação.
MODEL_URL = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"

# A forma que o modelo pré-treinado espera para as imagens.
IMAGE_SHAPE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5 # Geralmente, poucas épocas são suficientes com Transfer Learning

# 2. Preparação do Dataset de Flores
# Baixa e organiza o conjunto de dados de 5 tipos de flores.
data_root = tf.keras.utils.get_file(
    'flower_photos',
    'https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
    untar=True
)

# Cria os conjuntos de treinamento e validação a partir do diretório.
# Este método é simples e prático, ele redimensiona e normaliza as imagens.
train_ds = tf.keras.utils.image_dataset_from_directory(
    str(data_root),
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMAGE_SHAPE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    str(data_root),
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMAGE_SHAPE,
    batch_size=BATCH_SIZE
)

# Obtém os nomes das classes (rosas, dentes-de-leão, etc.)
class_names = np.array(train_ds.class_names)
num_classes = len(class_names)
print(f"\nClasses encontradas: {num_classes} - {class_names}")

# O TF Hub espera entradas normalizadas entre [0, 1], o Keras Dataset
# gera dados entre [0, 255]. Adicionamos uma camada de Rescaling.
normalization_layer = tf.keras.layers.Rescaling(1./255)
train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y))

# Otimiza o pipeline de dados para melhor performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


# 3. Construção do Modelo com hub.KerasLayer (Transferência de Aprendizado)

# A camada principal: carrega o MobileNet V2
feature_extractor_layer = hub.KerasLayer(
    MODEL_URL,
    input_shape=IMAGE_SHAPE + (3,), # Entrada (224, 224, 3)
    trainable=False # ESSENCIAL: Congela os pesos do modelo pré-treinado
)

# Cria o modelo sequencial
model = tf.keras.Sequential([
    # Camada 1: O Extrator de Características Congelado (TF Hub)
    feature_extractor_layer, 
    
    # Camada 2: Sua nova Camada de Classificação (Keras Dense)
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.summary()


# 4. Compilação e Treinamento do Modelo (TensorFlow/Keras)

# Compilação
model.compile(
    optimizer='adam',
    # Usamos SparseCategoricalCrossentropy porque os labels são inteiros (0, 1, 2, ...)
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy']
)

# Treinamento
print("\nIniciando o Treinamento...")
history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS
)

# 5. Avaliação
print(f"\nAvaliação final após {EPOCHS} épocas:")
loss, accuracy = model.evaluate(val_ds)
print(f"Perda (Loss): {loss:.4f}")
print(f"Acurácia (Accuracy): {accuracy:.4f}")


# 6. Exemplo de Predição (Inferência)

# Pega um lote de imagens de validação para teste
for images, labels in val_ds.take(1):
    break
    
# Faz a predição no lote (retorna probabilidades)
predictions = model.predict(images)

# Converte as probabilidades para o índice da classe prevista
predicted_classes = np.argmax(predictions, axis=1)

print("\nExemplo de Predição no primeiro lote:")
print(f"Rótulos Reais (Índices): {labels.numpy()[:5]}")
print(f"Classes Previstas (Índices): {predicted_classes[:5]}")
print(f"Nomes Previstos: {class_names[predicted_classes[:5]]}")