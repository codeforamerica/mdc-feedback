 # -*- coding: utf-8 -*-

SURVEY_DAYS = 30

EMAIL = {}
EMAIL[1] = ['mdcfeedbackdev+1a@gmail.com', 'mdcfeedbackdev+1b@gmail.com']
EMAIL[2] = ['mdcfeedbackdev+2a@gmail.com', 'mdcfeedbackdev+2b@gmail.com']
EMAIL[3] = ['mdcfeedbackdev+3a@gmail.com', 'mdcfeedbackdev+3b@gmail.com']
EMAIL[4] = ['mdcfeedbackdev+4a@gmail.com', 'mdcfeedbackdev+4b@gmail.com']
EMAIL[5] = ['mdcfeedbackdev+5a@gmail.com', 'mdcfeedbackdev+5b@gmail.com']
EMAIL[6] = ['mdcfeedbackdev+6a@gmail.com', 'mdcfeedbackdev+6b@gmail.com']
EMAIL[7] = ['mdcfeedbackdev+7a@gmail.com', 'mdcfeedbackdev+7b@gmail.com']
EMAIL[8] = ['mdcfeedbackdev+8a@gmail.com', 'mdcfeedbackdev+8b@gmail.com']
EMAIL[9] = ['mdcfeedbackdev+9a@gmail.com', 'mdcfeedbackdev+9b@gmail.com']
EMAIL[10] = ['mdcfeedbackdev+10a@gmail.com', 'mdcfeedbackdev+10b@gmail.com']
EMAIL[11] = ['mdcfeedbackdev+11a@gmail.com', 'mdcfeedbackdev+11b@gmail.com']
EMAIL[12] = ['mdcfeedbackdev+12a@gmail.com', 'mdcfeedbackdev+12b@gmail.com']
EMAIL[13] = ['mdcfeedbackdev+13a@gmail.com', 'mdcfeedbackdev+13b@gmail.com']
EMAIL[14] = ['mdcfeedbackdev+14a@gmail.com', 'mdcfeedbackdev+14b@gmail.com']

BEST = {}
BEST['ex. Getting questions answered and explained'] = 1
BEST['ex. Finishing tasks quickly'] = 2
BEST['ex. Courteous staff'] = 3
BEST[1] = 'ex. Getting questions answered and explained'
BEST[2] = 'ex. Finishing tasks quickly'
BEST[3] = 'ex. Courteous staff'
BEST[4] = 'Other'

WORST = {}
WORST['ex. Long wait time'] = 1
WORST['ex. Repeated visits for the same issue'] = 2
WORST['ex. Not being familiar with how the process works'] = 3
WORST[1] = 'ex. Long wait time'
WORST[2] = 'ex. Repeated visits for the same issue'
WORST[3] = 'ex. Not being familiar with how the process works'
WORST[4] = 'Other'

ROLES = {}
# FIXME: VERIFY CONSTANTS AGAINST V4 TEXTIT
ROLES[1] = 'Contractor'
ROLES[2] = 'Architect / Engineer'
ROLES[3] = 'Permit Consultant'
ROLES[4] = 'Homeowner'
ROLES[5] = 'Business Owner'
ROLES['Contractor'] = 1
ROLES['Contratista'] = 1
ROLES['Architect / Engineer'] = 2
ROLES['Arquitecto / Ingeniero'] = 2
ROLES['Permit Consultant'] = 3
ROLES['Consultor de Permiso'] = 3
ROLES['Homeowner'] = 4
ROLES[u'Dueño/a de Casa'] = 4
ROLES['Business Owner'] = 5
ROLES[u'Dueño/a de Negocio'] = 5

PURPOSE = {}
PURPOSE['Apply for a permit'] = 1
PURPOSE['Meet with an Inspector'] = 2
PURPOSE['Meet with a Plan Reviewer'] = 3
PURPOSE['Find out about a violation or lien on your property'] = 4
PURPOSE['Obtain a certificate of use and/or occupancy'] = 5
PURPOSE['Solicitar un permiso'] = 1
PURPOSE['Reunirse con un Inspector'] = 2
PURPOSE[u'Reúnirse con un Revisador de Planes'] = 3
PURPOSE['Nos enteramos de una violación o de un gravamen sobre nuestra propiedad'] = 4
PURPOSE[u'Obtener un certifcado de uso y / o ocupación'] = 5
PURPOSE[1] = 'Obtain a certificate of use and/or occupancy'
PURPOSE[2] = 'Apply for a permit'
PURPOSE[3] = 'Meet with a Plan Reviewer'
PURPOSE[4] = 'Meet with an Inspector'
PURPOSE[5] = 'Find out about a violation or lien on your property'
PURPOSE[6] = 'Other'

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
ROUTES[1] = 'Building / Roofing / Structural'
ROUTES[2] = 'Cashier'
ROUTES[3] = 'Code Violations'
ROUTES[4] = 'Contractor Licensing'
ROUTES[5] = 'Electrical'
ROUTES[6] = 'Environmental Resources Management (DERM)'
ROUTES[7] = 'Fire Department'
ROUTES[8] = 'Health Department (HRS)'
ROUTES[9] = 'Microfilm'
ROUTES[10] = 'Mechanical'
ROUTES[11] = 'Permit Application Intake and Information'
ROUTES[12] = 'Plumbing'
ROUTES[13] = 'Water and Sewer Department (WASD)'
ROUTES[14] = 'Zoning / Impact Fees / Public Works'

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
