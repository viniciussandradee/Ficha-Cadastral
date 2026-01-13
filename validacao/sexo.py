"""
Validação de sexo/gênero para o sistema de ficha cadastral.
Implementa validação inclusiva com múltiplas opções de gênero.
"""

from typing import Dict, Any, Optional

class ValidadorGenero:
    """
    Classe para validação inclusive de gênero/sexo.

    Suporta múltiplas formas de entrada e categoriza automaticamente.

    """

    #mapeamento completo de entradas válidas
    mapeamento_completo: Dict[str, Dict[str, str]] = {
        #códigos curtos (padrão):
        'M': {'display': 'Masculino', 'categoria':'binario', 'codigo':'M'},
        'F': {'display': 'Feminino', 'categoria':'binario', 'codigo':'F'},
        'O': {'display': 'Outro', 'categoria':'nao_binario', 'codigo':'O'},
        'NB': {'display': 'Não Binário', 'categoria':'nao_binario', 'codigo':'NB'},
        'N': {'display': 'Não Binário', 'categoria':'nao_binario', 'codigo':'NB'},
        'X': {'display': 'Não Especificado', 'categoria':'outro', 'codigo': 'X'},
        '': {'display': 'Prefiro não informar', 'categoria': 'nao_informado', 'codigo': ''},

        # Português completo
        'MASCULINO': {'display': 'Masculino', 'categoria': 'binario', 'codigo': 'M'},
        'FEMININO': {'display': 'Feminino', 'categoria': 'binario', 'codigo': 'F'},
        'HOMEM': {'display': 'Masculino', 'categoria': 'binario', 'codigo': 'M'},
        'MULHER': {'display': 'Feminino', 'categoria': 'binario', 'codigo': 'F'},
        'OUTRO': {'display': 'Outro', 'categoria': 'nao_binario', 'codigo': 'O'},
        'OUTROS': {'display': 'Outro', 'categoria': 'nao_binario', 'codigo': 'O'},
        'NÃO BINÁRIO': {'display': 'Não Binário', 'categoria': 'nao_binario', 'codigo': 'NB'},
        'NAO BINARIO': {'display': 'Não Binário', 'categoria': 'nao_binario', 'codigo': 'NB'},
        'NÃO-BINÁRIO': {'display': 'Não Binário', 'categoria': 'nao_binario', 'codigo': 'NB'},
        'NAO-BINARIO': {'display': 'Não Binário', 'categoria': 'nao_binario', 'codigo': 'NB'},
        'NONBINARY': {'display': 'Não Binário', 'categoria': 'nao_binario', 'codigo': 'NB'},
        'NON-BINARY': {'display': 'Não Binário', 'categoria': 'nao_binario', 'codigo': 'NB'},
        'NÃO ESPECIFICADO': {'display': 'Não Especificado', 'categoria': 'outro', 'codigo': 'X'},
        'NAO ESPECIFICADO': {'display': 'Não Especificado', 'categoria': 'outro', 'codigo': 'X'},

        # Inglês
        'MALE': {'display': 'Masculino', 'categoria': 'binario', 'codigo': 'M'},
        'FEMALE': {'display': 'Feminino', 'categoria': 'binario', 'codigo': 'F'},
        'OTHER': {'display': 'Outro', 'categoria': 'nao_binario', 'codigo': 'O'},

        # Números (para formulários antigos)
        '1': {'display': 'Masculino', 'categoria': 'binario', 'codigo': 'M'},
        '2': {'display': 'Feminino', 'categoria': 'binario', 'codigo': 'F'},
        '3': {'display': 'Outro', 'categoria': 'nao_binario', 'codigo': 'O'},
        '9': {'display': 'Não especificado', 'categoria': 'outro', 'codigo': 'X'},
    }

    @classmethod
    def validar(cls, entrada: Optional[str]) -> Dict[str, Any]:
        """
        Valida e normaliza entrada de gênero de forma inclusiva

        Args:
            entrada: String com gênero informado (ou None/vazio)

        Returns:
            dict: {
                'valor': 'M', #código curto
                'display': 'Masculino' #Para Exibição
                'categoria': 'binario', #Categoria lógica
                'entrada_original': 'M' #Entrada original
            }
        """

        #trata valores vazios
        if entrada is None:
            return {
                'valor': '',
                'display': 'Prefiro não informar',
                'categoria': 'nao_informado',
                'entrada_original': ''
            }

        if isinstance(entrada, str) and entrada.strip() == '':
            return {
                'valor': '',
                'display': 'Prefiro não informar',
                'categoria': 'nao_informado',
                'entrada_original': entrada
            }

        entrada_original = entrada.strip()
        entrada_upper = entrada_original.upper()

        #1. Procura correspondência exata
        if entrada_upper in cls.mapeamento_completo:
            dados = cls.mapeamento_completo[entrada_upper].copy()
            dados['valor'] = dados['codigo']
            dados['entrada_original'] = entrada_original
            return dados

        # 2. Procura correspondência parcial (MAS com prioridade para correspondências exatas)
        #Primeiro, tenta encontrar a correspondência mais específica

        correspondencias = []

        for chave, valor in cls.mapeamento_completo.items():
            if not chave:
                continue
            # Se a entrada contém a chave completa (para coisas como "Não Binário")
            if chave in entrada_upper and len(chave) > 3:  # Só para palavras completas
                correspondencias.append((len(chave), chave, valor))  # (tamanho, chave, valor)

        # Se encontrou correspondências, pega a mais longa (mais específica)
        if correspondencias:
            correspondencias.sort(reverse=True)  # Ordena pelo tamanho (maior primeiro)
            _, chave, valor = correspondencias[0]  # Pega a mais específica
            dados = valor.copy()
            dados['valor'] = dados['codigo']
            dados['entrada_original'] = entrada_original
            return dados

        # 3. Tenta correspondência por início (apenas para códigos curtos)
        for chave, valor in cls.mapeamento_completo.items():
            if not chave:
                continue
            if len(chave) <= 2 and entrada_upper.startswith(chave):
                dados = valor.copy()
                dados['valor'] = dados['codigo']
                dados['entrada_original'] = entrada_original
                return dados

        # 4. Se não encontrou, retorna como "Outro" preservando a entrada
        return {
            'valor': 'O',
            'display': entrada_original,  # Mantém como o usuário digitou
            'categoria': 'outro',
            'entrada_original': entrada_original
        }

    @classmethod
    def obter_opcoes_validas(cls) -> Dict[str, str]:
        """
        Retorna as opções válidas formatadas para exibição

        Returns:
            dict: Opções no formato {'M': 'Masculino', 'F': 'Feminino', ...}

        """

        opcoes = {}
        for codigo, dados in cls.mapeamento_completo.items():
            if len(codigo) <= 2 and codigo and 'codigo' in dados: #apenas códigos curtos
                opcoes[dados['codigo']] = dados['display']
        return dict(sorted(opcoes.items()))

