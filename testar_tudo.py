print('TESTE COMPLETO DO SISTEMA FICHA CADASTRAL')
print('=' * 60)

import os
print('\n1. VERIFICANDO ESTRUTURA DE PASTAS...')
estrutura_minima = [
    ('models', ['__init__.py', 'pessoa.py']),
    ('validacao', ['__init__.py', 'nome.py', 'idade.py', 'cpf.py', 'sexo.py']),
    ('cadastro', ['__init__.py', 'interface.py']),
]

tudo_ok = True
for pasta, arquivos in estrutura_minima:
    caminho = f'./{pasta}'
    if os.path.exists(caminho) and os.path.isdir(caminho):
        print(f'{pasta} - OK')
        for arquivo in arquivos:
            if os.path.exists(f'{caminho}/{arquivo}'):
                print(f'{arquivo} - OK')
            else:
                print(f'{arquivo} - ERRO')
                tudo_ok = False

    else:
        print(f'{pasta} - AUSENTE')
        tudo_ok = False

print('\n2. TESTANDO IMPORTAÇÃO DA CLASSE PESSOA...')
try:
    from models.pessoa import Pessoa
    print('CLASSE IMPORTADA COM SUCESSO')

    print('\n.3 CRIANDO UMA PESSOA DE TESTE...')
    try:
        pessoa_teste = Pessoa(
            nome = 'Vinicius Barcellos de Andrade',
            cpf = '12546460781',
            ano_nascimento = '1988',
            sexo = 'M',
            email = 'viniciuss.barcelloss@gmail.com',
            telefone = '27988664060'
        )
        print('PESSOA CRIADA COM SUCESSO')

        print('\n4. DADOS DA PESSOA: ')
        print(' ' + '-' * 40)
        print(f'Nome: {pessoa_teste.nome}')
        print(f'CPF: {pessoa_teste.cpf_formatado}')
        print(f'Idade: {pessoa_teste.idade} anos')
        print(f'Sexo: {pessoa_teste.sexo_formatado}')
        print(f'Email: {pessoa_teste.email or 'Não Informado'}')
        print(f'Telefone: {pessoa_teste.telefone or 'Não Informado'}')

        print('\n5. CONVERTENDO PARA DICIONÁRIO...')
        dados = pessoa_teste.to_dict()
        print(f' CONVERTIDO! Tem {len(dados)} campos')

        print('\n6. TESTANDO EXIBIÇÃO COMPLETA: ')
        print(' ' + '-' * 40)
        print(pessoa_teste)

    except Exception as e:
        print(f' Erro ao criar pessoa: {e}')
        print(f' Tipo de Erro: {type(e).__name__}')

except ImportError as e:
    print(f' Erro de Importação: {e}')
    print('\n SOLUÇÃO: Certifique-se de que: ')
    print(' 1. models/pessoa.py existe')
    print(' 2. models/__init__.py existe (pode ser vazio)')
    print(' 3. Você está na pasta raiz do projeto')
    tudo_ok = False

print('\n' + '-' * 60)
if tudo_ok:
    print(f'Parabéns! Sistema básico está funcionando')
    print('Próximo passo: Criar módulos de validação')
else:
    print('Alguns problemas encontrados')
    print('Vamos corrigir antes de continuar')

print('\n COMANDOS PARA CONTINUAR: ')
print(' 1. python3 validacao/sexo.py - Para criar validação de sexo')
print(' 2. python3 validacao/nome.py - Para criar validação de nome')
print(' 3. python3 main.py           - Quando tiver tudo pronto')

