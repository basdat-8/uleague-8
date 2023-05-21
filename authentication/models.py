# models.py
from django.db import connection

def insert_user(
    first_name,
    last_name,
    username,
    email,
    password,
    
)

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

def get_additional_data(id):
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT TM."Nama_Tim", "Universitas" FROM "Tim"
                        JOIN "Tim_Manajer" TM ON "Tim"."Nama_Tim" = TM."Nama_Tim"
                        JOIN "Manajer" M on M."ID_Manajer" = TM."ID_Manajer"
                        WHERE M."ID_Manajer" = %s
                        """, [id])
        rows = cursor.fetchall()
        
        data = []
        
        for row in rows:
            data.append({
                'nama_tim': row[0],
                'universitas': row[1]
            })
            
        return data
