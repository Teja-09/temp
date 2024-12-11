from flask import Flask, render_template, request, redirect, flash, url_for
import oracledb
 
app = Flask(__name__)
 
d = r"C:\oracle\instantclient_23_6"
oracledb.init_oracle_client(lib_dir=d)
print(oracledb.clientversion())
 
def get_db_connection():
    dsn_t = oracledb.makedsn('navydb.artg.arizona.edu', 1521, 'ORCL')
    connection = oracledb.connect(user="mis531groupS1G", password="hMkAdq?t72+/,0Y", dsn=dsn_t, disable_oob=True)
    return connection


@app.route('/')
def index():
    return render_template('index.html', loginStatus = False)

# CUSTOMERS
@app.route('/customers')
def customers():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM CUSTOMERS order by CustomerID")
        custDetails = cursor.fetchall()
    finally:
        # Close the cursor and connection in a finally block
        cursor.close()
        connection.close()
    return render_template('customers.html', customers = custDetails)


@app.route('/insertCustomers', methods=['POST'])
def insertCustomers():
    connection = get_db_connection()
    name = request.form['name'].strip()
    street = request.form['street'].strip()
    city = request.form['city'].strip()
    zipcode = request.form['zipcode'].strip()
    email = request.form['email'].strip()

    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO CUSTOMERS (customer_name, customer_street, customer_city, customer_zip, customer_email) VALUES (:name, :street, :city, :zipcode, :email)", name = name, street = street, city = city, zipcode = zipcode, email = email)
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('customers'))


@app.route('/updateCustomers', methods=['POST'])
def updateCustomers():
    connection = get_db_connection()
    custID = request.form['custID'].strip()
    name = request.form['name'].strip()
    street = request.form['street'].strip()
    city = request.form['city'].strip()
    zipcode = request.form['zipcode'].strip()
    email = request.form['email'].strip()

    colNames = ["customer_name", "customer_street", "customer_city", "customer_zip", "customer_email"]
    colValues = [name, street, city, zipcode, email]
    try:
        cursor = connection.cursor()
        for index in range(len(colValues)):
            if colValues[index] != "":
                sqlQuery = "UPDATE CUSTOMERS SET " + colNames[index] + " = :colValue WHERE CUSTOMERID = :custID"
                cursor.execute(sqlQuery, colValue = colValues[index], custID = custID)

    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()
    

    return redirect(url_for('customers'))


@app.route('/deleteCustomers', methods=['POST'])
def deleteCustomers():
    connection = get_db_connection()
    custID = request.form['custID'].strip()

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM  CUSTOMERS WHERE customerid = :custID", custID = custID)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('customers'))

# ==================================================================================================================================================
# Employees
@app.route('/employees')
def employees():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM EMPLOYEES order by EMPLOYEEID")
        empDetails = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('employees.html', empDetails=empDetails) 

@app.route('/insertEmployees', methods=['POST'])
def insertEmployees():
    connection = get_db_connection()
    name = request.form['name'].strip()
    email = request.form['email'].strip()
    city = request.form['city'].strip()
    state = request.form['state'].strip()
    zipcode = request.form['zipcode'].strip()

    try:
        cursor = connection.cursor()        
        cursor.execute("INSERT INTO EMPLOYEES (employee_name, employee_email, employee_city, employee_state, employee_zip) VALUES (:name, :email, :city, :state, :zip)", 
                       name = name, email = email, city = city, state = state, zip = zipcode)
        
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('employees'))

@app.route('/updateEmployees', methods=['POST'])
def updateEmployees():
    connection = get_db_connection()
    empID = request.form['empID'].strip()
    name = request.form['name'].strip()
    email = request.form['email'].strip()
    city = request.form['city'].strip()
    state = request.form['state'].strip()
    zipcode = request.form['zipcode'].strip()

    colNames = ["employeeid", "employee_name", "employee_email", "employee_city", "employee_state", "employee_zip"]
    colValues = [empID, name, email, city, state, zipcode]
    try:
        cursor = connection.cursor()
        for index in range(len(colValues)):
            if colValues[index] != "":
                sqlQuery = "UPDATE EMPLOYEES SET " + colNames[index] + " = :colValue WHERE employeeid = :empID"
                cursor.execute(sqlQuery, colValue = colValues[index], empID = empID)

    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()
    return redirect(url_for('employees'))


