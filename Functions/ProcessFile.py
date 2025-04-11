import re

def processar_arquivo(caminho_arquivo, grafo):

    # Abre e lê o conteúdo do arquivo
    with open(caminho_arquivo, "r") as a:
        conteudo = a.read()

    # Encontrar o e-mail do remetente
    f = r'(?:From:)\s([\w.-]+@[\w.-]+)'
    remetentes = re.findall(f, conteudo)
    
    # Encontrar a lista de destinatários
    to = r'To:(.*?)(?:\n\S|$)'
    busca_destinatarios = re.search(to, conteudo, re.DOTALL)
                                                    # o dotall serve para não parar em quebras de linhas

    emails_to = []
    if busca_destinatarios:
        # Substitui quebras de linha por espaço e extrai os e-mails
        linha_to = busca_destinatarios.group(1).replace('\n', ' ') 
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', linha_to)

        # padronizar tudo minusculo
        for email in emails:
            emails_to.append(email.lower())

    # Só entra se tiver remetente e pelo menos um destinatário
    if remetentes and emails_to:
        remetente = remetentes[0].lower()
        destinatarios = emails_to

        destinatarios_filtrados = []

        # Filtra destinatários válidos (com @ e sem espaços desnecessários)
        for d in destinatarios:
            if "@" in d:
                d = d.strip()
                destinatarios_filtrados.append(d)

        destinatarios = destinatarios_filtrados
        
        # Ignora se não sobrou nenhum destinatário válido
        if not destinatarios:
            return

        # Atualiza o grafo com as arestas
        for destinatario in destinatarios:
            if grafo.edge_exists(remetente, destinatario):
                peso_atual = grafo.get_weight(remetente, destinatario)
                grafo.add_edge(remetente, destinatario, peso_atual + 1)
            else:
                grafo.add_edge(remetente, destinatario, 1)