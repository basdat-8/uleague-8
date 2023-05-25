from django.db import connection

# Create your models here.

def get_manager_team(id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM "Tim_Manajer"
            WHERE "ID_Manajer" = %s
        """, [id])
        
        rows = cursor.fetchall()

        return {
            'id': rows[0][0],
            'nama': rows[0][1],
        }

def create_manager_team(payload, id):
    with connection.cursor() as cursor:
        nama_tim = payload['nama']
        universitas = payload['universitas']
        
        cursor.execute("BEGIN")
        
        try:
            cursor.execute(
                """
                    INSERT INTO "Tim" ("Nama_Tim", "Universitas") 
                    VALUES (%s, %s)
                """, 
                [nama_tim, universitas]
            )
            
            cursor.execute(
                """
                    INSERT INTO "Tim_Manajer" ("ID_Manajer", "Nama_Tim") 
                    VALUES (%s, %s)
                """,
                [id, nama_tim]
            )
            
            cursor.execute('COMMIT;')
        except Exception as e:
            cursor.execute('ROLLBACK;')
            raise e
        
def get_coaches_by_team(team_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                P."ID_Pelatih",
                "Nama_Depan" || ' ' || "Nama_Belakang" AS nama_pelatih,
                "Nomor_HP",
                "Email",
                "Alamat",
                string_agg("Spesialisasi", ', ')
            FROM "Tim"
                    JOIN "Pelatih" P
                        ON "Tim"."Nama_Tim" = P."Nama_Tim"
                    JOIN "Non_Pemain" NP
                        ON NP."ID" = P."ID_Pelatih"
                    JOIN "Spesialisasi_Pelatih" SP
                        ON P."ID_Pelatih" = SP."ID_Pelatih"
            WHERE P."Nama_Tim" = %s
            GROUP BY P."ID_Pelatih", nama_pelatih, "Nomor_HP", "Email", "Alamat"
        """, [team_name])
        rows = cursor.fetchall()
        
        coaches = []
        
        for row in rows:
            coaches.append({
                "id": row[0],
                "nama": row[1],
                "nomor_hp": row[2],
                "email": row[3],
                "alamat": row[4],
                "spesialisasi": row[5]
            })
            
        return coaches
    
def get_coaches():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                "Pelatih"."ID_Pelatih",
                "Nama_Depan" || ' ' || "Nama_Belakang" || ' - ' || string_agg("Spesialisasi", ', ')
            FROM "Pelatih"
            JOIN "Non_Pemain" NP
                ON NP."ID" = "Pelatih"."ID_Pelatih"
            JOIN "Spesialisasi_Pelatih" SP
                ON "Pelatih"."ID_Pelatih" = SP."ID_Pelatih"
            WHERE "Nama_Tim" IS NULL
            GROUP BY "Pelatih"."ID_Pelatih", "Nama_Depan", "Nama_Belakang"
        """)
        
        rows = cursor.fetchall()
        
        coaches = []
        
        for row in rows:
            coaches.append({
                "id": row[0],
                "nama": row[1],
            })
        
        return coaches

def add_coach(pelatih_id, nama_tim):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                UPDATE "Pelatih"
                SET "Nama_Tim" = %s
                WHERE "ID_Pelatih" = %s
            """, 
            [nama_tim, pelatih_id]
        )

def remove_coach(pelatih_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                UPDATE "Pelatih"
                SET "Nama_Tim" = NULL
                WHERE "ID_Pelatih" = %s
            """, 
            [pelatih_id]
        )
        
def get_players_by_team(nama_tim):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT
                    "ID_Pemain",
                    "Nama_Depan" || ' ' || "Nama_Belakang",
                    "Nomor_HP",
                    "Tgl_Lahir",
                    "Is_Captain",
                    "Posisi",
                    "NPM",
                    "Jenjang"
                FROM "Pemain"
                JOIN "Tim" T
                    ON T."Nama_Tim" = "Pemain"."Nama_Tim"
                WHERE T."Nama_Tim" = %s  
            """, 
            [nama_tim]
        )
        
        rows = cursor.fetchall()
        
        players = []
        
        for row in rows:
            players.append({
                "id": row[0],
                "nama": row[1],
                "nomor_hp": row[2],
                "tgl_lahir": row[3],
                "is_captain": row[4],
                "posisi": row[5],
                "npm": row[6],
                "jenjang": row[7]
            })
            
        return players

def promote_player(id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                UPDATE "Pemain"
                SET "Is_Captain" = 'True'
                WHERE "ID_Pemain" = %s
            """,
            [id]
        )
        
def remove_player(id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                UPDATE "Pemain"
                SET "Nama_Tim" = NULL
                WHERE "ID_Pemain" = %s
            """, 
            [id]
        )    

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
    
def add_player(pemain_id, nama_tim):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                UPDATE "Pemain"
                SET "Nama_Tim" = %s
                WHERE "ID_Pemain" = %s
            """, 
            [nama_tim, pemain_id]
        )
        
def get_stadiums():
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT "ID_Stadium", "Nama" FROM "Stadium"
            """
        )
        
        rows = cursor.fetchall()
        
        stadiums = []
        
        for row in rows:
            stadiums.append({
                "id": row[0],
                "nama": row[1]
            })
            
        return stadiums
    
def rent_stadium(payload, manajer_id):
    stadium_id = payload['stadium_id']
    start_date = payload['start_date']
    end_date = payload['end_date']
    
    with connection.cursor() as cursor:
        cursor.execute(
            """
                INSERT INTO "Peminjaman" ("ID_Manajer", "Start_Datetime", "End_Datetime", "ID_Stadium")
                VALUES (%s, %s, %s, %s)
            """, 
            [manajer_id, start_date, end_date, stadium_id]
        )
        
def get_rented_stadium(manajer_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT "Nama", "Start_Datetime" || ' - ' || "End_Datetime" FROM "Peminjaman"
                JOIN "Stadium" S
                    ON S."ID_Stadium" = "Peminjaman"."ID_Stadium"
                WHERE
                    "ID_Manajer" = %s
            """, 
            [manajer_id]
        )
        
        rows = cursor.fetchall()
        
        stadiums = []
        
        for row in rows:
            stadiums.append({
                "name": row[0],
                "date": row[1]
            })
            
        return stadiums