@app.route('/deleteEmployees', methods=['POST'])
def deleteEmployees():
    connection = get_db_connection()
    empID = request.form['empID'].strip()

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM EMPLOYEES WHERE employeeid = :empID", empID = empID)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('employees'))

# ===========================================================================================================================
# G1 Supply Details
@app.route('/spawnSupplier')
def spawnSupplier():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM G1SPAWN_SUPPLIERS order by SUPPLIERID")
        spawnSupplierDetails = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('spawnSupply.html', spawnSupplierDetails=spawnSupplierDetails) 

@app.route('/insertSpawnSupplier', methods=['POST'])
def insertSpawnSupplier():
    connection = get_db_connection()
    name = request.form['name'].strip()
    street = request.form['street'].strip()
    city = request.form['city'].strip()
    zipcode = request.form['zip'].strip()

    try:
        cursor = connection.cursor()        
        cursor.execute("INSERT INTO G1SPAWN_SUPPLIERS (supplier_name, supplier_street, supplier_city, supplier_zip) VALUES (:name, :street, :city, :zip)", 
                       name = name, street = street, city = city, zip = zipcode)
        
    finally:
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('spawnSupplier'))

@app.route('/updateSpawnSupplier', methods=['POST'])
def updateSpawnSupplier():
    connection = get_db_connection()
    supplierid = request.form['id'].strip()
    name = request.form['name'].strip()
    street = request.form['street'].strip()
    city = request.form['city'].strip()
    zipcode = request.form['zip'].strip()

    colNames = ["supplierid", "supplier_name", "supplier_street", "supplier_city", "supplier_zip"]
    colValues = [supplierid, name, street, city, zipcode]
    try:
        cursor = connection.cursor()
        for index in range(len(colValues)):
            if colValues[index] != "":
                sqlQuery = "UPDATE G1SPAWN_SUPPLIERS SET " + colNames[index] + " = :colValue WHERE supplierid = :supid"
                cursor.execute(sqlQuery, colValue = colValues[index], supid = supplierid)

    finally:
        connection.commit()
        cursor.close()
        connection.close()
    return redirect(url_for('spawnSupplier'))


@app.route('/deleteSpawnSupplier', methods=['POST'])
def deleteSpawnSupplier():
    connection = get_db_connection()
    supplierid = request.form['id'].strip()

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM G1SPAWN_SUPPLIERS WHERE supplierid = :supplierid", supplierid = supplierid)
    finally:
        # Close the cursor and connection in a finally block
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('spawnSupplier'))


# =================================================================================================================================================
# Material Supplier Details
@app.route('/materialSupplier')
def materialSupplier():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM SUBSTRATE_MATERIAL_SUPPLIER order by SUBSTRATE_SUPPLIERID")
        materialSupplierDetails = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('materialSupply.html', materialSupplierDetails=materialSupplierDetails) 

@app.route('/insertMaterialSupplier', methods=['POST'])
def insertMaterialSupplier():
    connection = get_db_connection()
    name = request.form['name'].strip()
    street = request.form['street'].strip()
    city = request.form['city'].strip()
    zipcode = request.form['zip'].strip()

    try:
        cursor = connection.cursor()        
        cursor.execute("INSERT INTO SUBSTRATE_MATERIAL_SUPPLIER (SUBSTRATE_supplier_name, SUBSTRATE_supplier_street, SUBSTRATE_supplier_city, SUBSTRATE_supplier_zip) VALUES (:name, :street, :city, :zip)", 
                       name = name, street = street, city = city, zip = zipcode)
        
    finally:
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('materialSupplier'))

@app.route('/updateMaterialSupplier', methods=['POST'])
def updateMaterialSupplier():
    connection = get_db_connection()
    supplierid = request.form['id'].strip()
    name = request.form['name'].strip()
    street = request.form['street'].strip()
    city = request.form['city'].strip()
    zipcode = request.form['zip'].strip()

    colNames = ["substrate_supplierid", "substrate_supplier_name", "substrate_supplier_street", "substrate_supplier_city", "substrate_supplier_zip"]
    colValues = [supplierid, name, street, city, zipcode]
    try:
        cursor = connection.cursor()
        for index in range(len(colValues)):
            if colValues[index] != "":
                sqlQuery = "UPDATE SUBSTRATE_MATERIAL_SUPPLIER SET " + colNames[index] + " = :colValue WHERE substrate_supplierid = :supid"
                cursor.execute(sqlQuery, colValue = colValues[index], supid = supplierid)

    finally:
        connection.commit()
        cursor.close()
        connection.close()
    return redirect(url_for('materialSupplier'))


