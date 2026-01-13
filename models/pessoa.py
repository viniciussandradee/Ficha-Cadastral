"""
Módulo Pessoa - Define a classe principal do sistema de ficha cadastral
Integra com validação inclusive de gênero
"""

from datetime import datetime, date
from typing import Optional, Dict, Any
from validacao.sexo import validar_sexo, formatar_sexo, obter_sexo_simplificado

class Pessoa:
    """Classe que representa uma pessoa no sistema"""

    def __init__(self, nome: str, cpf: str, ano_nascimento: int,
                 sexo: Optional[str] = None,
                 email: Optional[str] = None,
                 telefone: Optional[str] = None):

        self.nome = nome.strip()
        self.cpf = cpf
        self.ano_nascimento = ano_nascimento
        self.sexo_dados = validar_sexo(sexo)
        self.email = email.strip() if email else None
        self.telefone = telefone.strip() if telefone else None
        self.data_cadastro = datetime.now()

    @property
    def idade(self) -> int:
        """Calcula Idade Atual"""
        return datetime.now().year - self.ano_nascimento

    @property
    def cpf_formatado(self) -> str:
        """Formata CPF: 000.000.000-00"""
        cpf_limpo = ''.join(filter(str.isdigit, self.cpf))
        if len(cpf_limpo) != 11:
            return self.cpf
        return f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'

    @property
    def sexo(self) -> str:
        """Retorna o código simplificado do sexo/gênero (backward compatibility)"""
        return self.sexo_dados['valor']

    @property
    def sexo_display(self) -> str:
        """Retorna sexo/gênero formatado para exibição"""
        return self.sexo_dados['display']

    @property
    def sexo_categoria(self) -> str:
        """Retorna a categoria de gênero (binário, nao_binario, outro, nao_informado)"""
        return self.sexo_dados['categoria']

    @property
    def sexo_entrada_original(self) -> str:
        """Retorna a entrada original do usuário"""
        return self.sexo_dados['entrada_original']

    @property
    def sexo_formatado(self) -> str:
        """Formata a exibição do sexo (backward compatibility)"""
        return self.sexo_display

    def atualizar_sexo(self, nova_entrada: Optional[str]) -> None:
        """
        Atualiza o sexo/gênero de cada pessoa

        Args:
            nova_entrada: Nova entrada de sexo/gênero
        """
        self.sexo_dados = validar_sexo(nova_entrada)

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'nome': self.nome,
            'cpf': self.cpf,
            'cpf_formatado': self.cpf_formatado,
            'ano_nascimento': self.ano_nascimento,
            'idade': self.idade,
            'sexo': self.sexo,
            'sexo_dados':{
                'valor': self.sexo_dados['valor'],
                'display': self.sexo_dados['display'],
                'categoria': self.sexo_dados['categoria'],
                'entrada_original': self.sexo_dados['entrada_original'],
            },
            'email': self.email,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro.strftime('%d/%m/%Y %H:%M:%S'),
        }

    @classmethod
    def from_dict(cls, dados: Dict[str, Any]) -> 'Pessoa':
        """
        Cria uma Pessoa a partir de um dicionário

        Args:
            dados: Dicionário com os dados das pessoas

        Returns:
            Pessoa: Instância da Pessoa
        """
        #extrai entrada de sexo dos dados
        if 'sexo_dados' in dados:
            sexo_entrada = dados['sexo_dados'].get('entrada_original', dados['sexo_dados']['display'])
        else:
            #backward compatibility
            sexo_entrada = dados.get('sexo')

        pessoa = cls(
            nome = dados['nome'],
            cpf = dados['cpf'],
            ano_nascimento = dados['ano_nascimento'],
            sexo = sexo_entrada,
            email = dados.get('email'),
            telefone = dados.get('telefone')
        )
        #Restaura dados do Cadastro se existir
        if 'data_cadastro' in dados:
            pessoa.data_cadastro = datetime.strptime(dados['data_cadastro'], '%d/%m/%Y %H:%M:%S')
        return pessoa

    def __str__(self) -> str:
        """Exibição bonita para o usuario"""
        linha = '=' * 50

        # Adiciona emoji baseado na categoria
        emoji_map = {
            'binario': '👤',
            'nao_binario': '🦋',
            'outro': '🌈',
            'nao_informado': '🙈'
        }
        emoji = emoji_map.get(self.sexo_categoria, '👤')

        dados = [
            linha,
            "FICHA CADASTRAL",
            linha,
            f'Nome: {self.nome}',
            f'CPF: {self.cpf_formatado}',
            f'Idade: {self.idade} anos (nascido em {self.ano_nascimento})',
            f'Sexo/Gênero: {emoji} {self.sexo_display}'
        ]

        if self.sexo_categoria != 'nao_informado' and self.sexo_entrada_original != self.sexo_display:
            dados.append(f'  (Entrada Original: "{self.sexo_entrada_original}")')

        if self.email:
            dados.append(f'Email: {self.email}')
        if self.telefone:
            dados.append(f'Telefone: {self.telefone}')

        dados.append(f'Cadastro em: {self.data_cadastro.strftime("%d/%m/%Y %H:%M")}')
        dados.append(linha)

        return '\n'.join(dados)

