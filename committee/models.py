from django.db import connection
from datetime import datetime, timedelta
import uuid
from django.utils import timezone

# Create your models here.
def get_unstarted_matches():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                "Pertandingan"."ID_Pertandingan",
                string_agg("Nama_Tim", ' VS '),
                "Nama",
                "Start_Datetime",
                "End_Datetime"
            FROM "Pertandingan"
            LEFT OUTER JOIN "Rapat" R
                ON "Pertandingan"."ID_Pertandingan" = R."ID_Pertandingan"
            JOIN "Tim_Pertandingan"
                ON "Pertandingan"."ID_Pertandingan" = "Tim_Pertandingan"."ID_Pertandingan"
            JOIN "Stadium"
                ON "Pertandingan"."Stadium" = "Stadium"."ID_Stadium"
            WHERE R."ID_Pertandingan" IS NULL
            GROUP BY "Pertandingan"."ID_Pertandingan", "Nama", "Start_Datetime", "End_Datetime";               
        """)
        
        rows = cursor.fetchall()
        
        matches = []
        
        for row in rows:
            dateArr = str(row[3]).split(' ')
            date_object = datetime.strptime(dateArr[0], '%Y-%m-%d')
            date = date_object.strftime('%d %B %Y')
            startTime = dateArr[1]
            endTime = str(row[4]).split(' ')[1]
            dateTime = date + ", " + startTime + " - " + endTime 
            
            matches.append({
                'id_pertandingan': row[0],
                'tim_bertanding': row[1],
                'name': row[2],
                'dateTime': dateTime,
            })
            
            
        return matches

def create_meeting(isi_rapat, pertandingan_id, panitia_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT "ID_Manajer" FROM "Tim"
            JOIN "Tim_Pertandingan" TP on "Tim"."Nama_Tim" = TP."Nama_Tim"
            JOIN "Tim_Manajer" TM on "Tim"."Nama_Tim" = TM."Nama_Tim"
            WHERE "ID_Pertandingan" = %s;
        """, [pertandingan_id])
        
        [result_1, result_2] = cursor.fetchall()
        
        manager_1 = result_1[0]
        manager_2 = result_2[0]
        
        now = timezone.now()

        cursor.execute("""
                INSERT INTO "Rapat" (
                    "ID_Pertandingan", 
                    "Datetime", 
                    "Perwakilan_Panitia", 
                    "Manajer_Tim_A", 
                    "Manajer_Tim_B", 
                    "Isi_Rapat"
                ) VALUES (%s, %s, %s, %s, %s, %s)       
        """, [pertandingan_id, now, panitia_id, manager_1, manager_2, isi_rapat])    
        
def get_matches():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                TP."ID_Pertandingan",
                string_agg("Nama_Tim", ' VS '),
                "Nama",
                "Start_Datetime",
                "End_Datetime",
                "Isi_Rapat",
                string_agg("Skor", '-')
            FROM "Pertandingan"
            LEFT OUTER JOIN "Rapat" R
                ON "Pertandingan"."ID_Pertandingan" = R."ID_Pertandingan"
            JOIN "Tim_Pertandingan" TP
                ON "Pertandingan"."ID_Pertandingan" = TP."ID_Pertandingan"
            JOIN "Stadium"
                ON "Pertandingan"."Stadium" = "Stadium"."ID_Stadium"
            GROUP BY
                TP."ID_Pertandingan",
                "Start_Datetime",
                "End_Datetime",
                "Isi_Rapat",
                "Nama"
            """)
        
        rows = cursor.fetchall()
        
        matches = []
        
        for row in rows:
            dateArr = str(row[3]).split(' ')
            date_object = datetime.strptime(dateArr[0], '%Y-%m-%d')
            date = date_object.strftime('%d %B %Y')
            startTime = dateArr[1]
            endTime = str(row[4]).split(' ')[1]
            dateTime = date + ", " + startTime + " - " + endTime 
            
            [team_1, team_2] = row[1].split('VS')

            winner = None
            
            if row[6] is not None:            
                [str_skor_1, str_skor_2] = row[6].split('-')
                
                skor_1 = int(str_skor_1)
                skor_2 = int(str_skor_2)
                
                if row[5] is None:
                    winner = None
                elif skor_1 > skor_2:
                    winner = team_1
                elif skor_1 < skor_2:
                    winner = team_2
                elif skor_1 == skor_2:
                    winner = "Draw"
                
            now = timezone.now() + timedelta(hours=7)
            
            start_datetime = timezone.make_aware(row[3], timezone.get_current_timezone())
            end_datetime = timezone.make_aware(row[4], timezone.get_current_timezone())
            
            is_the_time = now > start_datetime and now < end_datetime
            
            matches.append({
                'id': row[0],
                'tim_bertanding': row[1],
                'stadium': row[2],
                'dateTime': dateTime,
                'is_meeted': True if row[5] is not None else False,
                "winner": winner,
                "is_the_time": is_the_time,
                "team_1": team_1,
                "team_2": team_2,
            })
        
        return matches

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
