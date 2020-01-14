#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-23 15:15:35
# @Author  : Yang Sen (yangsen@zuoyebang.com)
# @Link    : https://github.com/MagicSen
# @Version : 1.0.0

import os
#import ConfigParser
import configparser as ConfigParser

##
## @brief      Class for configuration.
##             load configuration file
##
class Configuration:
    def __init__(self, config_file):
        self.server_detail = {}
        self.model_detail = {}
        self.LoadConfigurationFile(config_file)

    def LoadConfigurationFile(self, config_file):
        if not os.path.exists(config_file):
            return False
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(config_file)

        server_detail_options = self.cf.options("ServerDetail")
        if 'port' in server_detail_options:
            self.server_detail['port'] = int(self.cf.get('ServerDetail', 'port'))
        else:
            self.server_detail['port'] = 9000

        if 'ip' in server_detail_options:
            self.server_detail['ip'] = self.cf.get('ServerDetail', 'ip')
        else:
            self.server_detail['ip'] = 'localhost'

        if 'workers' in server_detail_options:
            self.server_detail['workers'] = int(self.cf.get('ServerDetail', 'workers'))
        else:
            self.server_detail['workers'] = 1