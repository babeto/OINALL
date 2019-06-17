import xml.dom.minidom as minidom
from Schedule.Helper.LogHelper import LogHelper

class XMLHelper(object):
    """description of class"""
    @staticmethod
    def parsexmltodict(xmldt):
        dom = minidom.parseString(xmldt)
        eroot = dom.documentElement
        itemlist = eroot.getElementsByTagName('PROPERTY')
        for item in itemlist:
            # print(item)
            if item.getAttribute('NAME') == 'Data':
                elements = item.getElementsByTagName('VALUE')
                try:
                    value = elements[0].firstChild.nodeValue
                except Exception as e:
                    value = None
                    LogHelper.append(' '.join([r'parsexmltodict:find Data Value error:', str(e)]))
                    continue

            if item.getAttribute('NAME') == 'Name':
                elements = item.getElementsByTagName('VALUE')
                try:
                    key = elements[0].firstChild.nodeValue
                    # print(key)
                except Exception as e:
                    key = None
                    LogHelper.append(' '.join([r'parsexmltodict:find Name Value error:', str(e)]))
                    continue

        dtdict = {key:value}
        return dtdict