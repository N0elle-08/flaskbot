import google.generativeai as genai


tools_func = genai.protos.Tool(
    function_declarations=[
      genai.protos.FunctionDeclaration(
        name='create_incident',
        description="Creates/reports an incident",
        parameters=genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'Title':genai.protos.Schema(type=genai.protos.Type.STRING, description="title/breif description of the incident max 200 characters"),
                'incDate':genai.protos.Schema(type=genai.protos.Type.STRING, description="The date when the incident occured, in YYYY-MM-DD format."),
                'empname':genai.protos.Schema(type=genai.protos.Type.STRING, description="name of the employee reporting the incident"),
                'supname':genai.protos.Schema(type=genai.protos.Type.STRING, description="name of the supervisor"),
                'shift': genai.protos.Schema(type=genai.protos.Type.STRING, description="Shift the employee is working - Day, Evening, Night, Overtime ", enum=["1", "2","3", "4"]),
            },
            required=['Title','incDate', 'empname', 'supname', 'shift' ]
        )
      )
    ])


# tools_func = [{
#             "name": "create_incident",
#             "description": "When User needs to create an incident",
#             "parameters": {
#                 "type_": "object",
#                 "properties": {
#                     "title": {
#                         "type_": "string",
#                         "description": "title/breif description of the incident max 200 characters",
#                     },
#                     "incDate": {
#                         "type_": "string",
#                         "description": "The date when the incident occured, in YYYY-MM-DD format.",
#                     },
#                     "empname": {
#                         "type_": "string",
#                         "description": "name of the employee reporting the incident",
#                         #"enum": ["metric", "imperial"],  # Defines the acceptable values
#                     },
#                     "supname": {
#                         "type_": "string",
#                         "description": "name of the supervisor",
#                         #"enum": ["metric", "imperial"],  # Defines the acceptable values
#                     },
#                 },
#                 "required": ["title", "incDate"],  
#             },
#         }

# ]