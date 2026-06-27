from database.DB_connect import DBConnect
from model.customer import Customer


class DAO():
    @staticmethod
    def getDateRange():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct (i.InvoiceDate) 
                    from Invoice i 
                    order by InvoiceDate"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["InvoiceDate"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT  c.Country 
                    from Customer c """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes( country, date1, date2,):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT c.*
                    from Customer c
                    join Invoice i on i.CustomerId =c.CustomerId 
                    where c.Country = %s
                    and i.InvoiceDate BETWEEN  %s and %s
                    group BY c.CustomerId """

        cursor.execute(query, (country, date1, date2))

        for row in cursor:
            results.append(Customer(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(country, date1, date2, ):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT v1.CustomerId as idCustomer1, v2.CustomerId as idCustomer2, sum(v1.peso1) as pesoCust1, sum(v2.peso2) as pesoCust2
                    from (SELECT c.CustomerId , a.ArtistId , sum(i.total) as peso1
                            from Customer c 
                            join Invoice i on i.CustomerId = c.CustomerId 
                            join InvoiceLine il on i.InvoiceId =il.InvoiceId 
                            join Track t on t.TrackId = il.TrackId 
                            join Album a on t.AlbumId =a.AlbumId 
                            join Artist a2 on a2.ArtistId =a.ArtistId 
                            where c.Country = %s
                            and i.InvoiceDate BETWEEN  %s and %s
                            GROUP by c.CustomerId , a.ArtistId) v1
                    join (SELECT c2.CustomerId , a1.ArtistId, sum(i2.total) as peso2
                            from Customer c2 
                            join Invoice i2 on i2.CustomerId = c2.CustomerId 
                            join InvoiceLine il2 on i2.InvoiceId =il2.InvoiceId 
                            join Track t2 on t2.TrackId = il2.TrackId 
                            join Album a1 on t2.AlbumId =a1.AlbumId 
                            join Artist a12 on a12.ArtistId =a1.ArtistId 
                            where c2.Country = %s
                            and i2.InvoiceDate BETWEEN  %s and %s
                            GROUP by c2.CustomerId , a1.ArtistId ) v2
                    on v1.ArtistId=v2.ArtistId
                    where v1.CustomerId<v2.CustomerId
                    group by idCustomer1 , idCustomer2"""

        cursor.execute(query, (country, date1, date2, country, date1, date2,))

        for row in cursor:
            results.append(( row["idCustomer1"],
                            row["idCustomer2"],
                            row["pesoCust1"],
                             row["pesoCust2"],))

        cursor.close()
        conn.close()
        return results




