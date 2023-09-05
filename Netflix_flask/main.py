from flask import Flask, render_template, request, session
from classes import *
from random import choice, randint

def verificar_tema(nome, serie, temas):
    print(nome)
    if nome in temas:
        nome.adicionar_serie(serie)
    

app = Flask(__name__) 
app.secret_key = 'lalala' # armazenada no navegador da pessoa (variavel de sessão)
#(IMPORTÂNCIA: Variavel normal: vale pra qualquer um (global no servidor)| Variavel de SESSÃO: valor armazenado no cache do navegador da pessoa)

# INICIA OBJETOS 
tema_suspense = Tema("Suspense")

serie_stranger_things = Serie("Stranger Things", "strangerthings.jpg", "Quando Will Byers desaparece misteriosamente, seus amigos iniciam uma busca pelo garoto, descobrindo experimentos secretos, forças sobrenaturais e uma garota estranha com poderes telecinéticos.", 4, "4.5 estrelas", "Millie Bobby Brown, Finn Wolfhard")
tema_suspense.adicionar_serie(serie_stranger_things)

serie_dark = Serie("Dark", "dark.jpg", "Em uma cidade pequena, desaparecimentos inexplicáveis ​​levam quatro famílias a uma busca frenética por respostas enquanto tentam desvendar um mistério que abrange três gerações.", 3, "4.8 estrelas", "Louis Hofmann, Oliver Masucci")
tema_suspense.adicionar_serie(serie_dark)

serie_narcos = Serie("Narcos", "narcos.jpg", "Baseada na história real do narcotraficante Pablo Escobar, essa série retrata a vida do poderoso chefão do tráfico e as forças policiais e políticas que tentam capturá-lo.", 5, "4.7 estrelas", "Wagner Moura, Pedro Pascal")
tema_suspense.adicionar_serie(serie_narcos)

tema_policial = Tema("Policial")

serie_lupin = Serie("Lupin", "lupin.jpg", "Em Paris, o ladrão profissional Assane Diop busca vingança pelo injusto tratamento de seu pai, e usa as habilidades de ladrão para expor os crimes da elite.", 2, "4.6 estrelas", "Omar Sy, Ludivine Sagnier")
tema_policial.adicionar_serie(serie_lupin)

serie_casa_de_papel = Serie("La Casa de Papel", "lacasadepapel.jpeg", "Oito ladrões fazem reféns e se trancam na Casa da Moeda da Espanha com o ambicioso plano de realizar o maior roubo da história.", 5, "4.9 estrelas", "Úrsula Corberó, Álvaro Morte")
tema_policial.adicionar_serie(serie_casa_de_papel)

tema_drama = Tema("Drama")

serie_breaking_bad = Serie("Breaking Bad", "breakingbad.jpg", "Um professor de química do ensino médio com câncer terminal se junta a um ex-aluno para produzir e vender metanfetamina para garantir o futuro financeiro de sua família.", 6, "4.9 estrelas", "Bryan Cranston, Aaron Paul")
tema_drama.adicionar_serie(serie_breaking_bad)

serie_ozark = Serie("Ozark", "ozark.jpg", "Um consultor financeiro se muda com sua família para as montanhas Ozark para lavar 500 milhões de dólares e acalmar um traficante de drogas.", 4, "4.7 estrelas", "Jason Bateman, Laura Linney")
tema_suspense.adicionar_serie(serie_ozark)

serie_the_witcher = Serie("The Witcher", "witcher.jpg", "Um caçador de monstros solitário luta para encontrar seu lugar em um mundo onde as pessoas frequentemente se provam mais perversas do que as bestas.", 2, "4.6 estrelas", "Henry Cavill, Anya Chalotra")
tema_suspense.adicionar_serie(serie_the_witcher)


serie_the_crown = Serie("The Crown", "thecrown.jpg", "Esta série dramática segue a vida da rainha Elizabeth II desde sua juventude até a atualidade, explorando os eventos históricos que moldaram o segundo reinado mais longo da história britânica.", 5, "4.8 estrelas", "Olivia Colman, Tobias Menzies")
tema_drama.adicionar_serie(serie_the_crown)

