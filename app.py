from inspect import FullArgSpec
from flask import Flask, render_template, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine

app = Flask(__name__)


@app.route("/")
def ind():
    dialect = "mysql"
    username="root"
    password=""
    host="127.0.0.1:3306"
    dbname = "Campionato_Ciclistico"
    #Connection object creation
    engine = create_engine("%s://%s:%s@%s/%s"%(dialect,username,password,host,dbname))

    try:
        con = engine.connect()

        #QUERY SQL
        query="SELECT CodC, Cognome, Nome\
               FROM CICLISTA\
               ORDER BY Cognome, Nome"

        cyclists = con.execute(query)

        con.close()

        return render_template('Form_Query.html', CYCLISTS = cyclists)
    except SQLAlchemyError as e:

        error = str(e.__dict__['orig'])
        return render_template('Ins_Error.html', error_message=error)


app.run(debug=True, port=3306)
