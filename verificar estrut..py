import os

print('ESTRUTURA DO PROJETO "FICHA CADASTRAL"')
print('='*50)

estrutura_esperada = {
    'models': ['__init__.py', 'pessoa.py'],
    'validacao': ['__init__.py', 'nome.py', 'idade.py', 'cpf.py', 'sexo.py'],
    'cadastro': ['__init__.py', 'interface.py'],
    'arquivos_raiz': ['main.py', 'requirements.txt', 'README.md']
}

tudo_ok = True

for pasta, arquivos in estrutura_esperada.items():
    if pasta != 'arquivos_raiz':
        caminho_pasta = os.path.join('.', pasta)
        
        if os.path.exists(caminho_pasta) and os.path.isdir(caminho_pasta):
            print(f'{pasta}/ - OK')

            for arquivo in arquivos:
                caminho_arquivo = os.path.join(caminho_pasta, arquivo)
                if os.path.exists(caminho_arquivo):
                    print(f'{arquivo}/ - OK')
                else:
                    print(f'{arquivo} - FALTANDO')
                    tudo_ok = False
    else:
        print(f'{pasta}/ - NO ARQUIVO FOUND')
        tudo_ok = False

print('\n' + '=' * 50)
if tudo_ok:
    print('ESTRUTURA COMPLETA! Pronto para codificar')
else:
    print('Alguns Arquivos faltando. Vamos criá-los!')

print('\nEstrutura Atual Completa: ')
print('=' * 30)
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('.')]

    nivel = root.count(os.sep)
    indent = ' ' * nivel
    print(f'{indent}{os.path.basename(root) or '.'}/')

    for file in files:
        if file.endswith('.py') or file in ['README.md', 'requirements.txt']:
            print(f'{indent} {file}')
