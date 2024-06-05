
from flask import Flask, request, render_template, jsonify
import pyodbc
from conexaoDB import get_db_connection
from model import Querys, Mensagem



app = Flask(__name__)


@app.route('/unsubscribe_page', methods=['GET'])
def unsubscribe_page():
    if 'emid' not in request.args or not request.args['emid']:
        return Mensagem.get_mensagem_ERRO_PaginaDeveSerAcessadaPeloLinkDisponivelEmail()

    else:
        conn = get_db_connection()
        cursor = conn.cursor()

        emid = request.args['emid']
        try:
            query = Querys.get_emailing_query(emid)
            cursor.execute(query)

            row = cursor.fetchone()
           
            if row is None:
                # return "<br><br><center>Erro: não foi possível identificar o cliente.<br>Por gentileza entre em contato com a Ativos através do atendimento@ativossa.com.br</center>"
                return Mensagem.get_mensagem_ERRO_PaginaDeveSerAcessadaPeloLinkDisponivelEmail()

            columns = [column[0] for column in cursor.description]
            row_dict = dict(zip(columns, row))
            print(row_dict)
            id_emailing = row_dict['id_emailing']
            destinatario_email = row_dict['destinatario_email']
            id_categoria = row_dict['id_categoria']
            nome = row_dict['valor']
            id_unsub = row_dict['id_unsub']
            
            cursor.close()
            conn.close()

            conn = get_db_connection()
            cursor = conn.cursor()

            if id_unsub is None:
               
                query2 = Querys.get_emailing_query_2(id_categoria)
                cursor.execute(query2)
                
                print(id_categoria)
                unsub_motivos = cursor.fetchall()
                return render_template("unsubscribe_form.html", page_id="unsubscribe", destinatario=destinatario_email,
                                       id_emailing=id_emailing, unsub_motivos=unsub_motivos, nome=nome)
            else:    
                return Mensagem.get_mensagem_ERRO_JaDescadastrado()
            
        except pyodbc.Error as e:
            print('Ocorreu um erro durante a execução da consulta:', e)
            return Mensagem.get_mensagem_ERRO_PaginaDeveSerAcessadaPeloLinkDisponivelEmail()
    
        finally:
            cursor.close()
            conn.close()


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    if request.method == 'POST':
        try:
            # Depuração: imprimir os parâmetros recebidos
            print("answer:", request.form['answer'])
            print("id_emailing:", request.form['id_emailing'])

            id_unsub_motivo = request.form['answer']
            id_emailing = request.form['id_emailing']

            conn = get_db_connection()
            cursor = conn.cursor()

            sql = Querys.get_emailing_query_3(id_emailing, id_unsub_motivo)
            cursor.execute(sql)
            conn.commit()

            cursor.close()
            conn.close()

            return jsonify({'message': 'Descadastramento realizado com sucesso.'}), 200
        except pyodbc.Error as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
