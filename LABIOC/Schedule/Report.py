
import exchangelib
from DB import DB


class Report(object):
    """description of class"""

    REPORT_HTML = "Report.html"

    """html报告"""
    HTML_TMPL = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>CMSE LAB</title>
            <style>
                table {table-layout:fixed}
            </style>
        </head>
        <body>
        %(table)s
        </body>
        </html>"""
    
    TABLE_TMPL = """
        <b style="font-family: Microsoft YaHei">%(table_title)s:</b>
        <table id='result_table'>
            <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;background-color:lightgrey">
                <th>No.</th>    
                <th>Machine</th>
                <th>Owner</th>
                <th>OS</th>
                <th>LatestCU</th>
                <th>RebootPending</th>
                <th>Compliant</th>
            </tr>
            %(table_tr)s
        </table>
        <br/>
        """

    TR_TMPL = """
        <tr>
            <td>%(number)s</td>
            <td>%(machineName)s</td>
            <td>%(owner)s</td>
            <td>%(osName)s</td>
            <td>%(lastCU)s</td>
            <td>%(rebootRequired)s</td>
            <td>%(compliant)s</td>
        </tr>"""


    TABLE_TMPL_VM = """
        <b style="font-family: Microsoft YaHei">%(table_title)s:</b>
        <table id='result_table' class="table table-condensed table-bordered table-hover">
            <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;background-color:lightgrey">
                <th>No.</th>
                <th>Machine</th>
                <th>Host</th>
                <th>OS</th>
                <th>LatestCU</th>
                <th>RebootPending</th>
                <th>Compliant</th>
            </tr>
            %(table_tr)s
        </table>
        <br/>
        """

    TR_TMPL_VM = """
        <tr>
            <td>%(number)s</td>    
            <td>%(machineName)s</td>
            <td>%(host)s</td>
            <td>%(osName)s</td>
            <td>%(lastCU)s</td>
            <td>%(rebootRequired)s</td>
            <td>%(compliant)s</td>
        </tr>"""


    @classmethod
    def renderTable(Report, type, location, scope, title):
        machinelist = DB.getlist(type, location, scope)
        if type == 'hm':
            TABLE_TMPL = Report.TABLE_TMPL
            TR_TMPL = Report.TR_TMPL
        elif type == 'vm':
            TABLE_TMPL = Report.TABLE_TMPL_VM
            TR_TMPL = Report.TR_TMPL_VM

        table_tr = ''
        for num, machine in enumerate(machinelist, start = 1):
            if type == 'hm':
                
                if machine.rebootRequired == True:
                    rebootstatus = 'Need Reboot'
                else:
                    rebootstatus = 'No'
                table_tr += TR_TMPL % dict(
                                        number = num,
                                        machineName = machine.machineName,
                                        owner = machine.owner,
                                        osName = machine.osName,
                                        lastCU = machine.lastCU,
                                        rebootRequired = rebootstatus,
                                        compliant = machine.compliant                                        
                                        )
            elif type == 'vm':
                if machine.rebootRequired == True:
                    rebootstatus = 'Need Reboot'
                else:
                    rebootstatus = 'No'
                table_tr += TR_TMPL % dict(
                                        number = num,
                                        machineName = machine.machineName,
                                        host = machine.hostName,
                                        osName = machine.osName,
                                        lastCU = machine.lastCU,
                                        rebootRequired = rebootstatus,
                                        compliant = machine.compliant                                        
                                        )
        table = TABLE_TMPL % dict(table_tr = table_tr, table_title = title)
        return table

    @classmethod
    def generateReport(Report, file):
        table = ''
        table += Report.renderTable('hm', 'sh','delta','Shanghai hosts NOT compliant or NOT scanned')

        table += Report.renderTable('hm', 'sh','full','Shanghai hosts')

        html =Report.HTML_TMPL % dict (table = table)
        with open(file, 'wb') as f:
            f.write(html.encode('utf-8'))

if __name__ == '__main__':
    Report.generateReport()