
from odoo import http,api,SUPERUSER_ID ,registry
from odoo.http import Controller, request 
import logging

class LoginController(Controller):

    @http.route(['/web/login_with_url/<string:safer_database>/<string:safer_user>/<int:number>'],methods=['GET'], type='http', auth='public')
    def login_without_password(self,safer_database,safer_user,number):
        SHIFT=5
        db_registry = registry(self.decrypt(safer_database,SHIFT))
        if db_registry:
            return request.redirect('/')
        cr=db_registry.cursor()
        env = api.Environment(cr, SUPERUSER_ID, {})
        url_link=f"{request.httprequest.host_url}web/login_with_url/{safer_database}/{safer_user}/{number}"
        user=env["res.users"].search([('is_generated','=',True),('url_link','=',url_link)])        
        if user:
            request.session.authenticate_without_passwd(self.decrypt(safer_database,SHIFT), self.decrypt(safer_user,SHIFT))
        return request.redirect('/')
    
    def decrypt(self,text, shift):
        """
        Decrypts the text using the Caesar cipher.
        
        :param text: The encrypted text to decrypt.
        :param shift: The number of positions to shift each character back.
        :return: The decrypted text.
        """
        decrypted_text = ""
        for char in text:
            if char.isalpha():
                # Check if the character is uppercase or lowercase
                if char.isupper():
                    decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
                else:
                    decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
            else:
                # Non-alphabetic characters are added as is
                decrypted_text += char
        return decrypted_text