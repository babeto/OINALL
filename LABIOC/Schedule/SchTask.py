from Lab import Lab
from DBEval import DBEval
from Report import Report
from Email import Email

report_file = 'Report.html'
report_title = "Shanghai Lab hosts report"
email_to = 'v-alhuan@microsoft.com,qiani@microsoft.com,feixia@microsoft.com,v-frma@microsoft.com,v-jamhua@microsoft.com,v-yjmi@microsoft.com'

Lab.startscan('hm','sh', 'full')
DBEval.evalMachines('hm','sh', 'full')

Lab.startscan('hm','sh', 'delta')
DBEval.evalMachines('hm','sh', 'delta')

Report.generateReport(report_file)
Email.send(email_to, report_title, report_file)
