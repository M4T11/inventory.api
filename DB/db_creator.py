import psycopg2
from config import config

def create_database():
    parameters = config('../database.ini')
    connection_string = f"user={parameters['user']} password={parameters['password']}"
    connection = psycopg2.connect(connection_string)
    cursor = connection.cursor()
    connection.autocommit = True
    sql_query = f"CREATE DATABASE {parameters['database']}"
    try:
        cursor.execute(sql_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    else:
        connection.autocommit = False


def create_tables():
    commands = (
        """
        CREATE TABLE Locations (
            Location_id SERIAL PRIMARY KEY,
            Name VARCHAR(255) UNIQUE NOT NULL
            )
        """,
        """
        CREATE TABLE Producers (
            Producer_id SERIAL PRIMARY KEY,
            Name VARCHAR (255) NOT NULL
            )
        """,
        """
        CREATE TABLE Categories (
            Category_id SERIAL PRIMARY KEY,
            Name VARCHAR(255) UNIQUE NOT NULL
            )
        """,
        """
        CREATE TABLE EAN_Devices (
            EAN_Device_id SERIAL PRIMARY KEY,
            EAN VARCHAR(255) UNIQUE NOT NULL,
            Category_id SERIAL REFERENCES Categories(Category_id),  
            Producer_id SERIAL REFERENCES Producers(Producer_id),
            Model VARCHAR(255) UNIQUE NOT NULL
            )
        """,
        """
        CREATE TABLE Devices (
            Device_id SERIAL PRIMARY KEY,
            Name VARCHAR(255),
            Serial_number VARCHAR(255),
            Description VARCHAR(10000),
            EAN_Device_id SERIAL REFERENCES EAN_Devices(EAN_Device_id),
            Location_id SERIAL REFERENCES Locations(Location_id),
            Quantity INT NOT NULL,
            Condition VARCHAR(255) NOT NULL,
            Status VARCHAR(255) NOT NULL,
            Date_added DATE NOT NULL,
            QR_code VARCHAR(255) NOT NULL,
            Returned BOOLEAN NOT NULL DEFAULT FALSE
            )
        """,
        # """
        # CREATE TABLE Users (
        #     User_id SERIAL PRIMARY KEY,
        #     Username VARCHAR(255) NOT NULL,
        #     Password VARCHAR(255) NOT NULL,
        #     Email VARCHAR (255) NOT NULL
        #     )
        # """,
        """
        CREATE TABLE Device_histories (
            History_id SERIAL PRIMARY KEY,
            Event VARCHAR(255) NOT NULL,
            Device_id SERIAL REFERENCES Devices(Device_id),
            Date TIMESTAMP NOT NULL
            
            )
        """,
    )
    # jako ostatnie w device_histories User_id SERIAL REFERENCES Users(User_id)

    connection = None
    try:
        parameters = config('../database.ini')
        connection = psycopg2.connect(**parameters)
        cursor = connection.cursor()
        for command in commands:
            cursor.execute(command)
        cursor.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__=='__main__':
    create_database()
    create_tables()
