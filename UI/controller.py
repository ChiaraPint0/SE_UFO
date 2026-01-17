import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        #liste che servono a popolare il dropdown
        self._list_year = []
        self._list_shape = []

    def populate_dd(self): #per riempire i dropdown(tendina) degli anni
        """ Metodo per popolare il dropdown dd_year """
        sighting_list = self._model.list_sighting #accedo alla lista degli avvistamenti caricata dal model

        # Popola lista anni unici
        for n in sighting_list: #scorro tutti gli avvistamenti
            if n.s_datetime.year not in self._list_year:
                self._list_year.append(n.s_datetime.year) #estraggo l'anno dalla data

        # Popola dropdown anni
        for year in self._list_year: #per ogni anno creo l'opzione dropdown e la aggiungo alla view
            self._view.dd_year.options.append(ft.dropdown.Option(year))

        self._view.update() #aggiorno interfaccia

    def change_option_year(self, e):
        # Handler di dd_year associato all'evento "on_change"
        self._populate_dd_shape() #quando l'anno cambia, aggiorno le forme disponibili per quell'anno

    def _populate_dd_shape(self):
        # Metodo per popolare il dropdown dd_shape con le forme filtrate in base all'anno
        self._list_shape = self._model.get_shapes(self._view.dd_year.value) #leggo l'anno selezionato dall'utente e
        #chiedo al model le forme disponibili

        # Popola dropdown shapes
        for shape in self._list_shape:
            self._view.dd_shape.options.append(ft.dropdown.Option(shape))

        self._view.update()

    def handle_graph(self, e): # premere bottone crea grafo
        """ Handler per gestire creazione del grafo """
        selected_year = self._view.dd_year.value #leggo i parametri inseriti dall'utente
        selected_shape = self._view.dd_shape.value

        # Pulisce area risultato
        self._view.lista_visualizzazione_1.controls.clear() #pulisco area output

        # Costruisce grafo con i parametri selezionati
        self._model.build_graph(selected_shape, selected_year) #il controller affida la creazione del grafo al model

        # Mostra info grafo
        self._view.lista_visualizzazione_1.controls.append(
            ft.Text(
                f"Numero di vertici: {self._model.get_num_of_nodes()} " #il controller chiede al model i dati e li mostra 
                f"Numero di archi: {self._model.get_num_of_edges()}"
            )
        )

        # Mostra somma pesi per nodo
        for node_info in self._model.get_sum_weight_per_node():
            self._view.lista_visualizzazione_1.controls.append( #ottengo la lista di tuple (id_stato, somma_pesi)
                ft.Text(f"Nodo {node_info[0]}, somma pesi su archi = {node_info[1]}")
            )

        self._view.update()

    def handle_path(self, e):
        self._view.show_alert("Funzione Calcola Percorso non ancora implementata.")
        self._view.update()
