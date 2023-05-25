from django.db import connection
from datetime import datetime
from django.utils import timezone

# Create your models here.
def get_matches():
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
        
    