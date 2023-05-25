from django.db import connection
import uuid
from datetime import datetime


# Create your models here.
def convert_time(date_time):
    # Convert datetime-local value to SQL timestamp format
    dt = datetime.strptime(date_time, "%Y-%m-%dT%H:%M")
    timestamp_value = dt.strftime("%Y-%m-%d %H:%M:%S")
    print(timestamp_value)
    return timestamp_value

def get_all_wasit():
    with connection.cursor() as cursor:
        cursor.execute("""
        Select np."Nama_Depan" || ' ' || np."Nama_Belakang" AS nama_wasit 
            from public."Wasit" as w join public."Non_Pemain" as np on
            w."ID_Wasit" = np."ID"
        """)
        rows = cursor.fetchall()
        referee = []
        
        for row in rows:
            referee.append(
                row[0]
            )
        
        return referee
    
def get_all_stadium():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT "Nama" FROM public."Stadium"
        """)
        rows = cursor.fetchall()
        stadiums = []

        for row in rows:
            stadiums.append(
                row[0]
            )
        return stadiums

def get_all_team():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT "Nama_Tim" FROM public."Tim"
        """)
        rows = cursor.fetchall()
        teams = []

        for row in rows:
            teams.append(
                row[0]
            )
        return teams

def get_available_wasit(start_date, end_date):
    with connection.cursor() as cursor:
        cursor.execute("""
            Select np."Nama_Depan" || ' ' || np."Nama_Belakang" AS nama_wasit 
            from public."Wasit" as w join public."Non_Pemain" as np on
            w."ID_Wasit" = np."ID"

            except 

            Select np."Nama_Depan" || ' ' || np."Nama_Belakang" AS nama_wasit
            From public."Pertandingan" as p,
            public."Wasit" as w,
            public."Wasit_Bertugas" as wb,
            public."Non_Pemain" as np
            where
            p."ID_Pertandingan" = wb."ID_Pertandingan" and
            w."ID_Wasit" = wb."ID_Wasit" and
            w."ID_Wasit" = np."ID" and
            p."End_Datetime" >= %s and
            p."Start_Datetime" <= %s
        """, [start_date, end_date])
        rows = cursor.fetchall()
        referee = []
        
        for row in rows:
            referee.append({
                "nama": row[0],
            })
        
        return referee
    
def get_stadium_id(stadium):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT "ID_Stadium" FROM public."Stadium"
        WHERE "Nama" = %s
        """,[stadium])
        rows = cursor.fetchall()
        stadium_id = rows[0][0]
        return stadium_id
    
def get_wasit_id(wasit):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT "ID" FROM public."Non_Pemain"
        WHERE "Nama_Depan" || ' ' || "Nama_Belakang" = %s
        """,[wasit])
        rows = cursor.fetchall()
        wasit_id = rows[0][0]
        return wasit_id
    