serie_gambito = Serie("O Gambito da Rainha", "gambito.jpg", "Em um orfanato dos anos 1950, uma jovem prodígio do xadrez luta contra o vício enquanto enfrenta os melhores jogadores do mundo.", 1, "4.5 estrelas", "Anya Taylor-Joy, Bill Camp")
tema_drama.adicionar_serie(serie_gambito)

serie_suits = Serie("Suits", "suits.jpg", "Mike Ross, um jovem inteligente que abandonou a faculdade de direito, é contratado pelo advogado mais bem-sucedido de Nova York, Harvey Specter, apesar de não ter diploma de direito.", 9, "4.7 estrelas", "Gabriel Macht, Patrick J. Adams")
tema_drama.adicionar_serie(serie_suits)

catalogo = [tema_suspense, tema_policial, tema_drama]

# FIM DA INICIALIZAÇÃO DO CATÁLOGO

@app.route('/')
def home():
    serieDestaque = ''
    
    if 'login' not in session: # PARA QUANDO NUNCA FEZ LOGIN OU DESLOGOU, LOGO N EXISTE NADA EM SESSION QUANDO VC ABRE O SITE OU DESLOGA
        # cria uma variavel de sessão do navegador para controlar se a pessoa fez login
        # (só funciona dentro de um ambiente que tem método post e get | cria dentro de uma rota)
        
        session['login'] = False # serve pra não acessar rotas sem estar logado

    # escolhe a série destaque (SÓ PARA NÃO DAR ERRO NA COISA LAA WAWAWAWAW)
    temasComSerie = []
    if catalogo != []:
        for tema in catalogo:
            if tema.series == []:
                continue
            elif tema.series != []:
                temasComSerie.append(tema)
        
        if temasComSerie != []:
            serieDestaque = choice(choice(temasComSerie).series)
        

    conteudo = render_template('index.html', parSerieDestaque=serieDestaque, parCatalogo=catalogo) # render_template processa os templates. (é uma função nao biblioteca??)
    return conteudo

erros = 5
rep = 0
email = 'NUH UH'
@app.route("/dashboard", methods=["GET","POST"])# retonar para dashboard sem reiniciar o conteudo da pag
def dashboard():
    # var global
    global erros
    global email
    texto = 'tentativas'
    if request.method == "POST": # se chegou aqui via formulario de login
        email = request.form["email"]
        if request.form["email"] =="2@gmail" and request.form["senha"] == "aaa" and erros >= 1: #se estiver correta ele inicia a sessão com o session["login"] = True
                session["login"] = True
                return render_template("dashboard.html",parCatalogo = catalogo, parNome = email)
        else:
            erros -= 1
            for i in texto:
                    print(i)
                    if i == 's' and erros == 1:
                        texto = 'tentativa'
                        break
            if erros > 0:
                mensagem = f"Inválido, você tem {erros} {texto} "
            else:
                mensagem = "Você não tem mais tentativas "
                    
            return render_template("mensagem.html", parMensagem=mensagem)
        
#se chegar via link com o usuario ja logado
    if request.method == "GET" and session["login"] == True:
        return render_template("dashboard.html", parCatalogo = catalogo, parNome = email) #se for get é pq a pessoa ja realizou o login
    else:
        return render_template("mensagem.html", parMensagem='Acesso negado amigo.')


@app.route('/adicionar_tema', methods=['GET', 'POST'])
def adicionar_tema():
    if request.method == "POST":
        if request.form['tema'] != '':
            for item in catalogo:
                if item.nome == request.form['tema']:
                    return render_template('mensagem.html', parMensagem="Este tema já está cadastrado.", anterior = 'dashboard')
            else:
                novoTema = Tema(request.form['tema'])
                catalogo.append(novoTema)
                return render_template('mensagem.html', parMensagem="Tema Cadastrado com Sucesso", anterior = 'dashboard')
        else:
            return render_template('mensagem.html', parMensagem = "Preencha todos os campos", anterior='dashboard')
    
    elif 'login' not in session or session['login'] == False:
        return render_template('mensagem.html', parMensagem='Acesso negado amigo.')
    
    return render_template('mensagem.html', parMensagem='?', anterior = 'dashboard')
    

