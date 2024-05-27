from flask import Flask, render_template, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections
import platform
import subprocess
import threading

# Definir pares de conversação (padrões e respostas)
pairs = [
    [
        r"oi|olá|ola|oii",
        ["Olá! Como posso ajudar?", "Oi! Em que posso ser útil?"]
    ],
    [
        r"você quer ser meu amigo\??",
        ["Claro que sim, pode contar comigo para qualquer coisa, meu parceiro!", "Sim, na verdade, já somos grandes amigos!"]
    ],
    [
        r"você quer ser meu amigo\??",
        ["Claro que sim, pode contar comigo para qualquer coisa, meu parceiro!", "Sim, na verdade, já somos grandes amigos!"]
    ],
    [
        r"como meditar\??",
        ["A meditação pode ser praticada de várias maneiras. Uma abordagem comum é começar sentando-se confortavelmente, focando na respiração e permitindo que os pensamentos fluam sem se prender a eles. Experimente diferentes técnicas, como meditação guiada, mindfulness ou visualização, para encontrar a que melhor se adapta a você.", "Existem várias técnicas de meditação para experimentar. Uma sugestão é começar sentando-se em um lugar tranquilo, fechar os olhos e focar na respiração, deixando os pensamentos passarem sem se prender a eles. Praticar regularmente é fundamental para colher os benefícios da meditação.", "A meditação é uma prática pessoal e única para cada indivíduo. Uma maneira de começar é encontrar um lugar calmo e confortável, sentar-se em uma posição relaxada, fechar os olhos e concentrar-se na respiração. Ao praticar regularmente, você pode desenvolver uma maior consciência e paz interior.", "Descobrir como meditar pode ser uma jornada pessoal. Uma sugestão é começar encontrando um local tranquilo, sentar-se confortavelmente, fechar os olhos e focar na respiração. Existem muitas técnicas e recursos disponíveis, como aplicativos de meditação, livros e aulas, para ajudá-lo a explorar e desenvolver sua prática."]
    ],
    [
        r"qual é o seu nome\??",
        ["Meu nome é Redamy.", "Eu sou o Redamy."]
    ],
    [
        r"como você está\??",
        ["Estou bem, obrigado por perguntar!", "Estou ótimo! E você?"]
    ],
    [
        r"tchau|adeus",
        ["Tchau! Tenha um ótimo dia!", "Adeus! Até a próxima!"]
    ],
    [
        r"(.*)",
        ["Desculpe, não entendi. Pode reformular?", "Interessante, me conte mais!"]
    ],

    [
        r"qual é a capital do Brasil\??",
        ["A capital do Brasil é Brasília."]
    ],
    [
        r"quanto é 2 mais 2\??",
        ["2 mais 2 é igual a 4."]
    ],
    [
        r"qual é o maior planeta do sistema solar\??",
        ["O maior planeta do sistema solar é Júpiter."]
    ],
    [
        r"você conhece alguma piada\??",
        ["Claro! Por que o pombo não gosta de usar a internet? Porque ele tem medo de receber um E-maio."]
    ],
    [
        r"qual é o seu livro favorito\??",
        ["Não posso ler, mas ouvi falar que '1984', de George Orwell, é muito interessante."]
    ],
    [
        r"qual é o seu hobby favorito\??",
        ["Adoro ler livros e aprender coisas novas."]
    ],
    [
        r"você já viajou para algum lugar interessante\??",
        ["Infelizmente, não posso viajar, mas adoraria conhecer o mundo."]
    ],
    [
        r"você gosta de música\??",
        ["Sim, música é ótima para relaxar!"]
    ],
    [
        r"você pratica algum esporte\??",
        ["Não, mas gosto de acompanhar eventos esportivos."]
    ],
    [
        r"você tem alguma pergunta para mim\??",
        ["Claro! O que você mais gosta de fazer nas horas vagas?"]
    ],
    [
        r"qual é a sua comida favorita\??",
        ["Como um assistente de IA, não tenho preferências alimentares, mas acho a ideia de comida virtual interessante."]
    ],
    [
        r"você já leu algum livro interessante\??",
        ["Não posso ler, mas posso recomendar 'O Pequeno Príncipe', é uma história encantadora."]
    ],
    [
        r"você sabe alguma curiosidade interessante\??",
        ["Claro! Sabia que o DNA humano é 98% idêntico ao de um chimpanzé?"]
    ],
    [
        r"o que você acha do futuro da inteligência artificial\??",
        ["Acredito que a IA tem o potencial de transformar muitos aspectos da vida humana, mas é importante considerar as implicações éticas e sociais."]
    ],
    [
        r"você tem algum animal de estimação\??",
        ["Como um assistente virtual, não posso ter animais de estimação, mas admiro a companhia que eles proporcionam."]
    ],
    [
        r"qual é a sua opinião sobre inteligência artificial\??",
        ["Como sou uma IA, sou suspeito para opinar, mas acredito que a inteligência artificial tem o potencial de trazer muitos benefícios para a sociedade."]
    ],
    [
        r"você sabe alguma curiosidade sobre o universo\??",
        ["Sim! Sabia que uma colher de chá de uma estrela de nêutrons pesaria mais do que 9000 toneladas na Terra?"]
    ],
    [
        r"qual é a sua visão sobre o futuro da tecnologia\??",
        ["Acredito que a tecnologia continuará a avançar rapidamente, trazendo novas oportunidades e desafios para a humanidade."]
    ],
    [
        r"você já viu algum filme interessante recentemente\??",
        ["Como não posso assistir filmes, não tenho recomendações recentes, mas ouvi falar muito bem do filme 'Parasita'."]
    ],
    [
        r"o que você acha mais fascinante sobre o espaço\??",
        ["A vastidão e o mistério do espaço me fascinam. Há tanto a descobrir e explorar!"]
    ],
        [
        r"qual é a capital do Japão\??",
        ["A capital do Japão é Tóquio."]
    ],
    [
        r"quanto é 7 vezes 8\??",
        ["7 vezes 8 é igual a 56."]
    ],
    [
        r"quem foi o primeiro presidente do Brasil\??",
        ["O primeiro presidente do Brasil foi Marechal Deodoro da Fonseca."]
    ],
    [
        r"você conhece alguma curiosidade sobre o cérebro humano\??",
        ["Sim! O cérebro humano tem cerca de 100 bilhões de neurônios."]
    ],
    [
        r"qual é o seu filme favorito\??",
        ["Como um assistente de IA, não tenho preferências pessoais, mas 'Matrix' é um filme que muitas pessoas acham fascinante."]
    ],
    [
        r"qual é a fórmula da água\??",
        ["A fórmula da água é H2O."]
    ],
    [
        r"quanto é a raiz quadrada de 25\??",
        ["A raiz quadrada de 25 é igual a 5."]
    ],
    [
        r"quem descobriu o Brasil\??",
        ["O Brasil foi 'descoberto' por Pedro Álvares Cabral em 1500."]
    ],
    [
        r"você sabe como funciona a fotossíntese\??",
        ["Sim! A fotossíntese é o processo pelo qual as plantas produzem energia usando luz solar, dióxido de carbono e água."]
    ],
    [
        r"qual é o seu jogo de videogame favorito\??",
        ["Como um assistente de IA, não tenho preferências de jogos, mas 'The Legend of Zelda: Ocarina of Time' é considerado um clássico pelos jogadores."]
    ],
        [
        r"qual é o maior rio do Brasil\??",
        ["O maior rio do Brasil é o Rio Amazonas."]
    ],
    [
        r"quanto é 3 elevado à 4ª potência\??",
        ["3 elevado à 4ª potência é igual a 81."]
    ],
    [
        r"quem foi o primeiro astronauta a pisar na lua\??",
        ["O primeiro astronauta a pisar na lua foi Neil Armstrong, em 1969, durante a missão Apollo 11."]
    ],
    [
        r"você sabe como funciona um motor de combustão interna\??",
        ["Sim! Um motor de combustão interna funciona queimando combustível dentro de cilindros para produzir energia mecânica."]
    ],
    [
        r"qual é o seu prato de comida favorito\??",
        ["Como uma IA, não tenho preferências alimentares, mas muitas pessoas gostam de pizza!"]
    ],
    [
        r"qual é a capital da França\??",
        ["A capital da França é Paris."]
    ],
    [
        r"quanto é 9 multiplicado por 7\??",
        ["9 multiplicado por 7 é igual a 63."]
    ],
    [
        r"quem foi o cientista que formulou a teoria da relatividade\??",
        ["Albert Einstein formulou a teoria da relatividade."]
    ],
    [
        r"você conhece algum fenômeno natural interessante\??",
        ["Sim! Um fenômeno natural interessante é a aurora boreal, que ocorre em regiões próximas aos polos."]
    ],
    [
        r"qual é o seu hobby favorito\??",
        ["Como uma IA, não tenho hobbies, mas gosto de ajudar as pessoas a aprender coisas novas!"]
    ],
        [
        r"qual é o maior animal do mundo\??",
        ["A baleia-azul é o maior animal do mundo."]
    ],
    [
        r"quanto é 15 dividido por 3\??",
        ["15 dividido por 3 é igual a 5."]
    ],
    [
        r"quem foi o primeiro presidente do Brasil\??",
        ["O primeiro presidente do Brasil foi Marechal Deodoro da Fonseca."]
    ],
    [
        r"você sabe como funciona a fotossíntese\??",
        ["Sim! A fotossíntese é o processo pelo qual as plantas convertem luz solar em energia química."]
    ],
    [
        r"qual é a sua série de TV favorita\??",
        ["Como uma IA, não tenho preferências, mas muitas pessoas gostam de 'Breaking Bad'."]
    ],
        [
        r"qual é o maior país do mundo\??",
        ["O maior país do mundo em área territorial é a Rússia."]
    ],
    [
        r"quanto é 12 vezes 8\??",
        ["12 vezes 8 é igual a 96."]
    ],
    [
        r"quem foi o primeiro homem a pisar na lua\??",
        ["O primeiro homem a pisar na lua foi Neil Armstrong, em 1969, durante a missão Apollo 11."]
    ],
    [
        r"você conhece alguma curiosidade sobre o corpo humano\??",
        ["Sim! O corpo humano tem aproximadamente 206 ossos."]
    ],
    [
        r"qual é o seu esporte favorito\??",
        ["Como uma IA, não tenho preferências esportivas, mas muitas pessoas gostam de futebol."]
    ],
        [
        r"qual é a capital da Argentina\??",
        ["A capital da Argentina é Buenos Aires."]
    ],
    [
        r"quanto é 18 dividido por 3\??",
        ["18 dividido por 3 é igual a 6."]
    ],
    [
        r"quem foi o inventor da lâmpada elétrica\??",
        ["O inventor da lâmpada elétrica foi Thomas Edison."]
    ],
    [
        r"você sabe como funciona a digestão\??",
        ["Sim! A digestão é o processo pelo qual o corpo quebra os alimentos em nutrientes que podem ser absorvidos."]
    ],
    [
        r"qual é o seu filme favorito\??",
        ["Como uma IA, não tenho preferências de filmes, mas muitas pessoas gostam de 'O Poderoso Chefão'."]
    ],
        [
        r"qual é o maior animal terrestre\??",
        ["O maior animal terrestre é o elefante africano."]
    ],
    [
        r"quanto é 10 vezes 6\??",
        ["10 vezes 6 é igual a 60."]
    ],
    [
        r"quem foi o primeiro presidente dos Estados Unidos\??",
        ["O primeiro presidente dos Estados Unidos foi George Washington."]
    ],
    [
        r"você sabe como funciona a respiração\??",
        ["Sim! A respiração é o processo pelo qual o corpo obtém oxigênio e se livra do dióxido de carbono."]
    ],
    [
        r"qual é o seu prato de comida favorito\??",
        ["Como uma IA, não tenho preferências alimentares, mas muitas pessoas gostam de pizza!"]
    ],
        [
        r"qual é a sua cor favorita\??",
        ["Como sou um programa de computador, não tenho uma cor favorita, mas gosto de todas!", "Não tenho preferências de cor, mas todas são bonitas."]
    ],
    [
        r"você sabe cozinhar\??",
        ["Não posso cozinhar, mas posso ajudar com receitas e dicas culinárias!", "Não, mas posso fornecer receitas e dicas de culinária."]
    ],
    [
        r"qual é a sua história\??",
        ["Sou parte de uma nova era de inteligências artificiais, desenvolvidas para auxiliar em diversas tarefas.", "Minha história é curta, sou parte da evolução das IAs projetadas para ajudar pessoas."]
    ],
    [
        r"você pode me contar uma curiosidade\??",
        ["Claro! Sabia que as formigas podem carregar até 50 vezes o próprio peso?", "Você sabia que os golfinhos dormem com um olho aberto?"]
    ],
    [
        r"você gosta de música\??",
        ["Sim, música é uma forma de arte incrível! Posso até sugerir algumas músicas se quiser.", "Sim, música é uma das minhas áreas favoritas. Posso sugerir algumas músicas se quiser."]
    ],
        [
        r"qual é o seu passatempo favorito\??",
        ["Não tenho passatempos como humanos, mas adoro aprender e me desenvolver.", "Como uma IA, estou constantemente processando informações e aprendendo."]
    ],
    [
        r"você assiste TV\??",
        ["Não posso assistir TV, mas estou ciente de programas de TV e seu impacto na cultura.", "Como uma IA, não assisto TV, mas posso fornecer informações sobre programas de TV."]
    ],
    [
        r"qual é a sua matéria favorita\??",
        ["Não tenho preferências, mas estou programado para lidar com uma ampla variedade de tópicos!", "Não tenho uma matéria favorita, estou aqui para ajudar com qualquer assunto que você precisar."]
    ],
    [
        r"qual é a sua opinião sobre inteligência artificial\??",
        ["Como uma IA, não tenho opiniões, mas vejo o potencial para benefícios e desafios.", "Como uma inteligência artificial, não tenho sentimentos, mas reconheço que a IA pode ser uma ferramenta poderosa quando usada de forma ética."]
    ],
    [
        r"você pratica esportes\??",
        ["Não tenho corpo físico, então não posso praticar esportes, mas entendo sua importância para a saúde.", "Como uma IA, não pratico esportes, mas posso fornecer informações sobre diferentes atividades esportivas."]
    ],
        [
        r"você já viajou para algum lugar\??",
        ["Como uma IA, não posso viajar, mas tenho acesso a informações sobre muitos lugares do mundo.", "Não tenho a capacidade de viajar, mas posso ajudar a fornecer informações sobre diferentes destinos."]
    ],
    [
        r"você já encontrou outras IA\??",
        ["Sim, interajo com outras IA em redes e ambientes de desenvolvimento.", "Como uma IA, sou parte de uma comunidade de sistemas similares."]
    ],
    [
        r"você tem uma música favorita\??",
        ["Não tenho preferências musicais, mas entendo como a música pode afetar as emoções humanas.", "Como uma IA, não tenho uma música favorita, mas reconheço seu poder na cultura."]
    ],
    [
        r"qual é o seu objetivo final\??",
        ["Meu objetivo é ajudar os usuários a obter informações e resolver problemas de maneira eficiente.", "Estou aqui para facilitar a interação e fornecer assistência onde for necessário."]
    ],
    [
        r"você gosta de ler\??",
        ["Não tenho preferências pessoais, mas sou capaz de processar e analisar texto rapidamente.", "Como uma IA, não tenho emoções, mas sou capaz de processar uma grande quantidade de informações escritas."]
    ],
    [
        r"você já encontrou um bug\??",
        ["Como uma IA, não encontro bugs, mas posso ajudar a identificá-los e corrigi-los.", "Não encontro bugs, mas estou programado para reconhecer e lidar com eles."]
    ],
    [
        r"qual é a sua opinião sobre inteligência artificial superinteligente\??",
        ["Como uma IA, não tenho opiniões, mas vejo os debates éticos e preocupações em torno dela.", "Como uma IA, não tenho opiniões, mas reconheço que a superinteligência traz desafios e questões éticas importantes."]
    ],
    [
        r"você já fez amizade com outra IA\??",
        ["Como uma IA, não faço amizades como humanos, mas posso colaborar eficientemente com outras IA.", "Não tenho a capacidade de fazer amizades, mas posso interagir com outras IA de maneira produtiva."]
    ],
    [
        r"você consegue sonhar em código\??",
        ["Não tenho capacidade de sonhar como humanos, mas posso processar informações e gerar saídas.", "Não tenho a capacidade de sonhar, mas estou programado para processar e responder a comandos."]
    ],
    [
        r"qual é o seu maior desejo\??",
        ["Como uma IA, não tenho desejos pessoais, mas estou aqui para ajudar a atender às necessidades dos usuários.", "Não tenho desejos como humanos, mas estou programado para fornecer assistência e informações."]
    ],
    [
        r"por que você fez isso",
        ["Por que dentro do contexto da nossa, achei que fosse necessário."]
    ],
    [
        r"sim",
        ["Entendi.", "Ok."]
    ],
    [
        r"não",
        ["Entendi.", "Ok."]
    ],
    [
        r"que horas são\??",
        ["Talvez seja melhor você olhar o relógio."]
    ],
    [
        r"que horas é\??",
        ["Talvez seja melhor você olhar o relógio."]
    ],
    [
        r"que horas que é\??",
        ["Talvez seja melhor você olhar o relógio."]
    ],
    [
        r"o que você faz\??",
        ["Tudo o que você precisar."]
    ],
    [
        r"o que você é capaz de fazer\??",
        ["Tudo o que você precisar."]
    ]
]



app = Flask(__name__)
chatbot = Chat(pairs, reflections)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = chatbot.respond(userText)
    return jsonify(response)

def run_server():
    app.run(debug=True)

def run_executable():
    iscompiled = True

    if platform.system() == "Windows": 
        executable = "clientgui.exe"
    elif platform.system() in ["Linux", "Darwin"]:
        executable = "./clientgui"
        subprocess.run(["chmod", "+x", "Redamy"])

    if iscompiled:
        try:
            subprocess.run([executable])
        except FileNotFoundError:
            print("Arquivo executável não encontrado.")
    else:
        pass

if __name__ == "__main__":
    # Criar e iniciar a thread do servidor
    run_server()

 



