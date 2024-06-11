# LIBRAS ARCADE

LIBRAS ARCADE é um aplicativo de jogo educativo desenvolvido em Python e Arduino que tem como foco a Língua Brasileira de Sinais (LIBRAS). O objetivo do jogo é ajudar os usuários a aprender e praticar LIBRAS de forma interativa e divertida. O jogo utiliza vídeos e perguntas de múltipla escolha para ensinar frases e sinais em LIBRAS.

## Requisitos

### Software

- Python 3.x
- Bibliotecas Python:
- tkinter
- Pillow
- moviepy
- threading
- random
- time
- serial

### Hardware

- Placa Arduino
- Display LCD I2C (20x4)
- Botões de navegação e confirmação
- LEDs para indicar vidas e resultados
- Cabos e conexões adequadas

## Instalação

### Software

1. Clone o repositório ou faça o download dos arquivos do projeto.

2. Certifique-se de ter o Python 3.x instalado em seu sistema.

3. Instale as bibliotecas necessárias utilizando pip:

  pip install pillow moviepy pyserial

### Hardware

1. Conecte os componentes conforme o esquema de pinos descrito no código do Arduino.

2. Faça o upload do código para o Arduino.

## Estrutura do Projeto

- libras_arcade.py: Código principal do jogo em Python.
- arduino_code.ino: Código para ser carregado no Arduino.
- videos/: Pasta contendo os vídeos utilizados nas perguntas.
- libras-arcade.png: Imagem usada na tela inicial e na tela de agradecimento.

## Estrutura do Código

### Código Python (libras_arcade.py)

- __init__(self, root): Inicializa a interface gráfica, configura o Arduino e define as perguntas do jogo.
- start_serial_thread(self): Inicia a thread de leitura da porta serial.
- show_start_screen(self): Exibe a tela inicial do jogo.
- read_from_serial(self): Lê os comandos enviados pelo Arduino.
- show_options(self): Exibe as opções de categoria.
- handle_option(self, option): Lida com a seleção de categoria ou a opção de parar o jogo.
- show_question(self): Exibe a pergunta atual e suas opções.
- play_video(self, video_path): Reproduz o vídeo associado à pergunta.
- stop_video(self): Para a reprodução do vídeo.
- check_answer(self, selected_index, correct_index): Verifica se a resposta selecionada está correta e atualiza o jogo.
- next_question_with_delay(self): Avança para a próxima pergunta após um pequeno atraso.
- show_thank_you_screen(self): Exibe a tela de agradecimento ao final do jogo.

### Código Arduino (arduino_code.ino)

- setup(): Configura os pinos, inicializa o LCD e a comunicação serial, e exibe a tela inicial.
- loop(): Lida com a lógica do jogo, incluindo leitura de botões e atualização de estado.
- displayLives(): Atualiza a exibição das vidas restantes usando LEDs.
- displayMenu(): Exibe o menu de seleção de categorias.
- displayQuestion(): Exibe a pergunta atual e suas opções no LCD.
- displayAnswer(bool correct): Exibe se a resposta está correta ou incorreta usando LEDs.
- handleButtonPress(int buttonPin): Lida com a lógica de pressionamento de botões.
- startGame(): Inicia o jogo e envia o comando de início via serial.
- resetGame(): Reseta o jogo ao estado inicial.
- showThankYouScreen(): Exibe a tela de agradecimento ao final do jogo.
- nextQuestion(): Avança para a próxima pergunta.
- turnOffResultLeds(): Desliga os LEDs de resultado.

## Como Jogar

### Software

- Execute o arquivo libras_arcade.py:

 `python libras_arcade.py`

- A tela inicial será exibida com um botão "Começar". Clique nele para iniciar o jogo.
- Escolha uma das categorias: "Viagem", "Escola" ou "Cotidiano".
- Um vídeo será exibido com uma frase em LIBRAS. Após o vídeo, opções de resposta serão apresentadas. Selecione a resposta correta.
- Se a resposta estiver correta, a próxima pergunta será exibida. Caso contrário, você perderá uma vida.
- O jogo termina quando todas as perguntas são respondidas ou quando você perde todas as vidas.
- Na tela de agradecimento, você pode optar por jogar novamente clicando no botão "Jogar Novamente".

### Hardware

- Aperte o botão de confirmação para iniciar o jogo.
- Use os botões de navegação para selecionar uma das categorias: "Viagem", "Escola" ou "Cotidiano".
- As perguntas serão exibidas no display LCD com as opções de resposta (A, B, C).
- Use os botões de navegação para selecionar a resposta correta e aperte o botão de confirmação.
- LEDs indicam se a resposta está correta (verde) ou incorreta (vermelho).
- O jogo termina quando todas as perguntas são respondidas ou quando você perde todas as vidas. Uma mensagem de agradecimento será exibida no display.

## Créditos

- Desenvolvido por [Henrique Brito, Gabriel Marques, Felipe Marques e Guilherme Silva].
