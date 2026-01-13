#!/usr/bin/env python3

"""
SISTEMA DE FICHA CADASTRAL - Versão 1.0
==========================================
Sistema completo de cadastro de pessoas com validação inclusiva de gênero,
para inclusão como portóflio para o Github.

Autor: Vinicius Barcellos de Andrade
Data: 12.01.2026 (01.12.26 -- english data version)
GitHub: https://github.com/viniciussandradee

"""

import sys
import os
import time
if 'TERM' not in os.environ:
    os.environ['TERM'] = 'xterm-256color'
from datetime import datetime
from typing import List, Optional

# Adiciona o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.pessoa import Pessoa, CadastroPessoas, criar_pessoa_interativo
from validacao.sexo import ValidadorGenero, formatar_sexo

class SistemaCadastro:
    """Classe principal do sistema de Ficha Cadastral"""

    def __init__(self):
        """Inicializa o sistema"""
        self.cadastro = CadastroPessoas()
        self.carregar_dados()

    def carregar_dados(self):
        """Carrega dados de exemplo para demonstração"""
        try:
            #Dados de exemplo para portfólio
            pessoas_exemplo = [
                Pessoa(
                    nome = "Vinicius Barcellos de Andrade",
                    cpf = '12546460781',
                    ano_nascimento = 1988,
                    sexo = "Masculino",
                    email = 'viniciuss.barcelloss@gmailcom',
                    telefone = '(27) 98866-4060'
                ),
                Pessoa(
                    nome = "Livia Vidoto Monteiro Gomes",
                    cpf = '98765432100',
                    ano_nascimento = 1985,
                    sexo = 'F',
                    email = 'liviavmg@gmail.com',
                    telefone = '(21) 99876-5432'
                ),
                Pessoa(
                    nome = 'Taylor Oliveira',
                    cpf = '45678912345',
                    ano_nascimento = 1995,
                    sexo = 'Não Binário',
                    email = 'taylor.oliveira@email.com'
                ),
                Pessoa(
                    nome = "Deide Costas",
                    cpf = '78912345678',
                    ano_nascimento = 2002,
                    sexo = 'Outro',
                    telefone = '(31) 91234-5678'
                )
            ]

            for pessoa in pessoas_exemplo:
                self.cadastro.adicionar(pessoa)

            print('[OK] Dados de exemplo carregados para demonstração')

        except Exception as e:
            print(f'[AVISO] Não foi possível carregar dados de exemplo: {e}')

    def exibir_logo(self):
        """Exibe logo do sistema"""
        print('\n' + '-' * 60)
        time.sleep(0.2)
        print('        SISTEMA DE FICHA CADASTRAL - v.1.0')
        time.sleep(0.2)
        print('\n' + '-' * 60)
        time.sleep(0.2)
        print('        Cadastro Inclusivo de Pessoas')
        time.sleep(0.2)
        print('\n' + '-' * 60)
        time.sleep(0.2)

    def exibir_menu_principal(self):
        """Exibe o menu principal"""
        print('\n' + '-' * 50)
        print('MENU PRINCIPAL')
        print('\n' + '-' * 60)
        print('1. [NOVO] Cadastrar Nova Pessoa')
        print('2. [LISTA] Listar todas as Pessoas')
        print('3. [BUSCA] Buscar pessoas por CPF')
        print('4. [BUSCA] Buscar pessoas por Nome')
        print('5. [STATS] Ver Estatísticas do Cadastro')
        print('6. [INFO] Opções de Gêneros Disponíveis')
        print('7. [EXPORTAR] Exportar Dados')
        print('8. [AJUDA] Ajuda /Sobre o Sistema')
        print('0. [SAIR] Sair do Sistema')
        print('\n' + '-' * 60)

    def cadastrar_pessoa(self):
        """Cadastra uma nova pessoa"""
        print('\n' + '-' * 50)
        time.sleep(0.3)
        print('NOVO CADASTRO')
        time.sleep(0.3)
        print('-' * 50)
        time.sleep(0.3)

        try:
            pessoa = criar_pessoa_interativo()
            self.cadastro.adicionar(pessoa)

            print('\n[SUCESSO] CADASTRO REALIZADO COM SUCESSO!')
            time.sleep(0.5)
            print('-' * 50)

        except KeyboardInterrupt:
            print('\n\n[INTERROMPIDO] Cadastro cancelado pelo usuário')
        except Exception as e:
            print(f'\n[ERRO] Erro ao cadastrar: {e}')

    def listar_pessoas(self):
        """Lista todas as pessoas cadastradas"""
        print('\n' + '-' * 50)
        print('LISTA DE PESSOAS CADASTRADAS')
        print(f'Total: {len(self.cadastro)} pessoa(s)')
        print('-' * 50)

        if len(self.cadastro) == 0:
            print('[VAZIO] Nenhuma pessoa cadastrada ainda')
            return

        #Lista resumida
        print(self.cadastro.listar_todos())

        #Quer ver detalhes?
        ver_detalhes = input('\nVer detalhes de alguma pessoa? [S/N]: ').lower()
        if ver_detalhes == 's':
            try:
                #Pede o número que o usuario viu na lista (1, 2, 3, ...)
                total = len(self.cadastro.pessoas)
                numero_str = input(f'Digite o número da pessoa (Entre 1 - {total}): ')
                numero = int(numero_str)

                #Valida se está no intervalo correto
                if numero < 1 or numero > total:
                    print(f'[ERRO] O número deve estar entre 1 e {total}!')
                    return

                #Converte para indice Python (0, 1, 2, ...)
                indice = numero - 1

                #Mostra todos os detalhes
                print('\n' + '-' * 50)
                print(self.cadastro.pessoas[indice])

            except ValueError:
                print('[ERRO] Por favor, digite um número válido!')
            except Exception as e:
                print(f'[ERRO] Erro ao mostrar detalhes: {e}')

    def buscar_por_cpf(self):
        """Busca uma pessoa pelo CPF"""
        print('\n' + '-' * 50)
        print('BUSCAR POR CPF')
        print('-' * 50)

        cpf = input('Digite o CPF (com ou sem traço e hífen): ').strip()

        if not cpf:
            print('[ERRO] CPF não pode ser vazio!')
            return

        pessoa = self.cadastro.buscar_por_cpf(cpf)

        if pessoa:
            print('\n[ENCONTRADO] PESSOA ENCONTRADA: ')
            print('-' * 50)
            print(pessoa)
        else:
            print(f'\n[NÃO ENCONTRADO] Nenhuma pessoa encontrada com o CPF: {cpf}')

    def buscar_por_nome(self):
        """Busca pessoas por nome"""
        print('\n' + '-' * 50)
        print('BUSCAR POR NOME')
        print('-' * 50)

        nome = input('Digite o nome (ou parte dele): ').strip()

        if not nome:
            print('[ERRO] Nome não pode ser vazio!')
            return

        resultados = self.cadastro.buscar_por_nome(nome)

        if resultados:
            print(f'\n[ENCONTRADO] Encontradas {len(resultados)} pessoa(s): ')
            print('-' * 50)
            for i, pessoa in enumerate(resultados, 1):
                print(f'\n{i}. {pessoa.nome} - CPF: {pessoa.cpf_formatado} - {pessoa.sexo_display}')

            ver_detalhes = input('\nVer detalhes de alguma pessoa? [S/N]: ').lower()
            if ver_detalhes == 's':
                try:
                    total_resultados = len(resultados)
                    numero = int(input(f'Digite o número da pessoa (Entre 1 - {total_resultados}): '))

                    if 1 <= numero <= total_resultados:
                        indice = numero - 1
                        print('\n' + '-' * 50)
                        print(resultados[indice])
                    else:
                        print(f'[ERRO] O número deve estar entre 1 e {total_resultados}!')

                except ValueError:
                    print('[ERRO] Por favor, digite um número válido')

    def mostrar_estatisticas(self):
        """Mostra Estatísticas do Cadastro"""
        print('\n' + '-' * 50)
        print('ESTATÍSTICAS DO CADASTRO')
        print('-' * 50)

        estatisticas = self.cadastro.estatisticas()

        print(f'Total de Pessoas: {estatisticas["total_pessoas"]}')
        print(f'Media de Idade: {estatisticas["media_idade"]} anos')
        print(f'Pessoas com Email: {estatisticas["pessoas_com_email"]}')
        print(f'Pessoas com Telefone: {estatisticas["pessoas_com_telefone"]}')

        print('\nDistribuição por Gênero')
        print('-' * 30)

        distribuicao = estatisticas['distribuicao_sexo']
        if distribuicao:
            for codigo, quantidade in distribuicao.items():
                exemplo = next((p for p in self.cadastro.pessoas if p.sexo == codigo), None)
                if exemplo:
                    display = exemplo.sexo_display
                else:
                    display = formatar_sexo(codigo)
                print(f'* {display}: {quantidade} pessoa(s)')
        else:
            print('[VAZIO] Nenhum dado disponível')

    def mostrar_opcoes_genero(self):
        """Mostrar as opções de gênero disponíveis"""
        print('\n' + '-' * 50)
        print('OPÇÕES DE GÊNERO DISPONÍVEIS')
        print('-' * 50)

        opcoes = ValidadorGenero.obter_opcoes_validas()

        print('Códigos Principais [aceito pelo sistema]: ')
        print('-' * 40)
        for codigo, display in opcoes.items():
            print(f'* {codigo} -> {display}')

        print('\nVocê também pode digitar por extenso: ')
        print('-' * 40)
        print("* Masculino, Feminino, Homem, Mulher")
        print("* Nao Binario, Nao-Binario, NB")
        print("* Outro, Outros")
        print("* Não Especificado, X")
        print("* Em branco -> Prefiro não informar")
        print("\nAceitamos tambem em Ingles:")
        print("* Male, Female, Other, NonBinary")
        print("\nO sistema é inteligente e aceita variações!")

    def exportar_dados(self):
        """Exporta dados para o arquivo de texto"""
        print('\n' + '-' * 50)
        print('EXPORTAR DADOS')
        print('-' * 50)

        if len(self.cadastro) == 0:
            print('[ERRO] Nenhum dado para exportar')
            return

        timestamp = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        nome_arquivo = f'Cadastro_pessoas_{timestamp}.txt'

        try:
            with open(nome_arquivo, 'w', encoding = 'utf-8') as arquivo:
                arquivo.write('-' * 60 + '\n')
                arquivo.write('EXPORTAÇÃO DO SISTEMA DE FICHA CADASTRAL\n')
                arquivo.write(f'Data: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
                arquivo.write(f'Total de Pessoas: {len(self.cadastro)}\n')
                arquivo.write('-' * 60 + '\n\n')

                for i, pessoa in enumerate(self.cadastro.pessoas, 1):
                    arquivo.write(str(pessoa))
                    arquivo.write('\n\n')

                #Estatisticas
                estat = self.cadastro.estatisticas()
                arquivo.write('-' * 60 + '\n')
                arquivo.write('ESTATÍSTICAS DO CADASTRO\n')
                arquivo.write('-' * 60 + '\n')
                arquivo.write(f'Total: {estat["total_pessoas"]} pessoas\n')
                arquivo.write(f'Media de Idade: {estat["media_idade"]} anos\n')
                arquivo.write(f'Pessoas com Email: {estat["pessoas_com_email"]}\n')
                arquivo.write(f'Pessoas com Telefone: {estat["pessoas_com_telefone"]}\n')

                if estat['distribuicao_sexo']:
                    arquivo.write("\nDistribuição Por Gênero:\n")
                    for codigo, quantidade in estat['distribuicao_sexo'].items():
                        exemplo = next((p for p in self.cadastro.pessoas if p.sexo == codigo), None)
                        display = exemplo.sexo_display if exemplo else codigo
                        arquivo.write(f'   {display}: {quantidade}\n')

            print(f'[SUCESSO] Dados exportados com sucesso para: {nome_arquivo}')
            print(f'[ARQUIVO] Local: {os.path.abspath(nome_arquivo)}')

        except Exception as e:
            print(f'[ERRO] Erro ao exportar dados: {e}')

    def mostrar_ajuda(self):
        """Mostra tela de ajuda e informações do sistema"""
        print('\n' + '-' * 50)
        print('SOBRE O SISTEMA')
        print('-' * 50)

        sobre = """
        SISTEMA FICHA CADASTRAL - Versão 1.0
        
        DESCRIÇÃO:
        Sistema completo para cadastro de pessoas com validação inclusiva de gênero. Desenvolvido 
        como projeto de portfólio, com auxílio de IA - instrução e construção em níveis mais avançados.
        
        CARACTERÍSTICAS:
        * Cadastro completo de pessoas (Nome, CPF, Idade, etc...)
        * Validação Inclusiva de gênero com múltiplas opções
        * Busca por CPF e Nome
        * Estatísticas detalhadas
        * Exportação de Dados
        * Interface amigável
        
        VALIDAÇÃO INCLUSIVA:
        O sistema aceita diversas formas de identificar gênero:
        * Códigos: M, F, NB, O, X
        * Português: Masculino, Feminino, Não Binário, Outro
        * Inglês: Male, Female, Other and NonBinary
        
        TECNOLOGIAS:
        * Python 3.X
        * Programação Orientada a Objetos
        * Tipagem Estatística (Type Hints)
        * Módulos separados por responsabilidade
        
        AUTOR:
        Vinicius Barcellos de Andrade
        Github: https://github.com/viniciussandradee
        
        LICENÇA:
        Este projeto é open-source. Sinta-se livre para usar e modificar!
        
        REPOSITÓRIO:
        https://github.com/viniciussandradee?tab=repositories
        """

        print(sobre)

        print('\n' + '-' * 50)
        print('COMANDOS DO SISTEMA')
        print('-' * 50)

        comandos = """
        Durante o cadastro:
        * Pressione Ctrl + C para cancelar qualquer operação
        * Deixe campos opcionais em branco pressionando ENTER
        * Para gênero, você pode digitar códigos ou por extenso
        
        No Menu Principal:
        * Digite o número da opção desejada
        * Use ENTER para confirmar
        * A qualquer momento, pode voltar ao menu principal
        
        Dicas:
        * O CPF é automaticamente formatado
        * A IDADE é calculada automaticamente
        * Os dados são mantidos em memória durante a sessão
              
        """

        print(comandos)

    def sair_sistema(self):
        """Encerra o Sistema"""
        print('\n' + '-' * 50)
        print('SAINDO DO SISTEMA')
        print('-' * 50)

        if len(self.cadastro) > 0:
            print('Resumo da Sessão: ')
            print(f'  * Pessoas cadastradas: {len(self.cadastro)}')

            estat = self.cadastro.estatisticas()
            print(f'   * Media de Idade: {estat["media_idade"]} anos')

            exportar = input('\nDeseja exportar os dados antes de sair? [S/N]: ').lower()
            if exportar == 's':
                self.exportar_dados()

        print('\nObrigado por utilizar o Sistema de Ficha Cadastral')
        print('Até a próxima!\n')

    def executar(self):
        """Metódo Principal que executa o sistema"""
        try:
            #Limpa a tela (funciona em Windows, Linux e Mac)
            os.system('cls' if os.name == 'nt' else 'clear')

            #Exibe Logo:
            self.exibir_logo()

            #Loop Principal:
            while True:
                self.exibir_menu_principal()

                try:
                    opcao = input('\nEscolha uma opção [0 - 8]: ').strip()
                    if opcao == '0':
                        self.sair_sistema()
                        break
                    elif opcao == '1':
                        self.cadastrar_pessoa()
                    elif opcao == '2':
                        self.listar_pessoas()
                    elif opcao == '3':
                        self.buscar_por_cpf()
                    elif opcao == '4':
                        self.buscar_por_nome()
                    elif opcao == '5':
                        self.mostrar_estatisticas()
                    elif opcao == '6':
                        self.mostrar_opcoes_genero()
                    elif opcao == '7':
                        self.exportar_dados()
                    elif opcao == '8':
                        self.mostrar_ajuda()
                    else:
                        print('[ERRO] Opção Inválida! Por favor, digite um número de 0 a 8: ')

                    if opcao not in ["0", "8"]:
                        time.sleep(0.5)
                        input('Pressione ENTER para continuar...')

                except KeyboardInterrupt:
                    print('\n\n[INTERROMPIDO] Voltando ao menu...')
                    time.sleep(0.5)
                    continue
                except Exception as e:
                    print(f'\n[ERRO] Erro inesperado: {e}')
                    time.sleep(1)
                    input('\nPressione ENTER para continuar...')

        except KeyboardInterrupt:
            print('\n\nSistema encerrado pelo usuário. Até mais!')
        except Exception as e:
            print(f'\n[ERRO CRÍTICO] Erro no sistema: {e} ')
            print(f'Por favor, reinicie o sistema.')
            time.sleep(2)

def main():
    """Função Principal de Inicialização"""
    print('Inicializando o Sistema de Ficha Cadastral...')

    try:
        sistema = SistemaCadastro()
        sistema.executar()
    except Exception as e:
        print(f'[FALHA] Falha ao iniciar o sistema: {e}')
        print('Verifique se todos os módulos estão corretamente instalados')
        sys.exit(1)

if __name__ == '__main__':
    main()