def get_pertandingan_id(start_datetime, end_datetime, stadium):
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT "ID_Pertandingan" FROM public."Pertandingan"
        WHERE "Start_Datetime" = %s and
        "End_Datetime" = %s and
        "Stadium" = %s
        """,[start_datetime, end_datetime, stadium])
        rows = cursor.fetchall()
        pertandingan_id = rows[0][0]
        return pertandingan_id

def create_pertandingan(payload):
    with connection.cursor() as cursor:
        stadium = payload['stadium']
        tanggal_pertandingan_awal = payload['tanggal-pertandingan-awal']
        tanggal_pertandingan_akhir = payload['tanggal-pertandingan-akhir']
        wasit_utama = payload['wasit-utama']
        wasit_pembantu_1 = payload['wasit-pembantu-1']
        wasit_pembantu_2 = payload['wasit-pembantu-2']
        wasit_cadangan = payload['wasit-cadangan']
        tim_1 = payload['tim-1']
        tim_2 = payload['tim-2']
        
        stadium_id = get_stadium_id(stadium)

        id_wasit_utama = get_wasit_id(wasit_utama)
        id_wasit_pembantu_1 = get_wasit_id(wasit_pembantu_1)
        id_wasit_pembantu_2 = get_wasit_id(wasit_pembantu_2)
        id_wasit_cadangan = get_wasit_id(wasit_cadangan)

        tanggal_pertandingan_awal = convert_time(tanggal_pertandingan_awal)
        tanggal_pertandingan_akhir = convert_time(tanggal_pertandingan_akhir)
        print(tanggal_pertandingan_awal)        
        print(tanggal_pertandingan_akhir)        


        id_pertandingan = uuid.uuid4()
        print(id_pertandingan)
        
        cursor.execute("BEGIN;")

        try:
            cursor.execute(
                """
                    INSERT INTO public."Pertandingan" ("ID_Pertandingan","Start_Datetime", "End_Datetime", "Stadium") 
                    VALUES (%s, %s, %s, %s)
                """, 
                [id_pertandingan, tanggal_pertandingan_awal, tanggal_pertandingan_akhir, stadium_id]
            )
            cursor.execute(
                """
                    INSERT INTO public."Wasit_Bertugas" ("ID_Wasit", "ID_Pertandingan", "Posisi_Wasit") 
                    VALUES (%s, %s, 'utama')
                """,
                [id_wasit_utama, id_pertandingan]
                )
            cursor.execute(
                """
                    INSERT INTO public."Wasit_Bertugas" ("ID_Wasit", "ID_Pertandingan", "Posisi_Wasit") 
                    VALUES (%s, %s, 'pembantu')
                """,
                [id_wasit_pembantu_1, id_pertandingan]
                )
            cursor.execute(
                """
                    INSERT INTO public."Wasit_Bertugas" ("ID_Wasit", "ID_Pertandingan", "Posisi_Wasit") 
                    VALUES (%s, %s, 'pembantu')
                """,
                [id_wasit_pembantu_2, id_pertandingan]
                )
            cursor.execute(
                """
                    INSERT INTO public."Wasit_Bertugas" ("ID_Wasit", "ID_Pertandingan", "Posisi_Wasit") 
                    VALUES (%s, %s, 'cadangan')
                """,
                [id_wasit_cadangan, id_pertandingan]
                )
            cursor.execute(
                """
                    INSERT INTO public."Tim_Pertandingan" ("Nama_Tim", "ID_Pertandingan", "Skor") 
                    VALUES (%s, %s, '0')
                """,
                [tim_1, id_pertandingan]
                 )
            cursor.execute(
                """
                    INSERT INTO public."Tim_Pertandingan" ("Nama_Tim", "ID_Pertandingan", "Skor") 
                    VALUES (%s, %s, '   0')
                """,
                [tim_2, id_pertandingan]
                 )
            
            cursor.execute('COMMIT;')
        except Exception as e:
            cursor.execute('ROLLBACK;')
            raise e

def delete_page_by_id(id):
    with connection.cursor() as cursor:
        cursor.execute("""
        DELETE FROM "Peristiwa"
        WHERE "ID_Pertandingan" = %s;
        """, [id])

        cursor.execute("""
        DELETE FROM "Wasit_Bertugas"
        WHERE "ID_Pertandingan" = %s;
        """, [id])

        cursor.execute("""
        DELETE FROM "Pembelian_Tiket"
        WHERE "ID_Pertandingan" = %s;
        """, [id])

        cursor.execute("""
        DELETE FROM "Tim_Pertandingan"
        WHERE "ID_Pertandingan" = %s;
        """, [id])

        cursor.execute("""
        DELETE FROM "Rapat"
        WHERE "ID_Pertandingan" = %s;
        """, [id])

        cursor.execute("""
        DELETE FROM "Pertandingan"
        WHERE "ID_Pertandingan" = %s;
        """, [id])

def show_all_tim_bertanding():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT STRING_AGG(tm."Nama_Tim", ' vs ') AS tim_bertanding, p."Start_Datetime" ||' - '|| p."End_Datetime" as waktu, tm."ID_Pertandingan"
    FROM "Tim_Pertandingan" AS tm join "Pertandingan" AS p on tm."ID_Pertandingan" = p."ID_Pertandingan"
    GROUP BY (tm."ID_Pertandingan", waktu)
    ORDER BY (tim_bertanding);
        """)
        rows = cursor.fetchall()
        tim_bertandings = []

        for row in rows:
            tim_bertandings.append(
                {
                'Nama': row[0],
                'Waktu': row[1],
                'Id' : row[2]
            }
            )
        return tim_bertandings