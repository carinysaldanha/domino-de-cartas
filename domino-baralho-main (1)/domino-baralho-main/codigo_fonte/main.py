import time #Importa o módulo
from .setup_game import Jogo #Importa a classe
from .visual import limpar_tela #Importa a função
def mostrar_instrucoes():#Limpa a tela.Exibe as regras do jogo para o usuário.Pausa esperando o usuário pressionar ENTER para voltar.
    limpar_tela()
    print("\n==== INSTRUÇÕES ====")
    print("Dominó de Baralho:")
    print("- Jogue cartas sequenciais no mesmo naipe, como no dominó.")
    print("- O jogo começa com os 7 de cada naipe.")
    print("- Vence quem esvaziar a mão primeiro.")
    print("- Caso não possa jogar, você pode passar a vez digitando 0.")
    print("- Boa sorte!\n")
    
    input("Pressione ENTER para voltar ao menu...")

#Entra em um loop para jogar várias partidas seguidas, se o usuário quiser.
#Cria uma nova instância do jogo (Jogo()).
#Começa o jogo com jogo.iniciar().
#Após o jogo acabar, verifica se foi vitória ou derrota e mostra mensagem.
#Pergunta ao usuário se quer jogar novamente.
#Se "s" (sim), o loop recomeça e cria um novo jogo.
#Se "n" (não), a função termina e volta para o menu.
#Se resposta inválida, pede para digitar de novo.


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

#Loop infinito para manter o menu ativo até o usuário sair.
#Limpa a tela e faz uma pausa rápida para melhorar visual.
#Mostra uma arte em ASCII com o nome do jogo.
#Exibe o menu de opções numeradas.
#Pede para o usuário digitar a opção.
#Usa match para decidir o que fazer:
#"1" chama iniciar_partida()
#"2" chama mostrar_instrucoes()
#"3" imprime uma mensagem e sai do menu (termina o programa)
#Qualquer outra entrada exibe aviso de opção inválida

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
#Se o arquivo for executado diretamente (não importado), chama a função menu() para começar a interface.
if __name__ == "__main__":
    menu()
