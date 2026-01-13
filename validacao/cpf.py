"""
Validação de CPF para o sistema de Ficha Cadastral
Implementa algoritmo oficial de validação de CPF brasileiro.
"""

import re
from typing import Tuple

def limpar_cpf(cpf: str) -> str:
    """
    Remove todos os caracteres não númericos do CPF

    Args:
         cpf: CPF em qualquer formato (com pontos, traços, ou sem)

    Returns:
        str: CPF com apenas 11 dígitos numéricos.
    """
    return ''.join(filter(str.isdigit, cpf))

def validar_formato(cpf: str) -> str:
    """
    Valida o formato básico do CPF (11 dígitos, singulares).

    Args:
        cpf: CPF já limpo (apenas números)

    Returns:
        str: CPF limpo, se formato válido

    Raises:
        ValueError: Se formato for inválido

    """

    if len(cpf) != 11:
        raise ValueError('CPF deve conter 11 dígitos')
    if cpf == cpf[0] * 11:
        raise ValueError('CPF não pode ter todos os dígitos iguais')

    return cpf

def calcular_digito_verificador(cpf_parcial: str, peso_inicial: int) -> int:
    """
    Calcula um dígito verificado do CPF

    Algoritmo:
    1. Multiplica cada dígito por um peso decrescente
    2. Soma todos os resultados
    3. Calcula: 11 - (soma % 11)
    4. Se resultado > 9, dígito = 0

    Args:
        cpf_parcial: Primeiros 9 ou 10 dígitos do CPF
        peso_inicial: Peso inicial para multiplicação (10 ou 11)

    Returns:
        int: Digito verificador calculado (0-9)

    """
    soma = 0
    peso = peso_inicial

    for digito in cpf_parcial:
        soma += int(digito) * peso
        peso -= 1

    resto = soma % 11
    if resto < 2:
        return 0
    else:
        return 11 - resto

def validar_digitos_verificadores(cpf: str) -> bool:
    """
    Valida os dois dígitos verificadores do CPF.

    Args:
        cpf: CPF com 11 dígitos (formato válido)

    Returns:
        bool: True se dígitos verificadores estiverem corretos

    """

    #primeiros 9 dígitos
    nove_digitos = cpf[:9]

    #calcula primeiro dígito verificador
    digito1 = calcular_digito_verificador(nove_digitos, 10)

    #calcula segundo dígito verificador (incluindo o primeiro calculado)
    dez_digitos = nove_digitos + str(digito1)
    digito2 = calcular_digito_verificador(dez_digitos, 11)

    #verifica se os dígitos calculados bater com os informados
    return cpf[-2:] == f'{digito1}{digito2}'

def validar_cpf(cpf: str) -> str:
    """
    Valida um CPF completo (formato e dígitos verificadores)

    Args:
        cpf: CPF em qualquer formato

    Returns:
        str: CPF formatado no padrão 000.000.000-00

    Raises:
        ValueError: se CPF for inválido

    """

    if not cpf:
        raise ValueError('CPF não pode ser vazio')

    #limpa o CPF (remove pontos, traços, espaços)
    cpf_limpo = limpar_cpf(cpf)

    #valida formato básico
    cpf_limpo = validar_formato(cpf_limpo)

    #valida dígitos verificadores
    if not validar_digitos_verificadores(cpf_limpo):
        raise ValueError('CPF inválido (dígitos verificadores incorretos)')

    #formata para retorno
    return formatar_cpf(cpf_limpo)

def formatar_cpf(cpf: str) -> str:
    """
    Formata CPF no padrão brasileiro: 000.000.000-00

    Args:
         cpf: CPF limpo (11 dígitos)

    Returns:
        str: CPF formatado

    """

    cpf_limpo = limpar_cpf(cpf)
    if len(cpf_limpo) != 11:
        return cpf #retorna como está se não tiver 11 dígitos

    return f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'

def gerar_cpf_valido() -> str:
    """
    Gera um cpf válido para testes (não é um cpf real de uma pessoa).
    
    Returns:
        str: CPF válido gerado aleatoriamente
        
    """

    import random

    #gera os primeiros 9 dígitos aleatórios
    nove_digitos = ''.join(str(random.randint(0, 9)) for _ in range(9))

    #garante que não são todos iguais
    while nove_digitos == nove_digitos[0] * 9:
        nove_digitos = ''.join(str(random.randint(0.9) for _ in range(9)))

    #calcula dígitos verificadores
    digito1 = calcular_digito_verificador(nove_digitos, 10)
    dez_digitos = nove_digitos + str(digito1)
    digito2 = calcular_digito_verificador(dez_digitos, 11)

    cpf_completo = dez_digitos + str(digito2)

    return formatar_cpf(cpf_completo)

