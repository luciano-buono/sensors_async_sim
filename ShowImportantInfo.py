import sqlite3
import time;
import matplotlib.pyplot as plt
import datetime

db_name = 'D:\Descargas\Facultad\Base de DAtos\TP2\sensors_async_sim\iot-sqlite.db'
conn = sqlite3.connect(db_name)
cur = conn.cursor()


# -- 6.1 Obtenerelvalorpromediodealgúnsensordetemp eratura.
cur.execute('select AVG(value) FROM(table_Terrazatemperatura)')
aux=cur.fetchone()
print ("1. Temperatura promedio de un sensor (Terraza): "+str(aux[0])+"ºC" )

# -- 6.2 Obtenerelvalorpromediodeto doslossensoresdetemp eratura
cur.execute('SELECT AVG(value) FROM (SELECT value FROM table_Terrazatemperatura UNION SELECT value FROM table_Jardintemperatura UNION SELECT value FROM table_Patiotemperatura)')
aux= cur.fetchone()
print("2. Temperatura promedio de todos los sensores: "+str(aux[0])+"ºC" )

# --6.3 Obtenerelvalorpromediodelúltimodíadeto doslossensoresdetemp eratura.
# --Agarro el timestamp del ultimo elemento(ultimo del dia 3)
cur.execute('SELECT timestamp FROM table_Terrazatemperatura order by timestamp desc limit 1')
aux1= cur.fetchone()
#Le resto al ultimo elemento 64800. de esta forma me aseguro de solo agarrar los elementos del ultimo dia
cur.execute('SELECT AVG(value) FROM (SELECT value,timestamp FROM table_Terrazatemperatura UNION SELECT value,timestamp FROM table_Jardintemperatura UNION SELECT value,timestamp FROM table_Patiotemperatura) WHERE timestamp > ('+str(aux1[0])+' -86400)')
aux= cur.fetchone()
print("3. El valor promedio de temperatura de todos los sensores en el ultimo dia es: "+str(aux1[0])+"ºC")

#--6.4 Obtenerlafechadelmomentomáscalurosodelacasa.(Lamáximalecturadealgunodelossensoresdetemp eratura)
cur.execute('SELECT MAX(value), timestamp FROM (SELECT value,timestamp FROM table_Terrazatemperatura UNION SELECT value,timestamp FROM table_Jardintemperatura UNION SELECT value,timestamp FROM table_Patiotemperatura) ')
aux= cur.fetchone()
#Epoch a tiempo actual
maxTempTime = time.asctime( time.localtime(aux[1] ) )
print("4. El valor maximo de temp de todos los sensores fue: "+str(aux[0]) +"ºC y sucedio: "+maxTempTime)


##Ej 8
#Todos los valores de la terraza durante los 3 dias
cur.execute('select value,timestamp FROM(table_Terrazatemperatura) order by timestamp asc')
plotdata = cur.fetchall()
y_val = [y[0] for y in plotdata]
x_val = [datetime.datetime.utcfromtimestamp( x[1] ).strftime('%Y-%m-%d %H:%M:%S') for x in plotdata]

#Todos los valores del jardin durante los 3 dias
cur.execute('select value,timestamp FROM(table_Jardintemperatura) order by timestamp asc')
plotdata = cur.fetchall()
y_val2 = [y[0] for y in plotdata]
x_val2 = [datetime.datetime.utcfromtimestamp( x[1] ).strftime('%Y-%m-%d %H:%M:%S') for x in plotdata]

#Todos los valores del patio durante los 3 dias
cur.execute('select value,timestamp FROM(table_Patiotemperatura) order by timestamp asc')
plotdata = cur.fetchall()
y_val3 = [y[0] for y in plotdata]
x_val3 = [datetime.datetime.utcfromtimestamp( x[1] ).strftime('%Y-%m-%d %H:%M:%S') for x in plotdata]



plt.plot(x_val,y_val)
plt.plot(x_val,y_val,'or')
plt.title('Sensor Terraza Día 1 a 3')
plt.xlabel('Fecha')
plt.ylabel('Temperatura [ºC]')
plt.show()

plt.plot(x_val2,y_val2)
plt.plot(x_val2,y_val2,'or')
plt.title('Sensor Jardin Día 1 a 3')
plt.xlabel('Fecha')
plt.ylabel('Temperatura [ºC]')
plt.show()

plt.plot(x_val3,y_val3)
plt.plot(x_val3,y_val3,'or')
plt.title('Sensor Patio Día 1 a 3')
plt.xlabel('Fecha')
plt.ylabel('Temperatura [ºC]')
plt.show()


#Cierro DB
cur.close()
conn.close()





