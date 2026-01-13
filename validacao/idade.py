"""
Validação de idade e ano de nascimento para o sistema de ficha cadastral
"""

from datetime import datetime
from typing import Tuple

def validar_ano_nascimento(ano: str) -> int:
    """
    Valida um ano de nascimento.

    Regras:
    1. Deve ser um número
    2. Entre 1900 e ano atual
    3. A pessoa deve ter, pelo menos, 0 anos (permite recém-nascidos)

    Args:
        ano: Ano como string

    Returns:
        int: Ano validado como número

    Raises:
        ValueError: se o ano for inválido

    """
    if not ano:
        raise ValueError('Ano de nascimento não pode ser vazio')

    ano = ano.strip()

    if not ano.isdigit():
        raise ValueError('Ano deve conter apenas números')

    ano_int = int(ano)
    ano_atual = datetime.now().year

    if ano_int < 1900:
        raise ValueError('Ano não pode ser anterior a 1900')
    if ano_int > ano_atual:
        raise ValueError(f'Ano não pode ser no futuro (máximo: {ano_atual}')

    return ano_int

def calcular_idade(ano_nascimento: int) -> int:
    """
    Calcula idade com base no ano de nascimento

    Args:
         ano_nascimento: Ano de nascimento válido

    Returns:
        int: idade em anos completos

    """
    return datetime.now().year - ano_nascimento

def validar_idade_minima(idade: int, idade_minima: int = 0) -> bool:
    """
    Verifica se a idade atende a um mínimo

    Args:
        idade: Idade calculada
        idade_minima: Idade mínima requerida (padrão = 0)

    Returns:
        bool: True se idade >= idade_minima

    Raises:
        ValueError: Se idade for menor que o mínimo

    """
    if idade < idade_minima:
        raise ValueError(
            f'Idade mínima requerida: {idade_minima} anos.'
            f'\nIdade Informada: {idade} anos'
        )
    return True

def obter_idade_usuario(idade_minima: int = 0) -> Tuple[int, int]:
    """
    Interage com usuario para obter ano de nascimento válido

    Args:
        idade_minima: Idade mínima requerida (padrão = 0)

    Returns:
        tuple: (ano_nascimento, idade)

    """

    print('\nINFORMAÇÕES DE NASCIMENTO')
    print('-' * 30)
    print(f'Idade mínima requerida: {idade_minima} anos')

    while True:
        try:
            entrada = input('Ano de nascimento [4 dígitos]: ').strip()
            ano_nascimento = validar_ano_nascimento(entrada)
            idade = calcular_idade(ano_nascimento)
            validar_idade_minima(idade, idade_minima)

            print(f'Idade Calculada: {idade} anos')
            return ano_nascimento, idade
        except ValueError as e:
            print(f'{e}')
            print('Por favor, digite nomante.\n')

def formatar_idade(idade: int) -> str:
    """
    Formata idade para exibição amigável

    Args:
        idade: Idade em anos

    Returns:
        str: Idade formatada

    """
    if idade == 0:
        return 'Recém-Nascido(a)'
    elif idade == 1:
        return '1 ano'
    else:
       return f'{idade} anos'

if __name__ == '__main__':
    print('TESTANDO VALIDAÇÃO IDADE')
    print('-' * 50)
    
    print('\nTESTE DE VALIDAÇÃO DE ANOS')
    print('-' * 30)

    testes_ano = ['1990', '2025', 'abc', '1850', '', '2005', '1988']

    for teste in testes_ano:
        print(f'\nTestando: "{teste}"')
        try:
            resultado = validar_ano_nascimento(teste)
            idade = calcular_idade(resultado)
            print(f'Ano válido: {resultado}')
            print(f'Idade: {formatar_idade(idade)}')
        except ValueError as e:
            print(f'Inválido: {e}')
    print('\n\n2.TESTE DE IDADE MÍNIMA (18 ANOS): ')
    print('-' * 30)

    testes_idade = [2008, 2000, 1990, 2010, 1988]

    for ano in testes_idade:
        idade = calcular_idade(ano)
        print(f'\nAno {ano} -> Idade: {idade} anos')
        try:
            validar_idade_minima(idade,18)
            print(f'APROVADO (maior de 18)')
        except ValueError as e:
            print(f'{e}')

    print('\n\n3. TESTE DE INTERAÇÃO (Idade Mínima = 16 anos): ')
    print('-' * 50)

    # Descomente para testar interação
    # ano, idade = obter_idade_usuario(idade_minima=16)
    # print(f"\n Resultado: ")
    # print(f"   Ano nascimento: {ano}")
    # print(f"   Idade: {idade} anos ({formatar_idade(idade)})")

    print(f'\nTESTE ESPECIAL - SEU CADASTRO: ')
    print('-' * 30)

    seu_ano = 1988
    sua_idade = calcular_idade(seu_ano)

    print(f'Ano: {seu_ano}')
    print(f'Idade: {sua_idade} anos')
    print(f'Formatado: {formatar_idade(sua_idade)}')

    try:
        validar_ano_nascimento(str(seu_ano))
        print('Ano Válido')

        validar_idade_minima(sua_idade, 18)
        print('Maior de Idade')

        validar_idade_minima(sua_idade, 30)
        print('Maior de 30 anos')
    except ValueError as e:
        print(f'{e}')
