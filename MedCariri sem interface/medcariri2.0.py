import datetime
import json
import os

postos = {}
medicos = {}
agendamentos = []

# ------------------------------
# FUNÇÕES DE PERSISTÊNCIA
# ------------------------------
def salvar_dados():
    dados = {
        "postos": postos,
        "medicos": medicos,
        "agendamentos": agendamentos
    }
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print("Dados salvos com sucesso!\n")

def carregar_dados():
    global postos, medicos, agendamentos
    if os.path.exists("dados.json"):
        try:
            with open("dados.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
            postos = {int(k): v for k, v in dados.get("postos", {}).items()}
            medicos = {int(k): v for k, v in dados.get("medicos", {}).items()}
            agendamentos = dados.get("agendamentos", [])
            print("Dados carregados com sucesso!\n")
        except json.JSONDecodeError:
            print("Erro ao carregar dados. Arquivo pode estar corrompido.\n")
        except ValueError:
            print("Erro ao carregar dados. IDs inválidos no arquivo.\n")
    else:
        print("Nenhum arquivo de dados encontrado. Iniciando com dados vazios.\n")


# ------------------------------
# FUNÇÕES DE POSTOS DE SAÚDE
# ------------------------------
def cadastrar_posto():
    nome = input("Nome do posto: ")
    endereco = input("Endereço: ")
    id_posto = len(postos) + 1
    postos[id_posto] = {"nome": nome, "endereco": endereco}
    print("Posto cadastrado com sucesso!\n")


def editar_posto():
    listar_postos()
    pid = int(input("Digite o ID do posto que deseja editar: "))
    if pid not in postos:
        print("ID inválido.\n")
        return

    novo_nome = input("Novo nome (enter para manter): ")
    novo_endereco = input("Novo endereço (enter para manter): ")

    if novo_nome:
        if any(p["nome"] == novo_nome for p in postos.values()):
            print("Nome do posto já existe.\n")
            return
        postos[pid]["nome"] = novo_nome
    if novo_endereco:
        postos[pid]["endereco"] = novo_endereco

    print("Posto atualizado!\n")


def listar_postos():
    if not postos:
        print("Nenhum posto cadastrado.\n")
        return
    print("\n--- POSTOS DE SAÚDE ---")
    for pid, info in postos.items():
        print(f"{pid} - {info['nome']} | Endereço: {info['endereco']}")
    print()


# ------------------------------
# FUNÇÕES DE MÉDICOS
# ------------------------------
def cadastrar_medico():
    nome = input("Nome do médico: ")
    especialidade = input("Especialidade (área de atuação): ")
    id_med = len(medicos) + 1
    medicos[id_med] = {"nome": nome, "especialidade": especialidade, "horarios": []}
    print("Médico cadastrado!\n")


def editar_medico():
    listar_medicos()
    mid = int(input("Digite o ID do médico a editar: "))
    if mid not in medicos:
        print("ID inválido.\n")
        return

    novo_nome = input("Novo nome (enter para manter): ")
    nova_especialidade = input("Nova especialidade (enter para manter): ")

    if novo_nome:
        medicos[mid]["nome"] = novo_nome
    if nova_especialidade:
        medicos[mid]["especialidade"] = nova_especialidade

    print("Médico atualizado!\n")


def definir_horarios_medico():
    listar_medicos()
    mid = int(input("ID do médico: "))
    if mid not in medicos:
        print("ID inválido.\n")
        return

    print("Digite horários livres no formato HH:MM (vazio para encerrar)")
    while True:
        h = input("Horário: ")
        if not h:
            break
        medicos[mid]["horarios"].append(h)

    print("Horários adicionados!\n")


def listar_medicos():
    if not medicos:
        print("Nenhum médico cadastrado.\n")
        return
    print("\n--- MÉDICOS ---")
    for mid, info in medicos.items():
        print(f"{mid} - {info['nome']} | Especialidade: {info['especialidade']} "
              f"| Horários livres: {', '.join(info['horarios'])}")
    print()


# ------------------------------
# FUNÇÕES DE AGENDAMENTO
# ------------------------------
def agendar_consulta():
    listar_postos()
    pid = int(input("Escolha o ID do posto: "))
    if pid not in postos:
        print("ID inválido.\n")
        return

    listar_medicos()
    mid = int(input("Escolha o ID do médico: "))
    if mid not in medicos:
        print("ID inválido.\n")
        return

    if not medicos[mid]["horarios"]:
        print("Esse médico não tem horários disponíveis.\n")
        return

    especialidade = medicos[mid]["especialidade"]

    print("Horários disponíveis:")
    for h in medicos[mid]["horarios"]:
        print(f"- {h}")

    horario = input("Selecione o horário: ")
    if horario not in medicos[mid]["horarios"]:
        print("Horário inválido.\n")
        return

    nome_paciente = input("Nome do paciente: ")
    data = input("Data da consulta (dd/mm/aaaa): ")
    try:
        datetime.datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        print("Data inválida. Use o formato dd/mm/aaaa.\n")
        return

    agendamentos.append({
        "posto_id": pid,
        "medico_id": mid,
        "especialidade": especialidade,
        "horario": horario,
        "paciente": nome_paciente,
        "data": data
    })

    medicos[mid]["horarios"].remove(horario)
    print("Consulta agendada com sucesso!\n")


def listar_agendamentos():
    if not agendamentos:
        print("Nenhum agendamento realizado.\n")
        return

    print("\n--- AGENDAMENTOS ---")
    for i, ag in enumerate(agendamentos, 1):
        posto_nome = postos[ag['posto_id']]['nome']
        medico_nome = medicos[ag['medico_id']]['nome']
        print(f"{i} - {ag['data']} | Paciente: {ag['paciente']} | Médico: {medico_nome} "
              f"| Especialidade: {ag['especialidade']} | Posto: {posto_nome} | Horário: {ag['horario']}")
    print()


def cancelar_agendamento():
    listar_agendamentos()
    if not agendamentos:
        return

    num = int(input("Digite o número do agendamento a cancelar: "))
    if num < 1 or num > len(agendamentos):
        print("Número inválido.\n")
        return

    ag = agendamentos.pop(num - 1)

    medicos[ag['medico_id']]["horarios"].append(ag["horario"])

    print("Agendamento cancelado!\n")


# ------------------------------
# RELATÓRIOS
# ------------------------------
def relatorio_por_medico():
    listar_medicos()
    nome = input("Digite o nome do médico: ")

    print(f"\n--- RELATÓRIO DO MÉDICO: {nome} ---")
    encontrados = False

    for ag in agendamentos:
        medico_nome = medicos[ag['medico_id']]['nome']
        posto_nome = postos[ag['posto_id']]['nome']
        if medico_nome == nome:
            encontrados = True
            print(f"{ag['data']} | Paciente: {ag['paciente']} | Horário: {ag['horario']} | Posto: {posto_nome}")

    if not encontrados:
        print("Nenhuma consulta encontrada.\n")


def relatorio_por_posto():
    listar_postos()
    nome = input("Digite o nome do posto: ")

    print(f"\n--- RELATÓRIO DO POSTO: {nome} ---")
    encontrados = False

    for ag in agendamentos:
        posto_nome = postos[ag['posto_id']]['nome']
        medico_nome = medicos[ag['medico_id']]['nome']
        if posto_nome == nome:
            encontrados = True
            print(f"{ag['data']} | Paciente: {ag['paciente']} | Médico: {medico_nome} "
                  f"| Horário: {ag['horario']} | Especialidade: {ag['especialidade']}")

    if not encontrados:
        print("Nenhuma consulta encontrada.\n")


def relatorio_por_paciente():
    nome = input("Digite o nome do paciente: ")

    print(f"\n--- RELATÓRIO DO PACIENTE: {nome} ---")
    encontrados = False

    for ag in agendamentos:
        if ag["paciente"] == nome:
            medico_nome = medicos[ag['medico_id']]['nome']
            posto_nome = postos[ag['posto_id']]['nome']
            encontrados = True
            print(f"{ag['data']} | Médico: {medico_nome} | Posto: {posto_nome} "
                  f"| Horário: {ag['horario']} | Especialidade: {ag['especialidade']}")

    if not encontrados:
        print("Nenhuma consulta encontrada.\n")


# ------------------------------
# MENU PRINCIPAL
# ------------------------------
def menu():
    while True:
        
        print("""
===== SISTEMA DE AGENDAMENTO =====
1 - Cadastrar posto
2 - Editar posto
3 - Listar postos
4 - Cadastrar médico
5 - Editar médico
6 - Definir horários de médico
7 - Listar médicos
8 - Agendar consulta
9 - Listar agendamentos
10 - Cancelar agendamento
11 - Relatório por médico
12 - Relatório por posto
13 - Relatório por paciente
0 - Sair
""")

        op = input("Escolha uma opção: ")
        
        if op == "1": cadastrar_posto()
        elif op == "2": editar_posto()
        elif op == "3": listar_postos()
        elif op == "4": cadastrar_medico()
        elif op == "5": editar_medico()
        elif op == "6": definir_horarios_medico()
        elif op == "7": listar_medicos()
        elif op == "8": agendar_consulta()
        elif op == "9": listar_agendamentos()
        elif op == "10": cancelar_agendamento()
        elif op == "11": relatorio_por_medico()
        elif op == "12": relatorio_por_posto()
        elif op == "13": relatorio_por_paciente()
        elif op == "0":
            salvar_dados()
            print("Saindo...")
            break
        else:
            print("Opção inválida!\n")


carregar_dados()
menu()
