import sqlite3
connection = sqlite3.connect("projects.db")
cursor = connection.cursor()
# cursor.execute("""
#     CREATE TABLE projects
# 	(EPC TEXT PRIMARY KEY, Category TEXT, Read_Count INTEGER, Last_Read_From TEXT, First_Seen TEXT, Last_Seen TEXT, Time_Since_Last_Seen INTEGER, Last_RSSI INTEGER, RSSI_Avg INTEGER, RSSI_Max INTEGER, RSSI_Min INTEGER, Power INTEGER, Phase_Angle INTEGER, Doppler_Freq INTEGER)
# """)
cursor.execute("DROP TABLE IF EXISTS projects")
cursor.execute("""
    CREATE TABLE projects
    (EPC TEXT PRIMARY KEY, Category TEXT, Read_Count INTEGER, Last_Read_From TEXT, First_Seen TEXT, Last_Seen TEXT, Time_Since_Last_Seen INTEGER, Last_RSSI INTEGER, RSSI_Avg INTEGER, RSSI_Max INTEGER, RSSI_Min INTEGER, Power INTEGER, Phase_Angle INTEGER, Doppler_Freq INTEGER)
""")

cursor.execute("""INSERT INTO projects VALUES 
	('912391239123912391239123', 'Classic', 0, '127.0.0.1', '2022-01-01 12:00:00.001', '2022-01-02 12:00:00.001', 2678400, -50.30, -48.8, -45.2, -54.6, 30.00, NULL, NULL),
	('845684568456845684568456', 'Class 1', 1, '127.0.0.1', '2022-02-01 3:00:00.001', '2022-02-02 12:00:00.001', 2678400, -50.30, -48.8, -45.2, -54.6, 30.00, NULL, NULL),
	('789078907890789078907890', '18000-6C', 0, '127.0.0.1', '2022-02-01 5:00:00.001', '2022-02-03 12:00:00.001', 2764800, -50.30, -48.8, -45.2, -54.6, 30.00, NULL, NULL)
""")
connection.commit()
