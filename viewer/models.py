from datetime import datetime
import random
import string
from django.db import connection

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
                    JOIN "Tim_Pertandingan"
                        ON "Pertandingan"."ID_Pertandingan" = "Tim_Pertandingan"."ID_Pertandingan"
                    JOIN "Stadium"
                        ON "Pertandingan"."Stadium" = "Stadium"."ID_Stadium"
            WHERE
                "Start_Datetime" > current_timestamp
            GROUP BY
                "Pertandingan"."ID_Pertandingan",
                "Nama",
                "Start_Datetime",
                "End_Datetime";               
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
                'id': row[0],
                'name': row[1],
                'stadium': row[2],
                'dateTime': dateTime
            })
        
        return matches
    
def buy_ticket(payload, pertandingan_id, penonton_id):
    with connection.cursor() as cursor:
        jenis_tiket = payload['jenis_tiket']
        jenis_pembayaran = payload['pembayaran']
        nmr_receipt = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))
        
        cursor.execute("""
            INSERT INTO "Pembelian_Tiket" (
                "Nomor_Receipt", 
                "ID_Penonton", 
                "ID_Pertandingan", 
                "Jenis_Tiket", 
                "Jenis_Pembayaran"
            ) VALUES (%s, %s, %s, %s, %s)
            """, 
            (nmr_receipt, penonton_id, pertandingan_id, jenis_tiket, jenis_pembayaran)
        )