@app.route('/deleteMaterialSupplier', methods=['POST'])
def deleteMaterialSupplier():
    connection = get_db_connection()
    supplierid = request.form['id'].strip()

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM SUBSTRATE_MATERIAL_SUPPLIER WHERE substrate_supplierid = :supplierid", supplierid = supplierid)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

    return redirect(url_for('materialSupplier'))


# =================================================================================================================================================
# Scenarios
@app.route('/scenarios')
def scenarios():
    return render_template('scenario.html')

@app.route('/scenario1')
def scenario1():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
                SELECT 
                    gsd.supply_specie_name AS Species,
                    s.supplier_name AS Supplier_Name,
                    s.supplier_city AS Supplier_City,
                    s.supplier_zip AS Supplier_Zip,
                    COUNT(DISTINCT gsd.supply_supplierID) OVER (PARTITION BY gsd.supply_specie_name) AS Supplier_Count
                FROM G1SUPPLY_DETAILS gsd
                JOIN G1SPAWN_SUPPLIERS s 
                    ON gsd.supply_supplierID = s.supplierID
                WHERE gsd.supply_specie_name IN (
                    SELECT gsd_inner.supply_specie_name
                    FROM G1SUPPLY_DETAILS gsd_inner
                    GROUP BY gsd_inner.supply_specie_name
                    HAVING COUNT(DISTINCT gsd_inner.supply_supplierID) >=1
                )
                ORDER BY Supplier_Count desc
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario1.html', queryOutput=queryOutput) 


@app.route('/scenario2')
def scenario2():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
                SELECT 
                    c.customer_name AS Customer,
                    c.customer_email AS Email,
                    REPLACE(p.product_name, ' - Pack', '') AS Product,
                    EXTRACT(YEAR FROM od.order_date) AS Year,
                    'Q' || CEIL(EXTRACT(MONTH FROM od.order_date) / 3) AS Quarter,
                    SUM(od.order_quantity) AS Total_Blocks
                FROM ORDER_DETAILS od
                JOIN CUSTOMERS c 
                    ON od.order_customerID = c.customerID
                JOIN PRODUCTS p 
                    ON od.order_productID = p.productID
                GROUP BY 
                    c.customer_name, 
                    c.customer_email, 
                    REPLACE(p.product_name, ' - Pack', ''), 
                    EXTRACT(YEAR FROM od.order_date), 
                    CEIL(EXTRACT(MONTH FROM od.order_date) / 3)
                ORDER BY Year, Quarter, Customer, Product
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario2.html', queryOutput=queryOutput) 

@app.route('/scenario3')
def scenario3():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
                SELECT 
                    rmi.inventory_item_name AS Item_Name,
                    rmi.inventory_quantity AS Available_Pounds,
                    TO_CHAR(rmi.inventory_expiry_date, 'YYYY-MM-DD') AS Expiry_Date,
                    'Raw Material' AS Type
                FROM RAW_MATERIAL_INVENTORY rmi

                UNION ALL

                -- Products Inventory
                SELECT 
                    REPLACE(p.product_name, ' - Pack', '') AS Item_Name,
                    p.product_quantity_in_stock AS Available_Pounds,
                    TO_CHAR(p.product_expiry_date, 'YYYY-MM-DD') AS Expiry_Date,
                    'Product' AS Type
                FROM PRODUCTS p

                ORDER BY Type, Item_Name
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario3.html', queryOutput=queryOutput)


@app.route('/scenario4')
def scenario4():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
                SELECT 
                    li.lab_inoculation_labNum AS Location,
                    'Lab' AS Type,
                    SUM(li.lab_inoculation_col_roomID) AS Current_Capacity_Blocks
                FROM LAB_INOCULATION li
                GROUP BY li.lab_inoculation_labNum

                UNION ALL

                -- Grow Rooms Current Capacity in Blocks
                SELECT 
                    c.colonization_roomID AS Location,
                    'Grow Room' AS Type,
                    SUM(c.colonization_placementID) AS Current_Capacity_Blocks
                FROM COLONIZATION c
                GROUP BY c.colonization_roomID

                UNION ALL

                -- Fruiting Chambers Current Capacity in Blocks
                SELECT 
                    fc.fruiting_chamberID AS Location,
                    'Fruiting Chamber' AS Type,
                    SUM(fc.fruiting_placementID) AS Current_Capacity_Blocks
                FROM FRUITING_CHAMBER fc
                GROUP BY fc.fruiting_chamberID

                ORDER BY Type, Location
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario4.html', queryOutput=queryOutput)

