# models.py
from django.db import connection
from django.template.defaultfilters import date, time
import uuid

def insert_user(payload):
    with connection.cursor() as cursor:
        first_name = payload['first-name']
        last_name = payload['last-name']
        phone_number = payload['phone-number']
        address = payload['address']
        email = payload['email']
        password = payload['password']
        status = payload['status']
        role = payload['role']
        jabatan = payload['jabatan']
        
        username = (first_name + '.' + last_name.split(' ')[0]).lower()
        
        cursor.execute("BEGIN;")

        try:
            cursor.execute(
                """
                    INSERT INTO "User_System" ("Username", "Password") VALUES (%s, %s)
                """,
                (username, password)
            )
            
            id_non_pemain = uuid.uuid4()
            
            cursor.execute(
                """
                    INSERT INTO "Non_Pemain" ("ID", "Nama_Depan", "Nama_Belakang", "Nomor_HP", "Email", "Alamat") VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (id_non_pemain, first_name, last_name, phone_number, email, address)
            )
            
            cursor.execute(
                """
                    INSERT INTO "Status_Non_Pemain" ("ID_Non_Pemain", "Status") VALUES (%s, %s)
                """,
                (id_non_pemain, status)
            )
            
            if role == 'PANITIA':
                cursor.execute(
                    """
                        INSERT INTO "Panitia" ("ID_Panitia", "Username", "Jabatan") VALUES (%s, %s, %s)
                    """,
                    (id_non_pemain, username, jabatan)
                )
            elif role == 'MANAJER':
                cursor.execute(
                    """
                        INSERT INTO "Manajer" ("ID_Manajer", "Username") VALUES (%s, %s)
                    """,
                    (id_non_pemain, username)
                )
            elif role == 'PENONTON':
                cursor.execute(
                    """
                        INSERT INTO "Penonton" ("ID_Penonton", "Username") VALUES (%s, %s)
                    """,
                    (id_non_pemain, username)
                )
            
            cursor.execute("COMMIT;")
        except Exception as e:
            cursor.execute('ROLLBACK;')
            raise e
        
        return username


def get_user_by_username(username):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM "User_System" WHERE "Username" = %s', [username])
        row = cursor.fetchone()
        
        if row:
            user_data = {
                'username': row[0],
                'password': row[1],
            }
            return user_data
        else:
            return None
        
def get_user_role(username):
    with connection.cursor() as cursor:
        cursor.execute("""
                    SELECT
                        EXISTS(SELECT 1 FROM "Penonton" WHERE "Username" = %s) AS is_penonton,
                        EXISTS(SELECT 1 FROM "Manajer" WHERE "Username" = %s) AS is_manajer,
                        EXISTS(SELECT 1 FROM "Panitia" WHERE "Username" = %s) AS is_panitia;
                """, [username, username, username])
        return cursor.fetchone()

def get_user_by_role(username, role):
    with connection.cursor() as cursor:
            if role == 'PENONTON':
                cursor.execute("""
                                SELECT "ID", "Nama_Depan", "Nama_Belakang", "Nomor_HP", "Email", "Alamat", "Status" FROM "Penonton"
                                JOIN "Non_Pemain"
                                ON "Penonton"."ID_Penonton" = "Non_Pemain"."ID"
                                JOIN "Status_Non_Pemain"
                                ON "Non_Pemain"."ID" = "Status_Non_Pemain"."ID_Non_Pemain"
                                WHERE "Username" = %s
                               """, [username])
            elif role =='MANAJER':
                cursor.execute("""
                                SELECT "ID", "Nama_Depan", "Nama_Belakang", "Nomor_HP", "Email", "Alamat", "Status" FROM "Manajer"
                                JOIN "Non_Pemain"
                                ON "Manajer"."ID_Manajer" = "Non_Pemain"."ID"
                                JOIN "Status_Non_Pemain"
                                ON "Non_Pemain"."ID" = "Status_Non_Pemain"."ID_Non_Pemain"
                                WHERE "Username" = %s
                               """, [username])
            elif role == 'PANITIA':
                cursor.execute("""
                                SELECT "ID", "Nama_Depan", "Nama_Belakang", "Nomor_HP", "Email", "Alamat", "Status", "Jabatan" FROM "Panitia"
                                JOIN "Non_Pemain"
                                ON "Panitia"."ID_Panitia" = "Non_Pemain"."ID"
                                JOIN "Status_Non_Pemain"
                                ON "Non_Pemain"."ID" = "Status_Non_Pemain"."ID_Non_Pemain"
                                WHERE "Username" = %s
                               """, [username])
            
            row = cursor.fetchone()
            
            user = {
                'id': row[0],
                'nama_depan': row[1],
                'nama_belakang': row[2],
                'nomor_hp': row[3],
                'email': row[4],
                'alamat': row[5],
                'status': row[6],
                'jabatan': row[7] if role == 'PANITIA' else None
            }
            
            return user

def get_additional_data(id, role):
    with connection.cursor() as cursor:
        
        if role == 'MANAJER':
            cursor.execute("""
                SELECT TM."Nama_Tim", "Universitas" FROM "Tim"
                JOIN "Tim_Manajer" TM ON "Tim"."Nama_Tim" = TM."Nama_Tim"
                JOIN "Manajer" M on M."ID_Manajer" = TM."ID_Manajer"
                WHERE M."ID_Manajer" = %s
                """, [id]
            )
        elif role == 'PANITIA':
            cursor.execute("""
               SELECT 
                    "Datetime" AS tanggal_rapat, 
                    S."Nama" AS stadium, 
                    "Manajer_Tim_A" AS manajer_a,
                    "Manajer_Tim_B" AS manajer_b 
                FROM "Rapat"
                JOIN "Pertandingan" P
                    ON "Rapat"."ID_Pertandingan" = P."ID_Pertandingan"
                JOIN "Stadium" S
                    ON S."ID_Stadium" = P."Stadium"
                WHERE 
                    "Rapat"."Perwakilan_Panitia" = %s
                    AND "Datetime" > CURRENT_TIMESTAMP
                """, [id]
            )
        elif role == 'PENONTON':
            cursor.execute("""
                SELECT
                    string_agg("Nama_Tim", ' VS ') AS tim_bertanding,
                    S."Nama" AS nama_stadium,
                    "Start_Datetime"
                FROM "Pembelian_Tiket"
                JOIN "Pertandingan" P
                    ON P."ID_Pertandingan" = "Pembelian_Tiket"."ID_Pertandingan"
                JOIN "Stadium" S
                    ON S."ID_Stadium" = P."Stadium"
                JOIN "Tim_Pertandingan" TP
                    ON P."ID_Pertandingan" = TP."ID_Pertandingan"
                WHERE
                    "ID_Penonton" = %s
                    AND "Start_Datetime" > CURRENT_TIMESTAMP
                GROUP BY "Nomor_Receipt", S."Nama", "Start_Datetime"
                """, [id]
            )
        
        rows = cursor.fetchall()
        
        data = []
        
        for row in rows:
            if role == 'MANAJER':
                data.append({
                    'nama_tim': row[0],
                    'universitas': row[1]
                })
            elif role == 'PENONTON':
                data.append({
                    'tim_bertanding': row[0],
                    'stadium': row[1],
                    'tanggal_bermain': row[2]
                })
            elif role == 'PANITIA':
                cursor.execute("""
                    SELECT "Nama_Tim" FROM "Tim_Manajer" TM
                    JOIN "Manajer" M
                        ON M."ID_Manajer" = TM."ID_Manajer"
                    WHERE M."ID_Manajer" = %s
                    """, [row[2]]
                )
                
                tim_a = cursor.fetchall()[0][0]
                
                cursor.execute("""
                    SELECT "Nama_Tim" FROM "Tim_Manajer" TM
                    JOIN "Manajer" M
                        ON M."ID_Manajer" = TM."ID_Manajer"
                    WHERE M."ID_Manajer" = %s
                    """, [row[3]]
                )
                
                tim_b = cursor.fetchall()[0][0]
                
                formatted_date = date(row[0], "j F Y")
                formatted_time = time(row[0], "H.i")

                formatted_datetime = f"{formatted_date}, {formatted_time}"

                data.append({
                    'tanggal_rapat': formatted_datetime,
                    'stadium': row[1],
                    'tim_a': tim_a,
                    'tim_b': tim_b
                })
            
        return data
    