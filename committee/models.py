from django.db import models
from django.db import connection

def create_event(payload):
    with connection.cursor() as cursor:
        id_pertandingan = payload['id_pertandingan']
        jenis = payload['jenis']
        datetime = payload['datetime']
        id_pemain = payload['id_pemain']

        cursor.execute("BEGIN")
        
        try:
            cursor.execute(
                """
                    INSERT INTO "Peristiwa" ("ID_Pertandingan", "Jenis", "Datetime", "ID_Pemain") 
                    VALUES (%s, %s, %s, %s,)
                """, 
                [id_pertandingan, jenis, datetime, id_pemain]
            )
            
            cursor.execute('COMMIT;')
        except Exception as e:
            cursor.execute('ROLLBACK;')
            raise e
        
def get_players():
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT
                    "ID_Pemain",
                    "Pemain"."Nama_Depan" || ' ' || "Pemain"."Nama_Belakang" || ' - ' || "Posisi"
                FROM "Pemain"
                WHERE "Nama_Tim" IS NULL
            """
        )
        
        rows = cursor.fetchall()
        
        players = []
        
        for row in rows:
            players.append({
                "id": row[0],
                "nama": row[1],
            })
        
        return players 
    
