def get_emailing_query(emid):
    return f"""SELECT 
            t.id_emailing,
            t.destinatario_ndg, 
            c.id_categoria,
            t.id_campanha, 
            t.destinatario_email, 
            d.id_unsub,
            camp.valor
			
            FROM [dbo].tbl_emailing t 
                LEFT JOIN [dbo].tbl_emailing_campanha c 
                    ON c.id_campanha = t.id_campanha						
                LEFT JOIN [dbo].[tbl_emailing_unsubscribe] d 
                    ON t.id_emailing = d.id_emailing 
                INNER JOIN [dbo].[tbl_emailing_campos] camp
                    ON t.id_emailing = camp.id_emailing 
                    AND CAMP.chave = 'nome' 
                    WHERE t.hash = {emid}"""
                    
                                       
def get_emailing_query_2(id_categoria):
    return f"""
        SELECT id_motivo_unsubscribe, ds_motivo_unsubscribe 
            FROM [dbo].[tbl_emailing_unsubscribe_motivo] 
        WHERE st_ativo = 1 AND id_categoria = {id_categoria}"""
        
def get_emailing_query_3(id_emailing, id_unsub_motivo):
    return f"INSERT INTO [dbo].[tbl_emailing_unsubscribe] VALUES ({id_emailing}, {id_unsub_motivo})"