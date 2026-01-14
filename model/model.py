from database.dao import DAO
import networkx as nx


class Model:
    def __init__(self):
        self.list_sighting = []
        self.list_states = []

        self.G = nx.Graph() #grafo non orientato
        self._nodes = []
        self._edges = []
        self.id_map = {}

        self.load_sighting()
        self.load_states()

    def load_sighting(self): #delega per il Dao
        self.list_sighting = DAO.get_all_sighting() #salva i risultati in memoria

    def load_states(self):
        self.list_states = DAO.get_all_states() #salva gli oggetti che saranno i nodi del grafo

    def get_shapes(self, selected_year):
        return DAO.get_all_shapes(selected_year)

    def build_graph(self, s, a): #s = shapes, a = anno)
        self.G.clear()
        #con questi evito di ricreare il grafo più volte, accumulando dati
        self._nodes = []
        self._edges = []
        self.id_map = {}

        #1) nodi
        for p in self.list_states: #ogni stato diventa un nodo
            self._nodes.append(p)

        self.G.add_nodes_from(self._nodes) #inserisco i nodi al grafo

        self.id_map = {} #con questo passo da state_id(quindi DB) a oggetto state (grafo)
        for n in self._nodes:
            self.id_map[n.id] = n  #id_map[id] = oggetto

        #2) archi
        tmp_edges = DAO.get_all_weighted_neigh(a, s) #il dao restituisce (id_state1, id_state2, peso)
        #dove peso = numero di avvistamenti

        self._edges.clear() #pulizia lista archi
        for e in tmp_edges: #trasfromo (id1,id2,peso) -> (state1, state2, peso)
            self._edges.append((self.id_map[e[0]], self.id_map[e[1]], e[2]))

        self.G.add_weighted_edges_from(self._edges) #costrusico i grafo pesato

    def get_sum_weight_per_node(self):
        pp = []
        for n in self.G.nodes():
            sum_w = 0
            for e in self.G.edges(n, data=True):
                sum_w += e[2]['weight'] #sommo il peso degli archi incidenti
            pp.append((n.id, sum_w))
        return pp

    def get_nodes(self):
        return self.G.nodes()

    def get_edges(self):
        return list(self.G.edges(data=True))

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()

    def get_num_of_edges(self):
        return self.G.number_of_edges()