import cv2
print(cv2.__version__)

# 1. Cria um objeto VideoCapture
# O parâmetro '0' (zero) indica a primeira webcam disponível no sistema.
# Se tiver mais de uma, pode tentar '1', '2', etc.
cap = cv2.VideoCapture(0)

# 2. Verifica se a câmera foi aberta com sucesso
if not cap.isOpened():
    print("Erro: Não foi possível abrir a câmera.")
    exit()

# 3. Loop infinito para ler frames contínuos
while True:
    # A função read() retorna duas coisas:
    # 'ret': um booleano (True se o frame foi lido com sucesso)
    # 'frame': o array NumPy que representa a imagem (o frame)
    ret, frame = cap.read()
    
    # Se a leitura falhar, saia do loop
    if not ret:
        print("Erro: Não foi possível receber o frame. Saindo...")
        break
    
    # 4. Exibe o frame na janela
    # O primeiro argumento é o nome da janela
    cv2.imshow('Webcam ao Vivo - Aperte Q para Sair', frame)
    
    # 5. Espera por uma tecla
    # cv2.waitKey(1) espera por 1 milissegundo, permitindo o streaming em tempo real.
    # A expressão '& 0xFF == ord('q')' verifica se a tecla apertada foi 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 6. Libera os recursos e fecha as janelas
# Essencial para que outros programas possam usar a câmera
cap.release()
cv2.destroyAllWindows()