@app.route('/processar_tema', methods=['GET', 'POST'])
def processar_tema():
    if request.method == "POST":
        if request.form['titulo'] != '':
            imagem = request.files['imagem'] # pelo amor de Deus
            print(imagem)
            if imagem.filename != "":
                imagem.save('static/images/' + imagem.filename) # jesus (É IMAGEM.FILENAME NÃO SÓ IMAGEM?)
            for item in catalogo:
                if item.nome == request.form['tema']:
                    for serie in item.series:
                        if serie.titulo == request.form['titulo']:
                            return render_template('mensagem.html', parMensagem = 'Esta série já está cadastrada neste tema.', anterior='dashboard')
                    break # achei fassil
                
            print(imagem, '//', imagem.filename) # imagem: <FileStorage: 'wasa.jpeg' ('image/jpeg')> imagem.filename = blablabla.png ???? ok
            item.adicionar_serie(Serie(request.form['titulo'],imagem.filename,request.form['sinopse'],request.form['temporadas'],request.form['avaliacao']+' estrelas',request.form['elenco']))
            return render_template('mensagem.html', parMensagem = 'Série Cadastrada com Sucesso', anterior='dashboard')
        else:
            return render_template('mensagem.html', parMensagem = "Preencha todos os campos", anterior='dashboard') # anterior modificar tema?
        
    return render_template("mensagem.html", parMensagem='Acesso negado amigo.')

@app.route('/modificar_tema/<nome_tema>', methods=['GET', 'POST'])
def modificar_tema(nome_tema):
    if 'login' not in session or session['login'] == False:
        return render_template('mensagem.html', parMensagem='Acesso negado amigo.') 
    
    return render_template('modificar.html', parTema=nome_tema)

# ja ta feito essa parte
@app.route('/excluir_tema/<deletado>', methods=["GET", "POST"])
def excluir_tema(deletado):
    if request.method == "POST":
        for item in catalogo:
            if item.nome == deletado:
                catalogo.remove(item)
                return render_template('mensagem.html', parMensagem=(f'Tema "{item.nome}" excluído com sucesso.'), anterior='dashboard')
                
        return render_template('mensagem.html', parMensagem='Este tema não está cadastrado.', anterior='dashboard') 

    elif 'login' not in session or session['login'] == False:
        return render_template('mensagem.html', parMensagem='Acesso negado amigo.')
    
    return render_template('mensagem.html', parMensagem= "?", anterior='dashboard')
    
@app.route('/excluir_serie', methods=['GET', 'POST'])
def excluir_serie():
    if request.method == "POST":
        for item in catalogo:
            for serie in item.series:
                        if serie.titulo == request.form['titulo'] and item.nome == request.form['tema']:
                            item.remover_serie(serie)
                            return render_template('mensagem.html', parMensagem=(f'Série "{serie.titulo}" excluída com sucesso.'), anterior='dashboard')
                        
        return render_template('mensagem.html', parMensagem='Esta série não está cadastrada.', anterior='dashboard') 
    
    elif 'login' not in session or session['login'] == False:
        return render_template('mensagem.html', parMensagem='Acesso negado amigo.')     
    
    return render_template('mensagem.html', parMensagem= "?", anterior='dashboard')
            
@app.route('/logout')
def logout():
    global erros
    session['login'] = False
    erros = 5
    return render_template('mensagem.html', parMensagem = "Você saiu com sucesso")

if __name__ == '__main__': # serve para debugar o app apenas quando estiver sendo executado DIRETAMENTE do arquivo em que o Flask = app(__name__) foi criado (programa principal(main))
    app.run(debug=True) # debug é tipo hot reload (salvamento automatico)
