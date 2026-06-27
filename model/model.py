import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._allNodes = None
        self._allCountries = None
        self._graph = nx.DiGraph()
        self._idMap = {}

   
    def getDateRange(self):
        return DAO.getDateRange()
    
    def getAllCountries(self):
        self._allCountries= DAO.getAllCountries()
        return self._allCountries

    def buildGraph(self, country, date1, date2):
        self._graph.clear()
        self._allNodes = DAO.getAllNodes(country, date1, date2)
        for n in self._allNodes:
            self._idMap[n.CustomerId]=n
            self._graph.add_node(n)
        self.addEdges(country,date1 ,date2)

    def addEdges(self, genre, date1, date2):
        self._edges = DAO.getEdges(genre, date1, date2)
        for e in self._edges:
            if e[2] < e[3]:
                self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2] + e[3])
            elif e[2] > e[3]:
                self._graph.add_edge(self._idMap[e[1]], self._idMap[e[0]], weight=e[2] + e[3])
            else:
                self._graph.add_edge(self._idMap[e[0]], self._idMap[e[1]], weight=e[2] + e[3])
                self._graph.add_edge(self._idMap[e[1]], self._idMap[e[0]], weight=e[2] + e[3])

    def getGraph(self):
        return self._graph

    def detailGraph(self):
        return len(self._graph.nodes()), len(self._graph.edges())

    def top5(self):
        listaNodoPesotot=[]
        for n in self._graph.nodes():
            valore=0
            for s in self._graph.successors(n):
                peso = self._graph.get_edge_data(n, s, "weight")
                valore += peso["weight"]
            listaNodoPesotot.append((n, valore))
        return listaNodoPesotot

    def getPath(self, customerStart, customerEnd, lun):
        self._bestPath=[]
        self._lunPath=lun
        self._bestPeso=0
        self.ricorsione([customerStart], customerEnd)
        return self._bestPath, self._bestPeso

    def ricorsione(self, parziale, customerEnd):
        if len(parziale)<=self._lunPath and parziale[-1]==customerEnd:
            pesoTot= self.calcoloPeso(parziale)
            if pesoTot>self._bestPeso:
                self._bestPeso=pesoTot
                self._bestPath = copy.deepcopy(parziale)
        else:
            print("qui")
            for n in self._graph.successors(parziale[-1]):
                print(f"Esploro nodo {parziale[-1]}, successori: {list(self._graph.successors(parziale[-1]))}")
                if n not in parziale:
                    parziale.append(n)
                    self.ricorsione(parziale, customerEnd)
                    parziale.pop()



    def calcoloPeso(self, parziale):
        peso=0
        for i in range(len(parziale)-1):
            valore=self._graph.get_edge_data(parziale[i], parziale[i+1], "weight")
            peso += valore["weight"]
        return peso


