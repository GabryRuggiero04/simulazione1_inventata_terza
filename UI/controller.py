import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCountry(self):
        allCountries = self._model.getAllCountries()
        for c in allCountries:
            self._view._ddCountry.options.append(
                ft.dropdown.Option(text=c)
            )

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        if self._view._ddCountry.value is None:
            self._view.create_alert("Scegliere una nazione")
            return
        nazione=self._view._ddCountry.value
        dataStart = self._view._dp1.value
        dataEnd = self._view._dp2.value
        if (dataStart is None):
            self._view.create_alert("Scegliere data start!!")
            return
        if (dataEnd is None):
            self._view.create_alert("Scegliere data end!!")
            return
        if dataStart > dataEnd:
            self._view.create_alert("La data di start deve precedere la data di end!!")
            return
        self._view.txt_result.controls.append(
            ft.Text("Date selezionate: ", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Start: {dataStart.date()}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"End: {dataEnd.date()}")
        )
        self._model.buildGraph(nazione, dataStart, dataEnd)
        grafo = self._model.getGraph()
        if len(grafo.nodes()) < 1:
            self._view.txt_result.controls.append(
                ft.Text(f"Grafo vuoto o creato in modo errato", color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        numNodes, numEdges = self._model.detailGraph()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero nodi: {numNodes}")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero archi: {numEdges}")
        )
        listaNodoValore= list(self._model.top5())
        self._view.txt_result.controls.append(
            ft.Text("I 5 prodotti più venduti sono: ", color="green")
        )
        listaNodoValore.sort(key=lambda x: x[1], reverse=True)
        top=5
        if len(listaNodoValore)<top:
            top=len(listaNodoValore)
        for i in range (0, top):
            self._view.txt_result.controls.append(
                ft.Text(f"{listaNodoValore[i][0]} con peso: {listaNodoValore[i][1]}")
            )
        nodesList=grafo.nodes()
        for n in nodesList:
            self._view._ddCustomerStart.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.CustomerId,
                                    text=n.FirstName,
                                   on_click=self.choiceCostumerStart)
                                    )
            self._view._ddCustomerEnd.options.append(
                ft.dropdown.Option(data=n,
                                   key=n.CustomerId,
                                   text=n.FirstName,
                                   on_click=self.choiceCostumerEnd)
                )
            self._view.update_page()

    def choiceCostumerStart(self, e):
       self._CustomerStartSelectedValue = e.control.data
       return self._CustomerStartSelectedValue

    def choiceCostumerEnd(self, e):
        self._CustomerEndSelectedValue = e.control.data
        return self._CustomerEndSelectedValue

    def handleCercaCammino(self,e):
        self._view.txt_result.controls.clear()
        customerStart = self._CustomerStartSelectedValue
        customerEnd = self._CustomerEndSelectedValue
        if self._view._ddCustomerStart.value is None:
            self._view.create_alert("Scegliere un prodotto di partenza!!")
            return
        if self._view._ddCustomerEnd.value is None:
            self._view.create_alert("Scegliere un prodotto di arrivo!!")
            return
        lun = self._view._txtLun.value
        if lun == "":
            self._view.create_alert("Inserire lunghezza del cammino!!")
            return
        try:
            lunInt = int(lun)
        except ValueError:
            self._view.create_alert("Inserire un numero intero come lunghezza del cammino!!")
            return
        if lunInt < 0:
            self._view.create_alert("Inserire un numero positivo come la lunghezza del cammino!!")
            return
        pathNodes, sumWeight = self._model.getPath(customerStart, customerEnd, lunInt)
        if len(pathNodes) < 1:
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun cammino trovato da {customerStart} a {customerEnd} con lunghezza {lunInt} passi",
                        color="red")
            )
            self._view.update_page()
            return
        self._view.txt_result.controls.append(
            ft.Text(f"Cammino da ({customerStart}) a ({customerEnd}) con lunghezza {len(pathNodes)} passi trovato", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Peso totale del cammino: {sumWeight}", color="green")
        )
        for n in pathNodes:
            self._view.txt_result.controls.append(
                ft.Text(n)
            )
        self._view.update_page()

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)




