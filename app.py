#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Let your send message using Ajax.
"""

from rapidsms.apps.base import AppBase
from rapidsms.models import Contact, Connection
from rapidsms.messages.outgoing import OutgoingMessage


try:
    import cPickle as pickle
except ImportError:
    import pickle
    
def return_none(**kwargs): pass

from exceptions import DirectSmsError

PICKLED_LAMBDA = pickle.dumps( return_none).encode('utf-8')
PICKLED_DICT = pickle.dumps({}).encode('utf-8')


class App (AppBase):
    """
    Helper to send a message trough Ajax
    """

    def handle(self, message):
        pass


    def ajax_POST_send_message(self, params, form):
        """
        Callback method for sending messages from the webui via the ajax app.

        You can pass it a serialized callbacks with args, and either choose
        to send a message to a given reporter or to an anonymous one,
        according to a backend and an identity.         
        """
        
        pre_send_callback = form.get('pre_send_callback', 
                                     PICKLED_LAMBDA).encode('ASCII')
        pre_send_callback = pickle.loads(pre_send_callback) or return_none
        
        pre_send_callback_kwargs = form.get('pre_send_callback_kwargs', 
                                            PICKLED_DICT).encode('ASCII')
        pre_send_callback_kwargs = pickle.loads(pre_send_callback_kwargs) or {}
                                        
        post_send_callback = form.get('post_send_callback', 
                                     PICKLED_LAMBDA).encode('ASCII')
        post_send_callback = pickle.loads(post_send_callback) or return_none
        
        post_send_callback_kwargs = form.get('post_send_callback_kwargs', 
                                            PICKLED_DICT).encode('ASCII')
        post_send_callback_kwargs = pickle.loads(post_send_callback_kwargs) or {}
                                        
        
        backend_name = form.get('backend', '')
        identity = form.get('identity', '')
        
        if not backend_name or not identity:
        
            try:
                contact = Contact.objects.get(pk=form.get('contact', -1))
            except Contact.DoesNotExist:
                raise DirectSmsError(u"You need to specify either a valid "\
                                     u"reporter or a valid backend & identity")
            else:
                connection = contact.default_connection

                # abort if we don't know where to send the message to
                # (if the device the reporter registed with has been
                # taken by someone else, or was created in the WebUI)
                if not connection:
                   raise DirectSmsError("%s is unreachable (no connection)" %\
                                         contact)
                   
        else:        
            # attempt to send the message
            try:
                backend = self.router.backends[backend_name]
            except KeyError:
                raise DirectSmsError(u"The backend '%s' is not installed. Check "\
                                     u"your 'settings.py' file." % backend_name )
            else:
                connection = Connection(identity=identity, 
                                        backend=backend.model)
                connection.save()
                                 
        message = OutgoingMessage(connection, form.get('text', ''))
        
        pre_send_callback(outgoing_message=message, **pre_send_callback_kwargs)
        
        sent = message.send()
        
        post_send_callback(outgoing_message=message, **post_send_callback_kwargs)

        # attempt to call the callback 
        
        return sent
        
        
        

        
