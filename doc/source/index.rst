.. Direct SMS documentation master file, created by
   sphinx-quickstart on Fri Aug 13 09:44:27 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Direct SMS's documentation!
======================================

Direct SMS is a `RapidSMS <http://www.rapidsms.org/>`_ app that allows you
to send an SMS outside the router thread (e.g. from a Django view).

For now, it's tested only with the first version of RapidSMS, not the new core, 
and requires the "ajax" app to work.

Contents:

.. toctree::
   :maxdepth: 2

Setup
-----

Copy / paste the entire direct_sms folder to the ./apps directory of your 
project. Add 'direct_sms' in the app list of your local.ini file.

Usage
------

::

    from direct_sms.utils import send_msg
    
    # you can send a message to a reporter
    
    reporter = Reporter.objects.all()[0] 
    send_msg(reporter, "Hello !")
    
    # you can send a message knowing only the backend and identity
    
    backend = PersistantBackend.objects.get(title='pygsm')
    identity = "555-555-555"
    send_msg(backend=backend, identity=identity, text="Hello !")

    # you can set a callback fonction to be called just before the message
    # is sent
    
    def my_callback(outgoing_message, arg):
        print "Going to send %s with arg %s" % (str(outgoing_message), arg)
    
    send_msg(reporter, "Hello !",
             callback=my_callback, 
             callback_kwargs={'arg':'Super arg'})   
    

.. note::
    
    Callbacks are serialized using pickle. It means you better avoid passing
    complex objects (such as model, instead pass ids), and if you do, you 
    should refresh the object in the callback fonction (for model, reload data
    fromt he DB).
    
    The second thing you need to know is that Pickle can only serialize 
    fonctions declared at the top level of a module. Therefor you can define
    a callback fonction in a shell and use it to test it right away.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

