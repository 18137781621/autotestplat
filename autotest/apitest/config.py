import configparser
import os
def getConfig(section,key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '\\settings.conf'
    config.read(path)
    return config.get(section,key)
if __name__ == '__main__':
    co = getConfig('database','host')
    print(co)