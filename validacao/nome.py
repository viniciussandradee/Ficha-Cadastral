"""
Validação de nomes para o sistema de Ficha Cadastral
"""

import re
from typing import Optional

def validar_nome(nome: str) -> str:
    """
    Valida e Formata um nome Completo

    Regras:
    1. Minimo: 5 caracteres
    2. Máximo: 100 caracteres
    3. Apenas letras, espaços, hifens e apostrofos
    4. Pelo menos um espaço (nome e sobrenome)

    Args:
        nome: Nome a ser validado

    Returns:
        str: nome validado e formatado

    Raises:
        ValueError: se o nome for inválido

    """
    if not nome:
        raise ValueError('Nome não pode ser vazio')

    nome = nome.strip()

    if len(nome) < 5:
        raise ValueError('Nome deve ter, pelo menos, 5 caracteres')
    if len(nome) > 100:
        raise ValueError('Nome não pode exceder 100 caracteres')

    padrao = r'^[A-Za-zÀ-ÿ\s\-\']+$'
    if not re.match(padrao,nome):
        raise ValueError(
            "Nome deve conter apenas letras, espaços, hífens (-) ou apóstrofos (')"
        )
    if ' ' not in nome:
        raise ValueError('Informe nome e sobrenome completo')
    if '  ' in nome:
        nome = ' '.join(nome.split())

    preposicoes = {'de', 'da', 'do', 'das', 'dos', 'e'}
    partes = nome.split()
    partes_formatadas = []

    for i, parte in enumerate(partes):
        if i > 0 and parte.lower() in preposicoes:
            partes_formatadas.append(parte.lower())
        else:
            partes_formatadas.append(parte.capitalize())
    return ' '.join(partes_formatadas)


def obter_nome_usuario() -> str:
    """
    Interage com o usuario para obter um nome válido

    :Returns:
        str: nome validado e formatado

    """

    print('\nINFORMAÇÕES PESSOAIS')
    print('-' * 30)
    print('Digite nome e sobrenome completos')

    while True:
        try:
            entrada = input('Digite o nome: ')
            nome_validado = validar_nome(entrada)

            print(f'Nome Registrado: {nome_validado}')
            return nome_validado
        except ValueError as e:
            print(f'Erro: {e}')
            print('Por favor, digite novamente. \n')

def extrair_primeiro_nome(nome_completo: str) -> str:
    """
    Extrai o primeiro nome de um nome completo.

    Args:
        nome_completo: Nome completo validado

    Returns:
        str: primeiro nome apenas

    """
    return nome_completo.split()[0]

def extrair_sobrenome(nome_completo: str) -> str:
    """
    Extrai o sobrenome (último nome) de um nome completo.

    Args:
        nome_completo: nome completo validado

    Returns:
        str: Sobrenome apenas

    """
    partes = nome_completo.split()
    return partes[-1] if len(partes) > 1 else ""

if __name__ == '__main__':
    print('TESTANDO VALIDAÇÃO DE NOMES...')
    print('-' * 50)

    testes = [
        "Vinicius Barcellos", #Válido
        "maria silva", #Válido (será capitalizado)
        "joão", #inválido (falta sobrenome)
        "", #inválido (vazio)
        "a", #inválido (muito curto)
        "Ana Maria de Souza", #válido
        "123 João", #inválido (tem números)
        "  Carlos Santana  ", #válido (espaços extras)
    ]
    for teste in testes:
        print(f'\nTestando: "{teste}"')
        try:
            resultado = validar_nome(teste)
            print(f'Válido: {resultado}')
            print(f'Primeiro nome: {extrair_primeiro_nome(resultado)}')
            print(f'Sobrenome: {extrair_sobrenome(resultado)}')
        except ValueError as e:
            print(f'Erro: {e}')
    print('\n' + "-" * 50)
    print('Teste de interação com usuario: ')
    print('-' * 50)

    # Descomente para testar interação
    # nome = obter_nome_usuario()
    # print(f"\nNome obtido: {nome}")