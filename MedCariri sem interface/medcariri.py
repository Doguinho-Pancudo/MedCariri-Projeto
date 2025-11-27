import datetime

postos = {}
medicos = {}
agendamentos = []


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

    agendamentos.append({
        "posto": postos[pid]["nome"],
        "medico": medicos[mid]["nome"],
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
        print(f"{i} - {ag['data']} | Paciente: {ag['paciente']} | Médico: {ag['medico']} "
              f"| Especialidade: {ag['especialidade']} | Posto: {ag['posto']} | Horário: {ag['horario']}")
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

    for mid, m in medicos.items():
        if m["nome"] == ag["medico"]:
            m["horarios"].append(ag["horario"])

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
        if ag["medico"] == nome:
            encontrados = True
            print(f"{ag['data']} | Paciente: {ag['paciente']} | Horário: {ag['horario']} | Posto: {ag['posto']}")

    if not encontrados:
        print("Nenhuma consulta encontrada.\n")


def relatorio_por_posto():
    listar_postos()
    nome = input("Digite o nome do posto: ")

    print(f"\n--- RELATÓRIO DO POSTO: {nome} ---")
    encontrados = False

    for ag in agendamentos:
        if ag["posto"] == nome:
            encontrados = True
            print(f"{ag['data']} | Paciente: {ag['paciente']} | Médico: {ag['medico']} "
                  f"| Horário: {ag['horario']} | Especialidade: {ag['especialidade']}")

    if not encontrados:
        print("Nenhuma consulta encontrada.\n")


def relatorio_por_paciente():
    nome = input("Digite o nome do paciente: ")

    print(f"\n--- RELATÓRIO DO PACIENTE: {nome} ---")
    encontrados = False

    for ag in agendamentos:
        if ag["paciente"] == nome:
            encontrados = True
            print(f"{ag['data']} | Médico: {ag['medico']} | Posto: {ag['posto']} "
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
            print("Saindo...")
            break
        else:
            print("Opção inválida!\n")


menu()