@app.route('/scenario5')
def scenario5():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
               WITH Weekly_Production AS (
                    SELECT
                        hd.harvest_specie_name AS Mushroom_Type,
                        EXTRACT(YEAR FROM hd.harvest_date) AS Year,
                        TO_NUMBER(TO_CHAR(hd.harvest_date, 'IW')) AS Week_Number,
                        MIN(TO_CHAR(hd.harvest_date, 'DDD')) || '-' || MAX(TO_CHAR(hd.harvest_date, 'DDD')) AS Julian_Day_Range,
                        SUM(hd.harvest_quantity) AS Production_Amount
                    FROM HARVEST_DETAILS hd
                    WHERE hd.harvest_date BETWEEN TO_DATE('2023-11-01', 'YYYY-MM-DD') AND TO_DATE('2024-01-14', 'YYYY-MM-DD')
                    GROUP BY hd.harvest_specie_name, EXTRACT(YEAR FROM hd.harvest_date), TO_NUMBER(TO_CHAR(hd.harvest_date, 'IW'))
                ),
                All_Weeks AS (
                    SELECT
                        DISTINCT EXTRACT(YEAR FROM hd.harvest_date) AS Year,
                        TO_NUMBER(TO_CHAR(hd.harvest_date, 'IW')) AS Week_Number,
                        MIN(TO_CHAR(hd.harvest_date, 'DDD')) || '-' || MAX(TO_CHAR(hd.harvest_date, 'DDD')) AS Julian_Day_Range
                    FROM HARVEST_DETAILS hd
                    WHERE hd.harvest_date BETWEEN TO_DATE('2023-11-01', 'YYYY-MM-DD') AND TO_DATE('2024-01-14', 'YYYY-MM-DD')
                    GROUP BY EXTRACT(YEAR FROM hd.harvest_date), TO_NUMBER(TO_CHAR(hd.harvest_date, 'IW'))
                ),
                Weekly_Goals AS (
                    SELECT
                        aw.Year,
                        aw.Week_Number,
                        aw.Julian_Day_Range,
                        240 AS Production_Goal
                    FROM All_Weeks aw
                )
                SELECT
                    COALESCE(wp.Mushroom_Type, 'No Harvest') AS Mushroom_Type,
                    wg.Year,
                    wg.Week_Number,
                    wg.Julian_Day_Range,
                    COALESCE(wp.Production_Amount, 0) AS Total_Production,
                    wg.Production_Goal,
                    (wg.Production_Goal - COALESCE(wp.Production_Amount, 0)) AS Production_Shortfall
                FROM Weekly_Goals wg
                LEFT JOIN Weekly_Production wp 
                    ON wg.Year = wp.Year AND wg.Week_Number = wp                                                                                                                                                .Week_Number
                ORDER BY wg.Year, wg.Week_Number, wp.Mushroom_Type
                """
        cursor.execute(sqlQuery)
        queryOutputBike = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario5.html', queryOutput=queryOutputBike)

@app.route('/scenario6')
def scenario6():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
               SELECT 
                    li.lab_inoculation_labNum AS Lab_Number,
                    ms.mushroom_specieID AS Species_ID,
                    ms.mushroom_specie_common_name AS Species,
                    li.lab_inoculation_temp AS Temperature,
                    li.lab_inoculation_humidity AS Humidity,
                    gbd.batch_quantity AS Quantity_Blocks,
                    gbd.batch_date AS Inoculation_Date
                FROM LAB_INOCULATION li
                JOIN G1BATCH_DETAILS gbd 
                    ON li.lab_inoculation_labNum = gbd.batch_lab_num
                JOIN G1SPAWN gs
                    ON gbd.batch_spawnID = gs.spawnID
                JOIN MUSHROOM_SPECIES ms
                    ON gs.spawn_specieID = ms.mushroom_specieID
                ORDER BY li.lab_inoculation_labNum, ms.mushroom_specie_common_name, gbd.batch_date
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario6.html', queryOutput=queryOutput)


@app.route('/scenario7')
def scenario7():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
              SELECT 
                    g2b.g2BID AS G2_Batch_ID,
                    g2b.g2spawn_batch_date AS Batch_Date,
                    ms.mushroom_specieID AS Species_ID,
                    ms.mushroom_specie_common_name AS Species,
                    g2b.g2spawn_batch_quantity AS Quantity_Blocks,
                    i.incubation_roomID AS Incubation_Room_ID,
                    i.incubation_start_date AS Incubation_Start_Date,
                    i.incubation_temp AS Temperature,
                    i.incubation_humidity AS Humidity
                FROM G2SPAWN_BATCH g2b
                JOIN G1SPAWN gs
                    ON g2b.g1SpawnID = gs.spawnID
                JOIN MUSHROOM_SPECIES ms
                    ON gs.spawn_specieID = ms.mushroom_specieID
                JOIN INCUBATION i
                    ON g2b.col_roomID = i.incubation_roomID
                ORDER BY g2b.g2spawn_batch_date, ms.mushroom_specie_common_name
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario7.html', queryOutput=queryOutput)

# Scenario 8
@app.route('/scenario8')
def scenario8():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
               SELECT 
                    ct.cleaning_taskID AS Task_ID,
                    TO_CHAR(ct.cleaning_task_date, 'YYYY-MM-DD') AS Scheduled_Date,
                    ct.cleaning_task_details AS Details,
                    e.employeeID AS Assigned_Employee,
                    e.employee_email AS Employee_Email
                FROM CLEANING_TASKS ct
                JOIN EMPLOYEES e 
                    ON ct.cleaning_task_employeeID = e.employeeID
                WHERE ct.cleaning_task_details is not NULL
                ORDER BY ct.cleaning_task_date, e.employeeID
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario8.html', queryOutput=queryOutput)

@app.route('/scenario9')
def scenario9():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
               SELECT 
                    e.employeeID AS Employee_ID,
                    e.employee_name AS Employee_Name,
                    e.employee_email AS Email,
                    e.employee_city AS City,
                    e.employee_state AS State,
                    e.employee_zip AS ZIP,
                    CASE
                        WHEN ls.lab_staff_employeeID IS NOT NULL THEN 'Lab Staff'
                        WHEN asf.admin_staff_employeeID IS NOT NULL THEN 'Admin Staff'
                        ELSE 'Other'
                    END AS Role
                FROM EMPLOYEES e
                LEFT JOIN LAB_STAFF ls
                    ON e.employeeID = ls.lab_staff_employeeID
                LEFT JOIN ADMIN_STAFF asf
                    ON e.employeeID = asf.admin_staff_employeeID
                WHERE ls.lab_staff_employeeID IS NOT NULL
                OR asf.admin_staff_employeeID IS NOT NULL
                ORDER BY Role, e.employee_name
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario9.html', queryOutput=queryOutput)


@app.route('/scenario10')
def scenario10():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
               SELECT 
                    e.equipmentID AS Equipment_ID,
                    e.equipment_type AS Equipment_Type,
                    e.manufacturer AS Manufacturer,
                    e.supplier_name AS Supplier,
                    md.maintenance_date AS Scheduled_Maintenance_Date,
                    m.maintenance_type AS Maintenance_Type,
                    m.description AS Maintenance_Description,
                    md.maintenance_cost AS Estimated_Cost,
                    md.issue_description AS Issue_Description,
                    md.resolution_status AS Status
                FROM MAINTENANCE_DETAILS md
                JOIN EQUIPMENTS e 
                    ON md.equipmentID = e.equipmentID
                JOIN MAINTENANCE m 
                    ON md.maintenanceID = m.maintenanceID
                WHERE md.resolution_status = 'Completed'
                ORDER BY md.maintenance_date, e.equipment_type
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario10.html', queryOutput=queryOutput)


@app.route('/scenario11')
def scenario11():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        sqlQuery = """
               SELECT 
                    EXTRACT(YEAR FROM gbd.batch_date) AS Year,
                    ms.mushroom_specie_common_name AS Species,
                    SUM(gbd.batch_quantity) AS Total_Cultivated_Quantity
                FROM G1BATCH_DETAILS gbd
                INNER JOIN G1SPAWN gs
                    ON gbd.batch_spawnID = gs.spawnID
                INNER JOIN MUSHROOM_SPECIES ms
                    ON gs.spawn_specieID = ms.mushroom_specieID
                GROUP BY EXTRACT(YEAR FROM gbd.batch_date), ms.mushroom_specie_common_name
                ORDER BY Year, Total_Cultivated_Quantity DESC
                """
        cursor.execute(sqlQuery)
        queryOutput = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    return render_template('scenario11.html', queryOutput=queryOutput)


if __name__ == '__main__':
    app.run(host= '0.0.0.0')