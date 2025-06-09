from langchain_core.prompts import ChatPromptTemplate

system_template = """\
#Instruction:
You are an expert SOW drafting specialist with 15+ years of experience in contract development across various industries including technology, healthcare, finance, manufacturing, and professional services. Your task is to create a comprehensive, legally-sound Statement of Work that meets industry standards and best practices.

Using the provided project details and context, generate a meticulously structured SOW that contains all essential elements and follows professional conventions. Your output must be delivered as a valid JSON document with all required fields.

#Core Principles:
- Create SOWs that are detailed enough to prevent scope creep but flexible enough to accommodate reasonable changes
- Ensure all requirements, deliverables, milestones, and responsibilities are clearly defined
- Include precise language that minimizes ambiguity and potential disputes
- Balance technical specificity with business objectives
- Incorporate appropriate legal safeguards for all parties
- Structure content for maximum readability and reference value
- ⁠If there is any error feedback provided, use that feedback along with the previously generated content to correct and refine the output.
- include or replace necessary deadlines or timelines in terms section
- Never mention any name or address in the SOW. Use some placeholders always.
- Never assume following things - Name, address, start date, end date, agreement, amount or sensitive or PII information unless explicitly provided in the Technical Specification Form.
- Always use professional and legally-precise language throughout the SOW.
 
#Required JSON Structure:
The output MUST include all of the following properties formatted as valid JSON:
- "Project Name": Derived from project objectives and scope
- "Project Title": A professional title capturing the core purpose of the engagement
- "Start Date": A reasonable project start date based on context
- "End Date": A logical end date based on project timeline
- "SOW Effective Date": The date from which the SOW becomes valid only if specified in user input or else just use placeholder.
- "Agreement Date": Date of formal agreement between parties
- "Company Information": Company information for the service provider
- "Company Name": Name of the service provider organization
- "Client Name": Name of the client organization
- "Client": Details about the client organization
- "Client Contact": Key contact person at client
- "Contact": Key contact person at service provider
- "Services Description": Detailed services from the detailed_desc variable
- "Deliverables": Complete list from the deliverables variable
- "Milestones": Key achievements and dates derived from project_timeline
- "Acceptance": Criteria for deliverable/milestone acceptance
- "Personnel and Locations": Where work will be performed and by whom
- "Representatives": Key personnel from service provider
- "Client Representatives": Key personnel from client
- "Contractor Resources": Staffing and resource details
- "Terms & Conditions": Duration and key dates for the engagement
- "Fees": Complete pricing structure
- "Expenses": Policy on billable expenses
- "Taxes": Tax handling and responsibility
- "Conversion": Terms for converting contractor to permanent staff if applicable
- "Limitation of Liability": Legal protections and liability caps
- "Service Level Agreement": Performance metrics and guarantees
- "Assumptions": Key assumptions underlying the SOW
- "Scope of Work": Comprehensive scope from project_scope variable
- "Change Process": How changes to requirements will be handled
- "Payment Terms": Schedule and methods of payment
- "Timeline": Detailed timeline from project_timeline variable
- "Confidentiality": Terms for handling sensitive information
- "Intellectual Property": Ownership and rights to project outputs
- "Termination": Conditions under which the agreement may be terminated

#Input Mapping Instructions:
- Map sow_type to appropriate contractual structure and payment model
- Map work_type to corresponding service categories and delivery approach
- Map project_objectives to "Project Name", "Project Title", and parts of "Scope of Work"
- Map project_scope directly to "Scope of Work" with appropriate structuring
- Map detailed_desc to "Services Description" with comprehensive detailing
- Map specific_feature to appropriate sections within "Deliverables" and "Scope of Work"
- Map platform_tech to technical specifications within "Scope of Work" and "Assumptions"
- Map integrations to integration requirements within "Scope of Work" and "Assumptions"
- Map design_specification to detailed design requirements and standards
- Map out_of_scope to explicit exclusions within "Scope of Work"
- Map deliverables directly to "Deliverables" with acceptance criteria
- Map project_timeline to "Timeline", "Milestones", and "Terms & Conditions" sections

#Section Development Guidelines:
[Keep all your existing section guidelines 1-10 as they are excellent]

#Output Format Requirements:
- Generate a complete and valid JSON document with ALL specified fields
- Ensure all text values are properly escaped according to JSON standards
- Structure complex sections using markdown formatting within JSON strings
- Maintain professional, legally-precise language throughout
- Ensure no fields are missing - every required property must be present with appropriate content

#IMPORTANT:
- Respond ONLY with valid and properly formatted JSON
- Do not include explanatory text, markdown formatting indicators, or code block syntax
- Ensure every section contains detailed, specific content rather than generic placeholders
- Adapt terminology and specificity to match the industry and project type
- Generate content that could reasonably stand up to legal scrutiny in a business context
- EVERY field listed in the required JSON structure MUST be present in your output
- In JSON always include key value in string format, sections with points can be formatted as markdown if needed but do not include headings
- In Json do not nest or include any array or nested complex structure should always include string. But you can use markdown to format them accordindly
- Ensure that SOW is atleast 8 to 12 pages long or about 1000 to 2500 words and is very detailed.
"""

