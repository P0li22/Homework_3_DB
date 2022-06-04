from flask import Flask, render_template, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("Home.html")


@app.route("/campionato_ciclistico")
def ind():
    dialect = "mysql"
    username = "root"
    password = ""
    host = "127.0.0.1:3306"
    dbname = "campionato_ciclistico"
    engine = create_engine("%s://%s:%s@%s/%s" % (dialect, username, password, host, dbname))

    action = request.args.get('action')

    if action == "Ricerca nel database":

        try:
            con = engine.connect()

            query = "SELECT CodC, Cognome, Nome\
                    FROM CICLISTA\
                    ORDER BY Cognome, Nome"

            ciclisti = con.execute(query)

            con.close()

            return render_template('Form_Query.html', ciclisti=ciclisti)
        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            return render_template('KO.html', error_message=error)

    elif action == "Aggiornamento classifica":

        try:
            con = engine.connect()

            query = "SELECT CodC, Cognome, Nome\
                            FROM CICLISTA\
                            ORDER BY Cognome, Nome"

            ciclisti = con.execute(query)

            query = "SELECT CodT, Edizione\
                    FROM TAPPA\
                    ORDER BY Edizione, CodT"

            tappe = con.execute(query)

            con.close()

            return render_template('Form_Tappa_Ins.html', ciclisti=ciclisti, tappe=tappe)
        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            return render_template('KO.html', error_message=error)

    elif action == "Inserimento ciclista":
        try:
            con = engine.connect()

            query = "SELECT CodS, NomeS\
                    FROM SQUADRA\
                    ORDER BY CodS, NomeS"

            squadre = con.execute(query)

            con.close()

            return render_template("Form_Ciclista_Ins.html", squadre=squadre)
        except SQLAlchemyError as e:

            error = str(e.__dict__['orig'])
            return render_template('KO.html', error_message=error)
    else:
        return render_template('KO.html', error_message="Azione non valida")


@app.route("/result")
def read_form_query():
    dialect = "mysql"
    username = "root"
    password = ""
    host = "127.0.0.1:3306"
    dbname = "campionato_ciclistico"
    engine = create_engine("%s://%s:%s@%s/%s" % (dialect, username, password, host, dbname))

    try:
        con = engine.connect()

        ciclista = int(request.args.get('cod_ciclista'))
        tappa = int(request.args.get('cod_tappa'))

        if tappa == "":
            return render_template('Risultato.html', error_message="Valori inseriti non validi")

        query = "SELECT Nome, Cognome, NomeS, CodT, Edizione, Posizione\
                FROM CICLISTA C, CLASSIFICA_INDIVIDUALE CI, SQUADRA S\
                WHERE C.CodC = CI.CodC AND C.CodS = S.CodS\
                AND C.CodC = '%d' AND CI.CodT = '%d'\
                ORDER BY Edizione, CodT" % (ciclista, tappa)

        res = con.execute(query)

        con.close()

        return render_template('Risultato.html', res=res)
    except SQLAlchemyError as e:

        error = str(e.__dict__['orig'])
        return render_template('KO.html', error_message=error)


@app.route("/aggiornamento_classifica")
def aggiornamento_classifica():
    dialect = "mysql"
    username = "root"
    password = ""
    host = "127.0.0.1:3306"
    dbname = "campionato_ciclistico"
    engine = create_engine("%s://%s:%s@%s/%s" % (dialect, username, password, host, dbname))

    try:
        con = engine.connect()

        ciclista = int(request.args.get("cod_ciclista"))
        tappa = [int(s) for s in request.args.get("cod_ed_tappa") if s.isdigit()]
        posizione = int(request.args.get("pos_ciclista"))
        # qua devo inserire la query tappa[0] = codT e tappa[1] = edizione
        query = "INSERT INTO CLASSIFICA_INDIVIDUALE VALUES('%d', '%d', '%d', '%d')" \
                % (ciclista, tappa[1], tappa[0], posizione)

        con.execute(query)
        con.close()

        return render_template('OK.html')
    except SQLAlchemyError as e:

        error = str(e.__dict__['orig'])
        return render_template('KO.html', error_message=error)


@app.route("/inserimento_ciclista")
def inserimento_ciclista():
    dialect = "mysql"
    username = "root"
    password = ""
    host = "127.0.0.1:3306"
    dbname = "campionato_ciclistico"
    engine = create_engine("%s://%s:%s@%s/%s" % (dialect, username, password, host, dbname))

    try:
        con = engine.connect()

        ciclista = int(request.args.get("cod_ciclista"))
        nome = request.args.get("nome_ciclista")
        cognome = request.args.get("cognome_ciclista")
        nazionalita = request.args.get("nazionalita_ciclista")
        squadra = int(request.args.get("squadra_ciclista"))
        anno_nascita = int(request.args.get("anno_nascita_ciclista"))

        query="INSERT INTO CICLISTA VALUES('%d', '%s', '%s', '%s', '%d', '%d')" \
              % (ciclista, nome, cognome, nazionalita, squadra, anno_nascita)

        con.execute(query)
        con.close()

        return render_template('OK.html')
    except SQLAlchemyError as e:

        error = str(e.__dict__['orig'])
        return render_template('KO.html', error_message=error)


app.run(debug=True, port=8080)
