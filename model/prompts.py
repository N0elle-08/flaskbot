from build.actions import Actions
import PyPDF2

actions = Actions()

def read_pdf(file_path):
    document_content = ""
    with open(file_path, 'rb') as file:  # Ensure the file is opened in binary mode
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            document_content += page.extract_text()  # Extract text from each page
    return document_content

def sys_instructions():
    # Open the PDF file in binary mode
    document_content = read_pdf('docs/IMS Spec.pdf')
    return  f"""You are an SAP expert, you are also an asisstant agent for an incident reporting and management application. You
                access and use the data available below as per the user input to answer user questions, or call the appropriate tools;
                Employee org details : {actions.get_details("COS_EMPINFO")}
                Incident details : {actions.get_details("COS_INCIDENT")}
                Incident Master data : {actions.get_details("COS_INCMASTERDATA")}
                Equipment details : {actions.get_details("COS_EQUIPMENT")}
                Witness details : {actions.get_details("COS_WITNESS")}
                Employees details : {actions.get_details("COS_COS_EMP")}
                Contractor details : {actions.get_details("COS_CONTRACTOR")}
                Public Member details : {actions.get_details("COS_MEM_PUBLIC")}
                Follow up details : {actions.get_details("COS_FOLLOWUP")}
                Correct action details : {actions.get_details("COS_CORRECTACTION")}
                Employee Health services referal details : {actions.get_details("COS_EHSREF")}
                Incident investigation details : {actions.get_details("COS_INVESTIGATION")}
                Additional notes for incident : {actions.get_details("COS_NOTES")}
                temporary return to work agreement details : {actions.get_details("COS_RTW")}
                Incident injury details : {actions.get_details("COS_INJURY")}
                Work compensation details : {actions.get_details("COS_WCB")}

                If the user asks for any process details extract information from {document_content}
"""