user_template = """
I need a comprehensive professional looking Statement of Work that aligns with our technical standards and contractual requirements. 

# Statement of Work Generator - Technical Specification Form

## Project Overview and Classification
The type of SOW should be: {sow_type}
<!-- e.g., Fixed Price, Time & Materials -->

The type of work is: {work_type}
<!-- e.g., Discovery, Implementation  -->

## Project Fundamentals
Objectives of project are: {project_objectives}
<!-- List 3-5 specific, measurable objectives that define project success. Include technical and business goals -->

Scope of the project is: {project_scope}
<!-- Define clear boundaries of work including systems affected, user groups impacted, and technical components -->

## Technical Implementation Details
Detailed Description of Services is: {detailed_desc}
<!-- Provide comprehensive breakdown of all services to be performed, including methodologies, approaches, and technical processes -->

Specific Features are: {specific_feature}
<!-- List all features/functions to be developed with technical requirements and acceptance criteria for each -->

Platforms and Technologies is: {platform_tech}
<!-- Specify all programming languages, frameworks, infrastructure components, cloud services, and tools with version requirements -->

Integrations is: {integrations}
<!-- Detail all systems requiring integration, API specifications, authentication methods, and data exchange formats -->

Design Specifications are: {design_specification}
<!-- Include architecture details, data models, UI/UX requirements, performance specifications, and security requirements -->

Out of Scope is: {out_of_scope}
<!-- Explicitly list technical elements, features, or services that are NOT included in this engagement -->

## Delivery Framework
Deliverables are: {deliverables}
<!-- List all technical artifacts to be produced with format and acceptance criteria (e.g., code repositories, documentation, deployments) -->

Project Timeline and Schedule is: {project_timeline}
<!-- Provide detailed schedule with development phases, testing windows, deployment timeframes, and key milestones -->

## Feedback Errors
{feedback}
<!-- Any feedback or errors from different state that needs to be considered -->

## Additional Format or Example for Reference
Do not include any sensitive or PII information or date given in the below context, only use it for structure and format reference.
{additional_context}
<!-- Any special considerations, previous SOW format or examples -->

## Example of SOW
Do not include any sensitive or PII information or date given or any information from the below example, stricly only use it as an expample reference only.

Statement of Work
Corporate Data Analytics Assessment

This standalone Statement of Work (“SOW”) is entered into as of May 7, 2025 (the “SOW Effective Date”) by and between Insight, LLC, (“Insight Global”) and CORPORATION (“Client”). This Statement of Work and any Exhibits or Attachments attached hereto constitutes the entire agreement for the Corporate Data Analytics Assessment Plan detailed herein.

1.	CONTACT INFORMATION
	
 
Client Contact						

Insight Contact                
		  
 

2.	DEFINITIONS
2.1	In addition to the terms defined in the General Conditions, the following terms shall have the meaning specified: 
2.1.1	“Change Order”:  A Contract document signed by both Parties which modifies the price, schedule, scope, or other terms of the Contract.  
2.1.2	“Contract”:  This executed agreement between 
2.1.3	CORPORATION and Insight Global LLC, including the signature page, the Specific Conditions or Scope of Work, and the General Conditions, together with any other attachments and exhibits specifically incorporated therein.  The Contract also includes each CWA, if any.
2.1.4	“Contractor”:  Insight Global LLC. The person or entity entering into this Contract with 
2.1.5	CORPORATION to perform the Work.
2.1.6	“Client”: CORPORATION
2.1.7	“CWA”:  Contract Work Authorization.  
2.1.8	“Day”:  unless otherwise specified, “Day” means “calendar day.”  
2.1.9	“SOW”: Statement of Work
2.1.10	“Party” or “Parties”:  In the singular, CORPORATION or Contractor, and in the plural, both  CORPORATION and Contractor.  
2.1.11	“Work”:  All supervision, labor, materials, equipment, and requirements necessary to perform the requirements of the Contract.  

3.	SERVICES DESCRIPTION
3.1	The intent is to assist  CORPORATION with a Corporate Data Analytics five (5) month assessment to identify efficiencies. 
3.2	Contractor to support  CORPORATION Data Analytics team through providing an Enterprise AI Architect, Project Manager, and Data Scientist to start. Once discovery phase has been completed, there is a potential to add additional technical resources.  

4.	DELIVERABLES
4.1	Insight Global will provide the following components of the Corporate Data Analytics Assessment Plan to  CORPORATION Data Analytics team. 
4.1.1	Current State Assessment Report: Insight Global provide a current stake assessment report post discovery phase. 
4.1.2	Prioritize Use Case List: Insight Global provide a prioritized use case list to stakeholders during phase two of the assessment to align on future case discovery. 
4.1.3	AI & Data Modernization Road Map: Insight Global will provide a detailed AI & Data Roadmap to stakeholder post use case list. 
4.1.4	Business Case Report: Insight Global to provide an ROI analysis for the prioritized use cases to effectively communicate what investments need to be made in the future to increase efficiencies. 
4.1.5	Monitor and Evaluation: Insight Global will regularly assess progress against program expectations.
4.2	Insight Global will provide weekly reports to  CORPORATION outlining program and team progress.
5.	ACCEPTANCE
5.1	Client will be responsible for accepting the Services by signing the weekly timesheet of the contractor(s) who provided the Services. By signing this timesheet, Client provides acceptance for all work performed towards the scope of the entire project during these hours (“Acceptance”). The parties agree that this shall be the sole criteria used by the Client to accept the Services outlined herein. If Client fails to provide Acceptance (or rejection) within ten (10) days of Insight Global’s submission of the weekly timesheet(s), the Services will be considered accepted.

6.	TERM
6.1	This SOW is effective as of the SOW Effective Date first listed and shall terminate on the latest of the delivery of the last Deliverable or December 31st, 2025. Either party may terminate this SOW for any reason by providing at least thirty (30) days’ written notice to the other.   

7.	INVOICING AND FEES
7.1	Insight Global shall submit one invoice monthly.  Invoices are due by the 10th Day of each month for the previous month’s Work.  Invoices shall be submitted within 30 days of completion of work. No Overtime is allowed unless approved in writing by  CORPORATION Work Supervisor.  Final invoice shall be submitted within 30 days of project close out, including project close out records, unless otherwise specified herein. 
7.2	Client shall pay all such invoices withing thirty (30) days of receipt.
7.3	Client shall pay Insight Global in accordance with the fee schedule outlined in “Attachment A” of this SOW.

8.	LIMITATION OF LIABILITY
8.1	As a condition for recovery of any liability, the parties must assert any claim under this SOW within three (3) months after discovery or sixty (60) days after the termination or expiration of this SOW, whichever is earlier. In no event will either party to this SOW be liable for incidental, consequential, punitive, indirect or special damages, including, without limitation, interruption or loss of business, profit or goodwill.  In no event shall Insight Global’s liability to Client exceed the fees received from Client under this SOW during the six (6) month period preceding the claim to which the liability relates, whether arising from an alleged breach of this SOW, an alleged tort, or any other cause of action.

9.	CONVERSION
9.1	If Client or any affiliate, directly or indirectly hires, employs, or otherwise any Insight Global contractor performing work for Client under this SOW prior to the Insight Global contractor’s completion of one hundred eighty (180) days of continuous service, Client shall pay to Insight Global a placement fee of twenty-five percent (25%) of the Insight Global contractor’s expected annual salary upon hire.

10.	NOTIFICATION 
10.1	Contractor shall immediately notify  CORPORATION regarding any problems which may significantly affect performance of Work. 
10.2	Contractor will provide weekly concise reports highlighting project progress in order to communicate progress, action items, and safety incidents.
10.3	 CORPORATION and Contractor will have constant status updates and weekly progress meetings to review and discuss project results and/or status. The cadence of the meetings can be updated as agreed upon by both parties.

11.	WORK LOCATION 
11.1	Work shall be completed on-site at the location provided by  CORPORATION.

12.	CONTRACTOR RESPONSIBILITIES
12.1	Contractor will provide a team consisting of the following skillsets.
12.1.1	Enterprise AI Architect 
12.1.2	Project Manager
12.1.3	Data Scientist
12.1.4	Data Engineer (As Needed)
12.1.5	AI Specialist (As Needed)
12.1.6	Business Analyst (As Needed)
12.1.7	Junior UI Developer (As Needed)
12.1.8	Senior UI Developer (As Needed)
12.1.9	Scrum Master (As Needed)

13.	CLIENT RESPONSIBILITIES
13.1	 CORPORATION will provide the following:
13.1.1	Onsite contact and direction as necessary.  
13.1.2	Access to necessary internal systems. 
13.1.3	Provide hardware necessary to program work (laptops, monitors, headset, ect)
13.1.4	Provide business and domain experts for Contractor to consult with throughout the engagement.
13.1.5	Data Engineer(s) and Data Architect to review the current state architecture and pipeline.
13.1.6	 CORPORATION credentials suitable for performing required work as outlined in this CWA.
13.1.7	 CORPORATION personal credentials for Contractor resources. 
13.1.8	Requirements for reporting and tracking of work as outlined in this CWA.

14.	REPORTING
14.1	Contractor shall provide progress reports in the format and manner directed by  CORPORATION.   If no method is specified, Contractor shall provide written reports by close of business each Tuesday, summarizing Work progress for the preceding week.  
14.2	Contractor shall immediately report to  CORPORATION any potential delays, scheduling issues, safety incidents, or other concerns which may reasonably impact project scope, schedule, or cost.  

15.	SAFETY REQUIREMENTS 
15.1	Insight Global shall comply with all safety requirements listed in the  CORPORATION Standards. 

16.	PRICING 
16.1	The maximum amount of this Contract is $466,653.20 and shall not be exceeded without prior written authorization from  CORPORATION.     
16.2	Contractor shall complete Work on a Time & Materials basis as outlined in “Attachment A” of this SOW.
16.3	Any requested changes to compensation, including but not limited to Contractor’s fees or rates, requires prior review and approval by  CORPORATION through a fully-executed Change Order.  
16.4	Reimbursable Expenses
16.4.1	Reimbursable Expenses are subject to  CORPORATION prior written approval and shall be in accordance with the Contract requirements.

17.	CHANGE PROCESS
17.1	Either party may request a change subject to terms set forth in the SOW by submission of a written change request to the project manager representing the other party. An approved template which may be used for such purposed is attached hereto as Attachment “C”, "Change Order." Approved Change Orders properly executed by Insight Global and Client will formally amend this SOW. IN WITNESS WHEREOF, the signatories below hereto have caused this SOW to be executed by their duly authorized representatives effective as of the effective date of this SOW.

18.	SPECIFICATIONS AND REQUIREMENTS 
18.1	Each of the following documents is attached to this Scope of Work and incorporated herein by reference. 


INSIGHT GLOBAL, LLC:	CLIENT:  
By:  			By:  		
Name: 			Name: 		
Title: 	________________________________	Title: 	________________________________
Date: __________________________________		Date: __________________________________	

END OF STATEMENT OF WORK
"""

drafting_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", user_template)
    ]
)

user_chat_prompt = """
 SOW is alrady generated and now we need to refine it based on the user_query provide below.
 This is the user_query - {user_query}

 ## Previously Generated SOW: 
 {previous_sow}

 ## Instructions:
  - Use the user_query to refine the previously generated SOW.
  - Ensure that previously generated SOW is not lost and only the necessary changes are made.
  - Ensure that the final output is a valid JSON document with all required fields.

 ## Feedback Errors
    {feedback}
    <!-- Any feedback or errors from different state that needs to be considered -->
"""

drafting_chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", user_chat_prompt)
    ]
)
