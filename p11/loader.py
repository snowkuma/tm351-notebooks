import psycopg2 as pg
from sqlalchemy import create_engine
from pandas import read_sql as psql

def runPGquerydfd(query,
               dbname='tm351test',
               host='localhost', port=5432,
               user='test', password='test'):
    ''' Run a query on the specified database and return the result as a pandas dataframe '''
    conn = pg.connect(dbname=dbname, host=host, user=user, password=password, port=port)
    df=psql(query,conn)
    conn.close()
    return df


def showPGtables(dbname='tm351test',
                 host='localhost', port=5432,
                 user='test', password='test',
                 tableowner=None):
    ''' Display the public database tables '''
    q="SELECT tablename, tableowner FROM pg_catalog.pg_tables WHERE schemaname='public'"
    df=runPGquerydf(query,dbname=dbname,host=host, port=port,user=user, password=password)
    return df

    
def showPGconns(db=None,
                dbname='tm351test',
                host='localhost', port=5432,
                user='test', password='test'):
    ''' List current connections, optionally to a specified database '''
    if db is not None:
        query="SELECT datname,pid,usename FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname='${}';".format(db)
    else:
        query="SELECT datname,pid,usename FROM pg_stat_activity WHERE pid <> pg_backend_pid()"
    df=runPGquerydf(query,dbname=dbname,host=host, port=port,user=user, password=password)
    return df
    
    
def showPGdbs(dbname='tm351test',
                 host='localhost', port=5432,
                 user='test', password='test'):
    ''' List the user created databases '''
    q="SELECT datname FROM pg_database WHERE datistemplate = false;"
    df=runPGquerydf(query,dbname=dbname,host=host, port=port,user=user, password=password)
    return df
    

def clearConnections(db,
                     dbname='tm351test',
                     host='localhost', port=5432,
                     user='test', password='test'):
    ''' Clear all connections associated with a particular database '''

    engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{dbname}".format(dbname=dbname,
                                                                                          host=host, port=port,
                                                                                          user=user, password=password))
    conn = engine.connect()
    
    #Look for a database of the required name
    q="SELECT datname FROM pg_database WHERE datname='{db}'".format(db=db)
    dbs=psql(q,conn)
    #Return silently if it doesn't exist
    if len(dbs)==0: return
    
    #Check for connections to that database
    q="SELECT pid FROM pg_stat_activity WHERE pid <> pg_backend_pid() AND datname='{db}';".format(db=db)
    openconns=psql(q,conn)
    #Delete any outstanding connections to that database
    if len(openconns):
        for openconn in openconns['pid'].tolist():
            conn.execute("SELECT pg_terminate_backend({oc});".format(oc=openconn))
    conn.close()


def postgres_csv_loader(filepath, table=None,
                        dbname='tm351test',
                        host='localhost', port=5432,
                        user='test', password='test',
                        sep='\t'):
    ''' Load the contents of a tabular data file into a pre-existing postgres database table;
        If a table is not specified, the table will be named based on the filename, eg TABLENAME.suffix '''
    
    #If the database table to be usd has the same name as used in the datafile,
    #allow it to be extracted automatically
    if table is None: table=filepath.split('/')[-1].split('.')[0]
    print('Populating {table} using data from {filepath}'.format(table=table,filepath=filepath))
    
    # open a connection to the PostgreSQL database tm351test
    conn = pg.connect(dbname=dbname, host=host, user=user, password=password, port=port)
    # create a cursor
    c = conn.cursor()
    # open datafile
    io = open(filepath, 'r')
    # execute the PostgreSQL copy command
    c.copy_from(io, table, sep=sep)
    # close datafile
    io.close()
    # commit transaction
    conn.commit()
    # close cursor
    c.close()
    # close database connection
    conn.close()
    
def postgres_table_create_and_load(query,filepath, table=None,
                        dbname='tm351test',
                        host='localhost', port=5432,
                        user='test', password='test',
                        sep='\t'):
    ''' Create a table when passed the table creation statement as 'query' then load in the data '''
    engine = create_engine("postgresql://{u}:{pwd}@{h}:{port}/{db}".format(u=user,
                                                                           pwd = password,
                                                                           h=host,
                                                                           port=port,
                                                                           db=dbname
                                                                          ))
    engine.execute(query)

    postgres_csv_loader(filepath=filepath, table=table,
                        dbname=dbname,
                        host=host, port=port,
                        user=user, password=password,
                        sep=sep)

def postgres_housekeeping(dbs=['movies','doctors','books','references'],
                          dbname='tm351test',
                          host='localhost', port=5432,
                          user='test', password='test'):
    ''' Drop all the tables associated with a particular activity '''
    
    if dbs in ['movies','doctors','books','references']:
        dbs = [dbs]
    
    dropper={}
    
    dropper['books']='''
    DROP TABLE IF EXISTS book_authors CASCADE;
    DROP TABLE IF EXISTS author CASCADE;
    DROP TABLE IF EXISTS books_purchased CASCADE;
    DROP TABLE IF EXISTS order_item_book CASCADE;
    DROP TABLE IF EXISTS order_customer CASCADE;
    DROP TABLE IF EXISTS order_item CASCADE;
    DROP TABLE IF EXISTS book CASCADE;
    DROP TABLE IF EXISTS orders CASCADE;
    DROP TABLE IF EXISTS customer CASCADE;
    '''
    
    dropper['movies']='''
    DROP TABLE IF EXISTS movie_genres_list CASCADE;
    DROP TABLE IF EXISTS movie_genres_array CASCADE;
    DROP TABLE IF EXISTS movie_actor CASCADE;
    DROP TABLE IF EXISTS movie_country CASCADE;
    DROP TABLE IF EXISTS movie_director CASCADE;
    DROP TABLE IF EXISTS movie_genre CASCADE;
    DROP TABLE IF EXISTS movie CASCADE;
    DROP TABLE IF EXISTS movie_unnormalised CASCADE;
    ''' 
    
    dropper['drugs']='''
    DROP TABLE IF EXISTS drugs_prescribed CASCADE;
    DROP TABLE IF EXISTS patient_prescription CASCADE;
    DROP TABLE IF EXISTS patient_doctor CASCADE;
    DROP TABLE IF EXISTS prescription CASCADE;
    DROP TABLE IF EXISTS drug CASCADE;
    DROP TABLE IF EXISTS doctor CASCADE;
    DROP TABLE IF EXISTS patient CASCADE;
    '''
    
    dropper['references']='''
    DROP TABLE IF EXISTS referencing_table CASCADE;
    DROP TABLE IF EXISTS referenced_table CASCADE;
    '''

    
    engine = create_engine("postgresql://{user}:{password}@{host}:{port}/{dbname}".format(dbname=dbname,
                                                                                          host=host, port=port,
                                                                                          user=user, password=password))
    conn = engine.connect()
    for drop in dbs:
        if drop in dropper: conn.execute(dropper[drop])
    conn.close()