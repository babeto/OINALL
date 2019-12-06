
import exchangelib
from DB import DB


class Report(object):
    """description of class"""

    REPORT_HTML = "Report.html"

    """html报告"""
    HTML_TMPL = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>CMSE LAB</title>
            <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
            <h1 style="font-family: Microsoft YaHei">CMSE LAB</h1>
            <style type="text/css" media="screen">
        body  { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px;}
        </style>
        </head>
        <body>
        %(table)s
        </body>
        </html>"""
    
    TABLE_TMPL = """
        <h3 style="font-family: Microsoft YaHei">%(table_title)s</h3>
        <table id='result_table' class="table table-condensed table-bordered table-hover">
            <colgroup>
                <col align='left' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
            </colgroup>
            <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
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
        """

    TR_TMPL = """
        <tr class='failClass warning'>
            <td>%(number)s</td>
            <td>%(machineName)s</td>
            <td>%(owner)s</td>
            <td>%(osName)s</td>
            <td>%(lastCU)s</td>
            <td>%(rebootRequired)s</td>
            <td>%(compliant)s</td>
        </tr>"""


    TABLE_TMPL_VM = """
        <h3 style="font-family: Microsoft YaHei;">%(table_title)s</h3>
        <table id='result_table' class="table table-condensed table-bordered table-hover">
            <colgroup>
                <col align='left' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
                <col align='right' />
            </colgroup>
            <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
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
        """

    TR_TMPL_VM = """
        <tr class='failClass warning'>
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
                table_tr += TR_TMPL % dict(
                                        number = num,
                                        machineName = machine.machineName,
                                        owner = machine.owner,
                                        osName = machine.osName,
                                        lastCU = machine.lastCU,
                                        rebootRequired = machine.rebootRequired,
                                        compliant = machine.compliant                                        
                                        )
            elif type == 'vm':
                table_tr += TR_TMPL % dict(
                                        number = num,
                                        machineName = machine.machineName,
                                        host = machine.hostName,
                                        osName = machine.osName,
                                        lastCU = machine.lastCU,
                                        rebootRequired = machine.rebootRequired,
                                        compliant = machine.compliant                                        
                                        )
        table = TABLE_TMPL % dict(table_tr = table_tr, table_title = title)
        return table

    @classmethod
    def generateReport(Report):
        table = ''
        table += Report.renderTable('hm', 'sh','delta','Shanghai Lab Not compliant or scanned hosts')
        table += Report.renderTable('hm', 'red','delta','Redmond Lab Not compliant or scanned hosts')
        table += Report.renderTable('vm', 'red','delta','Redmond Lab Not compliant or scanned VMs')
        table += Report.renderTable('hm', 'sh','full','Shanghai Lab all hosts')
        table += Report.renderTable('hm', 'red','full','Redmond Lab all hosts')
        table += Report.renderTable('vm', 'red','full','Redmond Lab all VMs')

        html =Report.HTML_TMPL % dict (table = table)
        with open(Report.REPORT_HTML, 'wb') as f:
            f.write(html.encode('utf-8'))

if __name__ == '__main__':
    Report.generateReport()