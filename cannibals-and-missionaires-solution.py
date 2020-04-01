

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
        if ((self.left_missionaires < 0) or (self.left_cannibals < 0)
            or (self.right_missionaires < 0) or (self.right_cannibals < 0)):
            return False

        #Verifica se a não há mais canibais que missionarios em cada lado do rio.
        return ((self.left_missionaires == 0 or self.left_missionaires >= self.left_cannibals) and
                (self.right_missionaires == 0 or self.right_missionaires >= self.right_cannibals))




    

    #Gera estados validos sem ser estado final
    def generate_childrens(self):
        # Lista de possíveis combinações no barco 
        possible_moves = [
            
            {'miss': 0, 'can': 1},
            {'miss': 0, 'can': 2},
            {'miss': 2, 'can': 0},
            {'miss': 1, 'can': 0},
            {'miss': 1, 'can': 1},
            
        ]

        

        # Encontra o novo lado do rio
        new_side = 'ls' if self.side == 'rs' else 'rs'
        
       
        # Gera os possíveis estados e armazena apenas os válidos no estado atual
        for move in possible_moves:
            if self.side == 'rs':
                #Barco na direita, ambos saem da direita pra esquerda
                right_missionaires = self.right_missionaires - move['miss']
                left_missionaires = self.left_missionaires + move['miss']
                right_cannibals = self.right_cannibals - move['can']
                left_cannibals = self.left_cannibals + move['can']
              
            else:
                #Barco na esquerda, ambos saem da esquerda pra direita
                left_missionaires = self.left_missionaires - move['miss']
                right_missionaires = self.right_missionaires + move['miss']
                left_cannibals = self.left_cannibals - move['can']
                right_cannibals = self.right_cannibals + move['can']
            # Cria o estado do filho e caso este seja válido, o adiciona à lista de children do pai
            children = State(left_missionaires, right_missionaires, left_cannibals,
                           right_cannibals, new_side)
            children.node = self
            if children.valid_state():
                self.childrens.append(children)


            

        # Verifica se todos atravessaram o rio (3 e 3 / 0 e 0)
    def final_state(self):
        #rs = lado direito | ls = lado esquerdo
        result_ls = self.left_missionaires == self.left_cannibals == 0
        result_rs = self.right_missionaires == self.right_cannibals == 3
        return (result_ls and result_rs)

       

#Gera arvore de estados.
class Problem():
    def __init__(self):
        #Inicializa uma instância com raiz pré-definida e ainda sem solução.
        #Insere a raiz na fila de execução, que será utilizada para fazer uma busca em largura
        self.query = [State(3, 0, 3, 0, 'ls')]
        self.solution = None

    def solve_problem(self):
        #Solucao gerando árvore de estados percorrida com busca em alrgura, utilizando a query
        # Realiza a busca em largura em busca da solução
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
            'Missionarios a esquerda do rio:',state.left_missionaires, '\t|\t ' ,  'Missionarios a direita do rio:',state.right_missionaires,'\n'
            'Canibais a esquerda do rio:',state.left_cannibals, '\t\t|\t ', 'Canibais a direita do rio:',state.right_cannibals,'\n',50*'--'
           )

if __name__ == '__main__':
    main()