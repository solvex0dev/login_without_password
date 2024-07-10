# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.http import request
import time


from math import ceil
import logging 

class ConfigLogin(models.Model):
    _inherit = 'res.users'

    url_link= fields.Char(
        string='url',  
        )

    database= fields.Char(
        string='Database',
        default=lambda self: self.env.cr.dbname,
        )
    
    timestamp = fields.Integer()
    is_generated=fields.Boolean(default=False)

    def generate_url_login(self):
        SHIFT=5
        if request and self.login:
            self.timestamp=time.time()
            self.is_generated=True
            self.url_link=f"{request.httprequest.host_url}web/login_with_url/{self.encrypt(self.database,SHIFT)}/{self.encrypt(self.login,SHIFT)}/{self.timestamp}"
        else:
            self.timestamp=0
            self.is_generated=False
            self.url_link=""
            
    def disable_url_login(self):
        self.timestamp=0
        self.is_generated=False
        self.url_link = ""
        
    
    def encrypt(self,text, shift):        
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                # Check if the character is uppercase or lowercase
                if char.isupper():
                    encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
                else:
                    encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                encrypted_text += char
        return encrypted_text