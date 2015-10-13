 # -*- coding: utf-8 -*-

SURVEY_DAYS = 30

BEST = {}
BEST['ex. Getting questions answered and explained'] = 1
BEST['ex. Finishing tasks quickly'] = 2
BEST['ex. Courteous staff'] = 3

WORST = {}
WORST['ex. Long wait time'] = 1
WORST['ex. Repeated visits for the same issue'] = 2
WORST['ex. Not being familiar with how the process works'] = 3

ROUTES = {}
ROUTES['Building / Roofing / Structural'] = 1
ROUTES['Edificio / Techos / Estructural'] = 1
ROUTES['Cashier'] = 2
ROUTES['Cajero'] = 2
ROUTES['Code Violations'] = 3
ROUTES[u'Violaciónes de Código'] = 3
ROUTES['Contractor Licensing'] = 4
ROUTES['Licencias de contratista'] = 4
ROUTES['Electrical'] = 5
ROUTES[u'Eléctrico'] = 5
ROUTES['Environmental Resources Management (DERM)'] = 6
ROUTES[u'Gestión de Recursos Ambientales (DERM)'] = 6
ROUTES['Fire Department'] = 7
ROUTES['Health Department (HRS)'] = 8
ROUTES['Departamento de Salud (HRS)'] = 8
ROUTES['Microfilm'] = 9
ROUTES['Mechanical'] = 10
ROUTES['Mecánica'] = 10
ROUTES['Permit Application Intake and Information'] = 11
ROUTES[u'Información e Ingesta -- Applicaciones de Permiso'] = 11
ROUTES['Plumbing'] = 12
ROUTES[u'Plomería'] = 12
ROUTES['Water and Sewer Department (WASD)'] = 13
ROUTES['Departamento de Agua y Alcantarillado (WASD)'] = 13
ROUTES['Zoning / Impact Fees / Public Works'] = 14
ROUTES[u'Zonificación / Cargos de Impacto / Obras Públicas'] = 14

ROLES = {}
# FIXME: VERIFY CONSTANTS AGAINST V4 TEXTIT
ROLES['1'] = 'Contractor'
ROLES['2'] = 'Architect'
ROLES['3'] = 'Permit Consultant'
ROLES['4'] = 'Homeowner'
ROLES['5'] = 'Business Owner'

TF = {}
TF['API'] = 'https://api.typeform.com/v0/form/NNCQGT?key='
TF['KEY'] = '433dcf9fb24804b47666bf62f83d25dbef2f629d'

TF['LANG_EN'] = 'list_11278243_choice'
TF['ROLE_EN'] = 'list_11029984_choice'
TF['ROLE_ES'] = 'list_11029987_choice'

TF['PURP_EN'] = 'list_11029985_choice'
TF['PURP_OTHER_EN'] = 'list_11029985_other'
TF['PURP_ES'] = 'list_11422502_choice'
TF['PURP_OTHER_ES'] = 'list_11422502_other'

TF['OPINION_EN'] = 'opinionscale_11029990'
TF['OPINION_ES'] = 'opinionscale_11029991'

TF['GETDONE_EN'] = 'yesno_11029979'
TF['GETDONE_ES'] = 'yesno_11278208'

TF['BEST_EN'] = 'list_11277420_choice'
TF['BEST_OTHER_EN'] = 'list_11277420_other'
TF['WORST_EN'] = 'list_11277432_choice'
TF['WORST_OTHER_EN'] = 'list_11277432_other'
TF['BEST_ES'] = 'list_11277910_choice'
TF['BEST_OTHER_ES'] = 'list_11277910_other'
TF['WORST_ES'] = 'list_11277952_choice'
TF['WORST_OTHER_ES'] = 'list_11277952_other'

TF['IMPROVE_EN'] = 'textarea_11959533'
TF['IMPROVE_ES'] = 'textarea_11959667'

TF['COMMENTS_EN'] = 'textarea_11029995'
TF['COMMENTS_ES'] = 'textarea_11029999'

TF['ROUTE_EN'] = 'list_11510353_choice'
TF['ROUTE_ES'] = 'list_11510726_choice'

TF['FOLLOWUP_EN'] = 'yesno_11029980'
TF['FOLLOWUP_ES'] = 'yesno_11029983'
TF['CONTACT_EN'] = 'textfield_11277574'
TF['CONTACT_ES'] = 'textfield_11278128'
