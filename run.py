from trains import app
app.run()

try:
    if not app.debug:
        import logging
        from logging.handlers import RotatingFileHandler
          
        '''
        The log file will go to our logs directory, with name logs.log. 
        I am using the RotatingFileHandler so that there is a limit to the amount of logs that are generated. 
        In this case I limit the size of a log file to one megabyte, and we will keep the last ten log files as backups.
        Resource: Miguel Grinberg blogpost "The Flask Mega-Tutorial"
        '''
          
        file_handler = RotatingFileHandler('../logs/logs.log', 'a', 1 * 1024 * 1024, 10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('Kiwiland Trains')
 
except Exception as e:
            print (str(e))