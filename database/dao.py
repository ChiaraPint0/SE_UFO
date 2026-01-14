from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting

class DAO:
    @staticmethod
    def get_all_states(): #restutiusce la lista completa degli stati
        conn = DBConnect.get_connection() #apro connessione

        result = [] #creo una lista che conterrà gli oggetti State risultati

        cursor = conn.cursor(dictionary=True) #cursore che restituisce ogni riga come dizionario
        query = """ SELECT * FROM state """

        cursor.execute(query)

        for row in cursor:
            result.append(State(row["id"], row["name"], row["capital"],
                                row["lat"], row["lng"], row["area"],
                                row["population"], row["neighbors"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_sighting(): #recupera tutti gli avvistamenti
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * 
                    FROM sighting
                    ORDER BY s_datetime ASC """ #ordina per data crescente così la lista è cronologica

        cursor.execute(query)

        for row in cursor:
            result.append(Sighting(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_shapes(year):  #recupera l'elenco delle forme disponibili in un certo anno
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT shape #no duplicati
                    FROM sighting 
                    WHERE shape <> "" AND YEAR(s_datetime) = %s """ #esclude la forma vuota e filtra per anno

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_weighted_neigh(year, shape):  #crea archi pesati tra stati confinanti, dove il peso è il numero di avvistamenti compatibili.
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT LEAST(n.state1, n.state2) AS st1,
                           GREATEST(n.state1, n.state2) AS st2, 
                           COUNT(*) as N
                    FROM sighting s , neighbor n 
                    WHERE year(s.s_datetime) = %s #solo quelli dell'anno e della shape selezionati
                          AND s.shape = %s
                          AND (s.state = n.state1 OR s.state = n.state2)
                    GROUP BY st1 , st2 """

        cursor.execute(query, (year, shape)) #eseguo la query con i parametri

        for row in cursor:
            result.append((row['st1'], row['st2'], row["N"])) #ogni riga restituisce id primo stato, id secondo stato, peso arco

        cursor.close()
        conn.close()
        return result