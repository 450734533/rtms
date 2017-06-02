# -*- coding:utf-8 -*-
import logging
import time

def initLogging(logFilename):
    """Init for logging
    """
    logdate = time.strftime('%Y%m%d',time.localtime())
    logging.basicConfig(
                    level    = logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  #format: 指定输出的格式和内容
                    filename = logFilename+'_'+logdate+'.log',
                    filemode = 'a');
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler();
    console.setLevel(logging.DEBUG);
    # set a format which is simpler for console use
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s');
    # tell the handler to use this format
    #console.setFormatter(formatter);
    #logging.getLogger('').addHandler(console);  #控制台输出