def validar_sexo(entrada: Optional[str]) -> Dict[str, Any]:
    """
    Função simplificada para validação de sexo/gênero

    Args:
        entrada: Sexo/gênero informado pelo usuário

    Returns:
        dict: Dados validados do gênero

    """
    return ValidadorGenero.validar(entrada)

def obter_sexo_usuario() -> Dict[str, Any]:
    """
    Interage com o usuario para obter gênero de forma inclusiva.

    Returns:
        dict: Dados Validados de Gênero

    """

    print('\nINFORMAÇÕES DE IDENTIDADE')
    print('-' * 40)
    print('Como você se identifica?')
    print('(Deixe em branco se preferir não informar)')
    print('\nOpções Comuns: ')

    opcoes = ValidadorGenero.obter_opcoes_validas()
    for codigo, descricao in opcoes.items():
        print(f'{codigo}: {descricao}')

    print('\nVocê também pode digitar por extenso: ')
    print("  Exemplos: 'Não Binário', 'Outro', 'Masculino', etc...' ")

    while True:
        try:
            entrada = input('\nSua identidade de gênero: ').strip()
            resultado = validar_sexo(entrada)

            #Mostra confirmação amigável
            if resultado['categoria'] == 'nao_informado':
                print(f'REGISTRADO: Prefiro não informar')
            else:
                print(f"REGISTRADO: {resultado['display']}")

            #Adiciona emoji baseado na categoria:
            if resultado['categoria'] == 'binario':
                print("   👤 Categoria: Binário")
            elif resultado['categoria'] == 'nao_binario':
                print("   🦋 Categoria: Não binário")
            elif resultado['categoria'] == 'outro':
                print("   🌈 Categoria: Outro")

            return resultado
        except ValueError as e:
            print(f'Ocorreu um Erro: {e}')
            print('Tente novamente, por favor')