class CadastroPessoas:
    """Gerencia o cadastro de múltiplas pessoas"""

    def __init__(self):
        """Inicializa um cadastro vazio"""
        self.pessoas = []

    def adicionar(self, pessoa: Pessoa) -> None:
        """Adiciona uma pessoa ao cadastro"""
        self.pessoas.append(pessoa)

    def remover_por_cpf(self, cpf: str) -> bool:
        """
        Remove uma pessoa pelo CPF

        Args:
            cpf: CPF da pessoa a remover

        Returns:
            bool: True se removeu, False se não encontrou

        """
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        for i, pessoa in enumerate(self.pessoas):
            pessoa_cpf_limpo = ''.join(filter(str.isdigit, pessoa.cpf))
            if pessoa_cpf_limpo == cpf_limpo:
                del self.pessoas[i]
                return True
        return False
    def buscar_por_cpf(self, cpf:str) -> Optional[Pessoa]:
        """Busca uma pessoa pelo CPF"""
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        for pessoa in self.pessoas:
            pessoa_cpf_limpo = ''.join(filter(str.isdigit, pessoa.cpf))
            if pessoa_cpf_limpo == cpf_limpo:
                return pessoa
        return None

    def buscar_por_nome(self, nome: str) -> list[Pessoa]:
        """Busca por pessoas por nome (case-insensitive, parcial)"""
        nome_lower = nome.lower()
        return [p for p in self.pessoas if nome_lower in p.nome.lower()]

    def filtrar_por_sexo(self, codigo_sexo: str) -> list[Pessoa]:
        """Filtrar pessoas por código do sexo"""
        return [p for p in self.pessoas if p.sexo == codigo_sexo]

    def estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas do cadastro"""
        total = len(self.pessoas)

        if total == 0:
            return {
                'total_pessoas': 0,
                'media_idade': 0,
                'distribuicao_sexo': {},
                'pessoas_com_email': 0,
                'pessoas_com_telefone': 0
            }

        #Contagem por sexo/gênero
        distribuicao = {}
        for pessoa in self.pessoas:
            codigo = pessoa.sexo
            distribuicao[codigo] = distribuicao.get(codigo, 0) + 1

        #Media de Idade
        media_idade = sum(p.idade for p in self.pessoas) / total

        return {
            'total_pessoas': total,
            'media_idade': round(media_idade, 1),
            'distribuicao_sexo': distribuicao,
            'pessoas_com_email': sum(1 for p in self.pessoas if p.email),
            'pessoas_com_telefone': sum(1 for p in self.pessoas if p.telefone)
        }
    def listar_todos(self) -> str:
        """Lista todas as pessoas do cadastro"""
        if not self.pessoas:
            return 'Cadastro Vazio'

        resultado = []

        for i, pessoa in enumerate(self.pessoas, 1):
            resultado.append(f'\n{i}. {pessoa.nome} - CPF: {pessoa.cpf_formatado} - {pessoa.sexo_display}')
        return '\n'.join(resultado)

    def __len__(self) -> int:
        """Retorna o número de pessoas no cadastro"""
        return len(self.pessoas)

    def __str__(self) -> str:
        """Representação do cadastro"""
        estat = self.estatisticas()

        if estat['total_pessoas'] == 0:
            return 'Cadastro Vazio'

        resultado = [
            f"Cadastro de Pessoas",
            '-' * 40,
            f"Total de pessoas: {estat['total_pessoas']}",
            f"Média de Idade: {estat['media_idade']} anos",
            f"Pessoas com email: {estat['pessoas_com_email']}",
            f"Pessoas com telefone: {estat['pessoas_com_telefone']}",
            "\nDistribuição por sexo/gênero: "
        ]
        for codigo, quantidade in estat['distribuicao_sexo'].items():
            #Pega exemplo para mostrar display
            exemplo = next((p for p in self.pessoas if p.sexo == codigo), None)
            display = exemplo.sexo_display if exemplo else codigo
            resultado.append(f" {display}: {quantidade}")

        return "\n".join(resultado)

#Função para criar pessoas interativamente:
def criar_pessoa_interativo() -> Pessoa:
    """Cria uma pessao interativamente via terminal

    Returns:
        Pessoa: Pessoa criada

    """
    from validacao.sexo import obter_sexo_usuario

    print('\n' + '-' * 50)
    print('CADASTRO DE NOVA PESSOA')
    print('-' * 50)

    #Nome
    while True:
        nome = input('\nDigite o nome Completo: ').strip()
        if nome:
            break
        print('Nome é obrigatório')

    #CPF
    while True:
        cpf = input('Digite seu cpf: ').strip()
        cpf_limpo = ''.join(filter(str.isdigit, cpf))
        if len(cpf_limpo) == 11:
            break
        print('CPF deve conter 11 dígitos')

    #Ano de Nascimento
    while True:
        try:
            ano_str = input('Digite o ano de nascimento [AAAA]: ').strip()
            ano = int(ano_str)
            if 1900 <= ano <= datetime.now().year:
                break
            print(f"Ano deve estar entre 1900 e {datetime.now().year}")
        except ValueError:
            print('Digite um ano válido!')

    #Sexo/Gênero
    print('\n' + '-' * 40)
    resultado_sexo = obter_sexo_usuario()

    #Email (opcional)
    email = input('\nEmail (opcional, pressione Enter para pular): ').strip()
    if not email:
        email = None

    #Telefone
    telefone = input('\nDigite o telefone (opcional): ').strip()
    if not telefone:
        telefone = None

    #Cria Pessoa
    pessoa = Pessoa(
        nome = nome,
        cpf = cpf,
        ano_nascimento = ano,
        sexo = resultado_sexo['entrada_original'],
        email = email,
        telefone = telefone
    )

    print('\n' + '-' * 50)
    print('PESSOA CADASTRADA COM SUCESSO')
    print('-' * 50)

    return pessoa

if __name__ == '__main__':
    print('TESTANDO A CLASSE PESSOA ATUALIZADA...')
    print('-' * 60)

    #1. Teste básico (backward compatibility)
    print('\n1. Teste Básico (Masculino): ')
    pessoa1 = Pessoa(
        nome = 'Vinicius Barcellos de Andrade',
        cpf = '12546460781',
        ano_nascimento = 1988,
        sexo = 'M',
        email = 'viniciuss.barcelloss@gmail.com'
    )
    print(pessoa1)

    #2. Teste com gênero Não-Binário
    print('\n\n2. Teste com Não-Binário: ')
    pessoa2 = Pessoa(
        nome = 'Manuela Monteiro',
        cpf = '98765432100',
        ano_nascimento = 1995,
        sexo = 'Não-Binário',
        telefone = '(11) 98765-4321'
    )
    print(pessoa2)

    #3. Teste com genero personalizado
    print('\n\n3. Teste Gênero Personalizado: ')
    pessoa3 = Pessoa(
        nome = 'Taylor Lisa',
        cpf = '11122233344',
        ano_nascimento = 2000,
        sexo = 'Agênero',
        email = 'taylor@email.com'
    )
    print(pessoa3)

    #4. Teste sem informar Sexo
    print("\n\n4. TESTE SEM INFORMAR SEXO:")
    pessoa4 = Pessoa(
        nome='Patricia Silva',
        cpf='55566677788',
        ano_nascimento=1985
    )
    print(pessoa4)

    #5. Teste Cadastro de Pessoas
    print("\n\n5. TESTE DE CADASTRO:")
    cadastro = CadastroPessoas()
    cadastro.adicionar(pessoa1)
    cadastro.adicionar(pessoa2)
    cadastro.adicionar(pessoa3)
    cadastro.adicionar(pessoa4)

    print(cadastro)

    #6. Teste Estatísticas
    print('\n\n6. Estatísticas Detalhadas: ')
    estat = cadastro.estatisticas()
    for chave, valor in estat.items():
        if chave == 'distribuicao_sexo':
            print(f'{chave}:')
            for codigo, quantidade in valor.items():
                print(f'  {codigo}: {quantidade}')
        else:
            print(f'{chave}: {valor}')
    #7. Teste Listagem
    print('\n\n7. LISTAGEM DE TODAS AS PESSOAS: ')
    print(cadastro.listar_todos())

    #8. Teste Busca
    print('\n\n8. TESTE DE BUSCA POR CPF: ')
    encontrada = cadastro.buscar_por_cpf('12546460781')
    if encontrada:
        print(f'Encontrada: {encontrada.nome}')
    else:
        print('Não encontrada')

    #9. Teste Atualização de Sexo
    print('\n\n9. TESTE DE ATUALIZAÇÃO DE SEXO: ')
    print(f'ANTES: {pessoa1.sexo_display}')
    pessoa1.atualizar_sexo('X')
    print(f'DEPOIS: {pessoa1.sexo_display}')

    #10. Teste de Conversão para/from dicionário
    print('\n\n10. TESTE DE SERIALIZAÇÃO: ')
    dados = pessoa2.to_dict()
    print('Dados serializados: ')
    for chave, valor in dados.items():
        if chave == 'sexo_dados':
            print(f'{chave}: ')
            for subchave, subvalor in valor.items():
                print(f'     {subchave}: {subvalor}')
        else:
            print(f'{chave}: {valor}')

    pessoa_reconstruida = Pessoa.from_dict(dados)
    print('\nPessoa Reconstruída: ')
    print(pessoa_reconstruida)

    #11. Teste Interativo (descomente para testar)
    # print("\n\n11. TESTE INTERATIVO: ")
    # pessoa_interativa = criar_pessoa_interativo()

    print('\n' + '=' * 60)
    print('TESTES CONCLUÍDOS COM SUCESSO!')
