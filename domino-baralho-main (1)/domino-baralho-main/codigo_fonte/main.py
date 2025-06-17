import time
from .setup_game import Jogo
from .visual import limpar_tela

def mostrar_instrucoes():
    limpar_tela()
    print("\n==== INSTRUÇÕES ====")
    print("Dominó de Baralho:")
    print("- Jogue cartas sequenciais no mesmo naipe, como no dominó.")
    print("- O jogo começa com os 7 de cada naipe.")
    print("- Vence quem esvaziar a mão primeiro.")
    print("- Caso não possa jogar, você pode passar a vez digitando 0.")
    print("- Boa sorte!\n")
    
    input("Pressione ENTER para voltar ao menu...")

def iniciar_partida():
    while True:
        jogo = Jogo()
        jogo.iniciar()

        if jogo.resultado == "vitoria":
            print("🎉 PARABÉNS! VOCÊ GANHOU! 🎉")
        elif jogo.resultado == "derrota":
            print("💀 VOCÊ PERDEU... TENTE NOVAMENTE. 💀")

        while True:
            resposta = input("Deseja jogar novamente? (s/n): ").lower()
            if resposta == 's':
                break
            elif resposta == 'n':
                return 
            else:
                print("Digite apenas 's' ou 'n'.")

def menu():
    while True:
        limpar_tela()
        time.sleep(0.5)
        
        print("""       

██████╗░░█████╗░███╗░░░███╗██╗███╗░░██╗░█████╗░  ██████╗░███████╗
██╔══██╗██╔══██╗████╗░████║██║████╗░██║██╔══██╗  ██╔══██╗██╔════╝
██║░░██║██║░░██║██╔████╔██║██║██╔██╗██║██║░░██║  ██║░░██║█████╗░░
██║░░██║██║░░██║██║╚██╔╝██║██║██║╚████║██║░░██║  ██║░░██║██╔══╝░░
██████╔╝╚█████╔╝██║░╚═╝░██║██║██║░╚███║╚█████╔╝  ██████╔╝███████╗
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═╝╚═╝░░╚══╝░╚════╝░  ╚═════╝░╚══════╝

    ██████╗░░█████╗░██████╗░░█████╗░██╗░░░░░██╗░░██╗░█████╗░
    ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║░░░░░██║░░██║██╔══██╗
    ██████╦╝███████║██████╔╝███████║██║░░░░░███████║██║░░██║
    ██╔══██╗██╔══██║██╔══██╗██╔══██║██║░░░░░██╔══██║██║░░██║
    ██████╦╝██║░░██║██║░░██║██║░░██║███████╗██║░░██║╚█████╔╝
    ╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░╚════╝░
              """)

        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║                         MENU DO JOGO                          ║")
        print("╠═══════════════════════════════════════════════════════════════╣")
        print("║                         1 - Jogar                             ║")
        print("║                         2 - Instruções                        ║")
        print("║                         3 - Sair                              ║")
        print("╚═══════════════════════════════════════════════════════════════╝")

        escolha = input("\nDigite sua opção: ")

        match escolha:
            case "1":
                iniciar_partida()
            case "2":
                mostrar_instrucoes()
            case "3":
                print("Até a próxima!")
                break
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
