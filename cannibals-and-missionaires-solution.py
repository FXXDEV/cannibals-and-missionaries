
# -*- coding: utf-8 -*-
class State():   
    def __init__(self, left_missionaires, right_missionaires, left_cannibals, right_cannibals, side):
        #Inicialização do estado
        self.side = side
        self.node = None
        self.childrens = []
        self.left_missionaires = left_missionaires
        self.right_missionaires = right_missionaires
        self.left_cannibals = left_cannibals
        self.right_cannibals = right_cannibals
 
    def valid_state(self):
        # Não  gerar estados numero negativo de elementos de cada lado do rio
        if ((self.left_missionaires < 0) 
            or (self.left_cannibals < 0)
            or (self.right_missionaires < 0) 
            or (self.right_cannibals < 0)):
            return False

        #Verifica se a não há mais canibais que missionarios em cada lado do rio.
        if ((self.left_missionaires == 0 or self.left_missionaires >= self.left_cannibals)and
            (self.right_missionaires == 0 or self.right_missionaires >= self.right_cannibals)):
            return True
       


    #Gera estados validos sem ser estado final
    def generate_childrens(self):
        # Lista de combinações possíveis no barco 
        possible_moves = [
            #[0 = missionario, 1 = cannibal ]
            [1,0],[1,1],[0,2],[2,0],[0,1]
        ]
              
        # Gera os possíveis estados e armazena apenas os válidos no estado atual
        for move in possible_moves:
            if self.side == 'rs':
                #Barco na direita, ambos saem da direita pra esquerda

                #movimentação dos missionarios da esquerda para a direita
                right_missionaires = self.right_missionaires - move[0]
                left_missionaires = self.left_missionaires + move[0]

                #movimentação dos cannibais da esquerda para a direita
                right_cannibals = self.right_cannibals - move[1]
                left_cannibals = self.left_cannibals + move[1]

                #Criação do estado do filho
                children = State(left_missionaires, right_missionaires, left_cannibals,right_cannibals, 'ls')
            else:
                #Barco na esquerda, ambos saem da esquerda pra direita

                #movimentação dos missionarios da direita para a esquerda
                left_missionaires = self.left_missionaires - move[0]
                right_missionaires = self.right_missionaires + move[0]

                #movimentação dos cannibais da direita para a esquerda
                left_cannibals = self.left_cannibals - move[1]
                right_cannibals = self.right_cannibals + move[1]
                
                #Criação do estado do filho
                children = State(left_missionaires, right_missionaires, left_cannibals,right_cannibals, 'rs')


            #adiciona a lista
            children.node = self

            #validação de estado
            if children.valid_state():
                #adiciona como filhos do pai
                self.childrens.append(children)


        # Verifica se todos atravessaram o rio (3 e 3 / 0 e 0)
    def final_state(self):
        #rs = lado direito | ls = lado esquerdo
        if ((self.right_missionaires and self.right_cannibals) == 3 and 
           (self.left_missionaires and self.left_cannibals) == 0):
           return True
        else:
            return False


#Gera arvore de estados.
class Problem():
    def __init__(self):
        #Insere a raiz indefinida na fila, apenas estado inicial,  insere a raiz na 
        #Insere a raiz na fila de execução, que será utilizada para fazer uma busca em largura
        self.query = [State(3, 0, 3, 0, 'ls')]
        self.solution = None

    def solve_problem(self):
        #Solucao gerando árvore de estados percorrida com busca em largura, utilizando a query
      
        for element in self.query:
            if element.final_state():
                # Se a solução foi encontrada, gera o caminho até a raiz da arvore e encerra
                self.solution = [element]
                while element.node:
                    self.solution.insert(0, element.node)
                    element = element.node
                break;
            #Se o elemento nao solucionar gera os filhos na query
            element.generate_childrens()
            self.query.extend(element.childrens)


def main():
    # Instancia do problema e chamada de soluçao    
    problem = Problem()
    problem.solve_problem()

    #reordena a lista de solucoes
    problem.solution.reverse() 
    print('\t\t\t\t  Solução:\n',50*'--')
    for state in problem.solution:
        print (
            'Missionarios a esquerda do rio:',state.left_missionaires, '\t|\t '  ,  'Missionarios a direita do rio:',state.right_missionaires,'\n'
            'Canibais a esquerda do rio:',state.left_cannibals, '\t\t|\t ' ,  'Canibais a direita do rio:',state.right_cannibals,'\n',50*'--'
           )

if __name__ == '__main__':
    main()