def obter_cpf_usuario() -> str:
    """
    Interage com o usuario para obter um CPF válido

    Returns:
        str: CPF válido e formatado

    """

    print('\nINFORMAÇÕES DO DOCUMENTO')
    print('-' * 30)
    print('Digite o CPF (com ou sem pontos e traços: ')
    print('Exemplo: xxx.xxx.xxx-xx ou xxxxxxxxxxx')

    while True:
        try:
            entrada = input('Digite o CPF: ').strip()
            cpf_validado = validar_cpf(entrada)
            print(f'CPF Válido: {cpf_validado}')
            return cpf_validado
        except ValueError as e:
            print(f'Erro: {e}')
            print('Por favor, digite novamente.\n')

def extrair_numero_cpf(cpf_formatado: str) -> str:
    """
    Extrai apenas os números do CPF formatado.

    Args:
        cpf_formatado: CPF no formato 000.000.000-00

    Returns:
        str: Apenas com 11 dígitos numéricos

    """
    return limpar_cpf(cpf_formatado)

if __name__ == '__main__':
    print('TESTANDO VALIDAÇÃO...')
    print('-' * 60)

    #CPF's para teste (alguns válidos, outros inválidos)
    cpf_teste = [
        #Válidos (CPF de exemplos conhecidos):
        '123.456.789-09', #CPF de exemplo padrão
        '111.444.777-35', #CPF de exemplo
        '529.982.247-25', #CPF válido aleatório

        #Inválidos
        '123.456.789-00', #Dígitos Errados
        '111.111.111-11', #Todos os dígitos iguais
        '123', #Muito curto
        '123.456.789-0A', #com letra
        '', #vazio
        '123.456.789-0', #faltando dígito
        '000.000.000-00', #zeros
    ]

    print('\n1. TESTE DE VALIDAÇÃO DE CPF CONHECIDO: ')
    print('-' * 40)

    for cpf in cpf_teste:
        print(f'\nTestando: {cpf}')
        try:
            resultado = validar_cpf(cpf)
            print(f'VÁLIDO: {resultado}')
            print(f'Números: {extrair_numero_cpf(resultado)}')
        except ValueError as e:
            print(f'INVÁLIDO: {e}')

    #teste de formatação
    print('\n2. TESTE DE FORMATAÇÃO: ')
    print('-' * 40)

    cpfs_para_formatar = [
        '12345678909',
        '123.456.789-09',
        '123456789-09',
        '123.45678909'
    ]
    for cpf in cpfs_para_formatar:
        formatado = formatar_cpf(cpf)
        print(f"\n'{cpf}' - > '{formatado}'")

    #teste de geração de cpf válido
    print('\n\n3.GERANDO CPFS VÁLIDOS PARA TESTE: ')
    print('-' * 40)

    for i in range(3):
        cpf_gerado = gerar_cpf_valido()
        print(f'\nCPF gerado: {i+1}: {cpf_gerado}')

    #verifica se é realmente válido
    try:
        validar_cpf(cpf_gerado)
        print(f'Validação Confirmada')
    except ValueError as e:
        print(f'Erro: {e}')

#teste de interação
print('\n\n4. TESTE DE INTERAÇÃO COM USUARIO')
print('-' * 60)

# Descomente para testar interação
# cpf_usuario = obter_cpf_usuario()
# print(f"\n CPF obtido: {cpf_usuario}")
# print(f" Apenas números: {extrair_numero_cpf(cpf_usuario)}")

print('\nTESTE ESPECIAL - SEU CPF: ')
print('-' * 40)

#teste com um cpf específico (substitua pelo seu se quiser):
seu_cpf_teste = '125.464.607-81' #cpf pessoal de exemplo

print(f'TESTANDO CPF: {seu_cpf_teste}')
try:
    resultado = validar_cpf(seu_cpf_teste)
    print(f'CPF VÁLIDO: {resultado}')
except ValueError as e:
    print(f'ERRO: {e}')