def formatar_sexo(entrada: Optional[str]) -> str:
    """
    Formata em sexo/gênero para exibição amigável

    Args:
        entrada: Sexo/gênero informado

    Returns:
        str: Texto formatado para exibição

    """
    dados = validar_sexo(entrada)
    return dados['display']

def obter_sexo_simplificado(entrada: Optional[str]) -> str:
    """
    Retorna apenas o código simplificado (M, F, O, NB ou vazio)

    Args:
        entrada: Sexo/gênero informado

    Returns:
        str: código de 1-2 caracteres

    """

    dados = validar_sexo(entrada)
    return dados['valor']

#teste de módulo
if __name__ == '__main__':
    print('TESTANDO VALIDAÇÃO DE GÊNERO/SEXO')
    print('-' * 60)

    #1. Teste de validação de várias entradas
    print('\n1. TESTE DE VALIDAÇÃO DE DIFERENTES ENTRADAS...')
    print('-' * 40)

    testes = [
        #Entradas Comuns
        "M", "F", "m", "f",
        "Masculino", "Feminino", "masculino", "feminino",
        "Homem", "Mulher", "HOMEM", "MULHER",

        #Não Binários e outras identidades
        "NB", "N", "Não Binário", "Não-Binário", "nao binario",
        "Outro", "OUTRO", "Outros",
        "X", "Não Especificado",

        #Inglês
        "Male", "Female", "Other", "NonBinary",

        #Vazio ou não informado
        "", " ", None,

        #Entradas personalizadas (serão corrigidas como "Outro")
        "Agênero", "Genderfluid", "Bigênero", "Transgênero",

        #Seu Teste
        "Masculino", #Seu gênero

    ]

    for teste in testes:
        if teste is None:
            print(f'\nTestando: None')
        else:
            print(f'\nTestando: "{teste}"')

        resultado = validar_sexo(teste)

        print(f'Valor:   "{resultado["valor"]}"')
        print(f'Display: "{resultado["display"]}"')
        print(f'Categoria: "{resultado["categoria"]}"')
        print(f'Original: "{resultado["entrada_original"]}"')

    #2. Teste Opção Válidas
    print('\n\n2. OPÇÕES VÁLIDAS (códigos curtos): ')
    print('-' * 40)

    opcoes = ValidadorGenero.obter_opcoes_validas()
    for codigo, descricao in opcoes.items():
        print(f'{codigo:2} -> {descricao}')

    #3. Teste de Formatação Simplificada
    print('\n\n3. TESTES DE FORMATAÇÃO:')
    print('-' * 40)

    entradas_formatacao = ['M', 'f', 'NB', 'não binário', '', "Agênero"]
    for entrada in entradas_formatacao:
        formatado = formatar_sexo(entrada)
        simplificado = obter_sexo_simplificado(entrada)
        print(f'\n"{entrada}" -> Display: {formatado}| Código: "{simplificado}"')

    #4. Teste de Interação com o Usuario
    print('\n\n4. TESTE DE INTERAÇÃO COM O USUARIO: ')
    print('-' * 60)

    # Descomente para testar interação
    # print("\nSimulando interação com usuario...")
    # resultado = obter_sexo_usuario()
    # print(f"\n Resultado completo: ")
    # for chave, valor in resultado.items():
    #     print(f"  {chave}: {valor}")

    print('\nTESTE ESPECIAL - SUA IDENTIDADE')
    print('-' * 40)

    seu_genero = 'Masculino'
    print(f'TESTANDO...: "{seu_genero}"')

    resultado = validar_sexo(seu_genero)
    print(f'DISPLAY: {resultado["display"]}')
    print(f'CÓDIGO: {resultado["valor"]}')
    print(f'CATEGORIA: {resultado["categoria"]}')
