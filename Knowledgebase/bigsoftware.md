# Title: Initiate a Sourcing Request

## Section 1: Initial Question
### Question: 
Do you want to make changes to an existing Contract? (Yes/No)

#### Options:
- Yes
- No

#### Instruction:
- If “Yes,” the user needs to indicate the Contract Worker (CW) they want to change.

## Section 2: Contract Selection
### Search Bar:
#### Prompt:
- “Please select the contract you would like to work with”

#### Search Criteria:
- Contract Name
- Contract ID
- Third Party
- Contract Manager

## Section 3: Additional Information
### Contract Status:
- If the contract is expired, the user can request an extension/renewal within 1 month after expiry.
- If the contract is in draft amendment status, it must be published first before raising another amendment/extension/renewal.

### Support Contact:
- Contact Chain IQ or Support Team if needed.

## Section 4: Navigation
- **Back Button**
- **Continue Button** (Inactive until selection is made)

# Title: Initiate a Sourcing Request

## Section: Initiative Description

### Link:
- **See sourcing questions**: Provides additional guidance or frequently asked questions related to the sourcing process.

### Field: Title (max. 120 Characters)
#### Prompt:
- "Please provide a short descriptive title following the Naming Convention."

#### Instruction:
- The title should be concise and adhere to the UBS Naming Convention.

#### Tooltip:
- The short description will be shared with GenIQ for their activities.

### Field: Objectives & Deliverables (min. 255 Characters)
#### Prompt:
Please specify:
- Business need
- Project scope
- Deliverables expected
- Impact if not approved
- Type of contract to be signed with selected vendor (supply order, master agreement, etc.)
- Type of cost (one-time, recurring, etc.)

#### Instruction:
- This detailed description helps ChainIQ understand what the sourcer needs to work on the request. It is also picked up in a report that goes into the group tech approval forum.

### Additional Information:
#### Naming Convention:
- Users are reminded to follow the UBS Naming Convention when choosing a name for their request. A link to "Request Naming Convention" is provided for detailed guidelines.

# Title: What is the type of Good or Service?

## Section 1: Prompt
- "Please make sure you select the correct type. If you are not sure and need further advice, please contact your local Client Service Desk."

## Section 2: Select the appropriate Category
### Search Bar:
- Users can search for their category.

### Dropdown Menu:
- Lists various categories such as:
  - Awards
  - Legal
  - LP Cloud Move Test - L1
  - Market Data Services (MDS)
  - Marketing & Comm.
  - Money Managers Services
  - Personnel Services
  - Post Trades (Post Trade Providers)
  - Real Estate and Logistics
  - Test Postores01

## Section 3: Selection Example
### Selected Category:
- IT Software > Application Service Providers - XaaS (IaaS, StaaS, etc.)

### Tooltip:
- There are two levels of selection:
  1. IT Software
  2. XaaS

## Section 4: Additional Information
### Expected Amount:
- The expected amount will be automatically split by calendar year.
- Users can manually change the allocation if needed.

### Start & End Date:
- Should represent the foreseen time frame for the provision/contract.

## Section 5: Navigation
### Field to Add Expected Amount:
- Users can specify the expected amount, currency, exchange rate, and total USD.

# Title: What is the type of Good or Service?

## Section 1: Selected Category
### Example:
- Personnel Services > Employee benefits

## Section 2: Prompt
- "At least one entry is required"

### Field: Type of Good/Services

## Section 3: Deal Financials and Duration
### Prompt:
- "Provide your available money to spend"

### Fields:
- **Start Date:** DD.MM.YYYY (Required)
- **End Date:** DD.MM.YYYY (Required)
- **Expected Amount:** (Required)
- **Add Button:** To add the financial details.

## Section 4: Popup: Category Selection
### Message:
- "Please note that the category choice will drive the further process. Please make sure you add all applicable subcategories."
- "If you need to change your category choice later, you may have to perform certain process steps again, even if the request has already reached the contract signature stage."

### Confirm Button:
- Users need to confirm their category selection to proceed.

## Section 5: Additional Information
### Expected Amount:
- Note that the expected amount will be automatically split by calendar year.
- Users can still change the allocation manually if needed.

### Start & End Date:
- Should represent the foreseen time frame for the provision/contract.

# Title: Deal Financials and Duration

## Section 1: Field - Deal Presenter
### Prompt:
- "Who presents in the approval forum the request"

## Section 2: Deal Financials and Duration
### Prompt:
- "Provide your available money to spend"

### Fields:
- **Start Date:** DD.MM.YYYY (Required)
- **End Date:** DD.MM.YYYY (Required)
- **Expected Amount:** (Required)
- **Year, Currency, Expected Amount, Exchange Rate, Total USD:** Table format for entering multiple entries.
- **Add Button:** To add the financial details.

### Fields:
- **Funding Type:**
  - Dropdown with options such as:
    - D & E (Development and Engineering)
    - SD (Service Delivery)
  - Tooltip: Glemo struggled a bit to find this code.

- **Cost Center:**
  - Example:
    - **OU (Base):**
      - LKG-C - Process Design & Transformation
    - **Cost Center:**
      - RCE2 - Customer Buy Exp and SC Transform CH
    - **GCRS Company:**
      - CB40 - UBS BSA (CH Ops) - Zurich
    - **OU (Deployment):**
      - LKG-C - Process Design & Transformation
    - **Cost Center:**
      - RCE2 - Customer Buy Exp and SC Transform CH
    - **GCRS Company:**
      - CB40 - UBS BSA (CH Ops) - Zurich

## Section 3: Additional Information
### Expected Amount:
- The expected amount will be automatically split by calendar year.
- Users can still change the allocation manually if needed.

### Start & End Date:
- Should represent the foreseen time frame for the provision/contract.

# Title: Cost Breakdown

## Section 1: Cost Breakdown
### Prompt:
- "Provide the cost breakdown for mentioned Expected Amount"

### Field: Spend Type
#### Options:
- Software - Internally Generated
- Software - Expensed
- Software Maintenance
- Software - Purchased
- Software Maintenance - Expensed
- Licenses
- Yash_Contract start
- Yash_Purchase date

#### Selected Example:
- Software - Internally Generated

### Field: Expected Delivery Date
#### Example Date:
- 18.08.2024

### Field: Cost
#### Example Cost:
- USD 1500000

### Add Button:
- Adds the cost breakdown entry to the table below.

## Section 2: Table
### Columns:
- Spend Type
- Expected Delivery Date
- Currency
- Breakdown Cost
- Total USD

### Prompt:
- "At least one entry is required"

## Section 3: Instruction
### Steps to follow:
1. Select spend type.
2. Insert date.
3. Insert cost.
4. Click on Add.
5. The item appears in the table below.

### Tooltip:
- You can split among spend types.

## Section 4: Additional Information
### Notification:
- "This amount will be frozen from your Business Division / Group Functions Function’s Consulting Operating Plan."

# Title: Is the spend funded out of the integration budget?

## Section 1: Question
### Question:
- "Is the spend funded out of the integration budget?"

#### Options:
- Yes
- No

#### Tooltip:
- "A spend is funded out of integration budget when the costs will be charged to a dedicated integration cost center(s)."

## Section 2: Additional Information for Global Software Asset Management (GSAM) Team

### Question:
- "Do we intend to replace an existing technology?"

#### Options:
- Yes
- No

### Field: Duration for Decommission
#### Prompt:
- "What is the technology being replaced and the timeline to decommission the existing technology?"

# Title: AppDir: Application, UBS Products, and Vendor Products

## Section 1: Question
### Question:
- "Do you already know the software you are buying?"

#### Options:
- Yes
- No

#### Tooltip:
- "For big new products, probably the answer is 'No,' and there is a tender to be done."

## Section 2: Instruction
- "Once you have selected the software, it will need to be registered in the Application directory."

### Link:
- Provides a link to the Application directory for registering the software.

### Note:
- "The application and Product ID will need to be provided latest at the Contract Manager confirmation prior to the Contract signature."

# Title: AppDir: Application, UBS Products, and Vendor Products

## Section 1: Question
### Question:
- "Do you already know the software you are buying?"

#### Options:
- Yes
- No

#### Tooltip:
- "For big new products, probably the answer is 'No,' and there is a tender to be done."

## Section 2: Instruction
- "Once you have selected the software, it will need to be registered in the Application directory."

### Link:
- Provides a link to the Application directory for registering the software.

### Note:
- "The application and Product ID will need to be provided latest at the Contract Manager confirmation prior to the Contract signature."

## Section 3: Field - GUID, NAME or ShortName
### Example Entry:
- arib

### Dropdown Menu:
- Suggestions such as:
  - 6360ED0DDBD749998644208214079BCB (SAP ARIBA, Ariba)
  - 69E0E6A3277B44A5B2B89D70759F6E65 (BNP Paribas Online Portal, BNP Login)
  - A33AA81A5F94BD592FE5628C3D1D174 (BNP PARIBAS PBLINK, BNP)
  - B9C388115F9497AF8D4F76F3CC675C (BNP Paribas, BNP Paribas)

## Section 4: Field - Apps or UBS Products
### Example Entry:
- Cirutuo Category Mgmt

### Prompt:
- "At least one entry is required"

## Section 5: Button - Add
- Adds the selected application to the table below.

## Section 6: Instruction
### Steps to follow:
1. Select the application.
2. Check the product and permit.
3. Click on “Add.”
4. The app disappears from this field and appears in the table below.

---

# Title: AppDir: Application, UBS Products, and Vendor Products

## Section 1: Field - Vendor Product
### Prompt:
- "Please select all Vendor Products"

### Field:
- "Vendor Product *"

### Add Button:
- Adds the selected vendor product to the table below.

## Section 2: Table
### Columns:
- Category
- IT Capability 1
- IT Capability 2
- Vendor
- Vendor Product
- Standard Status
- Action

### Example Entry:
- **Category:** Business Applications
- **IT Capability 1:** Supply Chain Management
- **IT Capability 2:** Procurement and Supply Chain
- **Vendor:** SAP
- **Vendor Product:** Procure-to-Pay (P2P)
- **Standard Status:** Standard

---

# Title: Chain IQ Involvement

## Section 1: Chain IQ Involvement
### Instruction:
- "For additional clarity, please refer to the Countries in scope and Category overview."

### Note:
- "Countries in scope" = PDF file
- "Category overview" = Excel file

## Section 2: Question
### Question:
- "Can you confirm that Chain IQ will be involved in the process?"

#### Options:
- Yes
- No

#### Additional Field if “No” is selected:
### Question:
- "Reason for not involving Chain IQ"

#### Dropdown Options:
- Sensitive/Confidential Project
- Internal Consulting
- Below CIQ involvement threshold for the category/country not covered by CIQ

#### Tooltip:
- "If you say ‘No,’ you need to say why."
- "Sensitive/Confidential" goes directly to the supply chain.
- "Below CIQ involvement" goes to the PNSS team.

## Section 3: Expandable Sections:
- Specify a different Contract Manager
- Confirm/Change the Cost Commitment Approvers
- Business/Budget Owner outside the Contract Manager’s Segment
- Attachments

# Title: Confirm/Change the Cost Commitment Approvers

## Section 1: Confirm/Change the Cost Commitment Approvers
### Instruction:
- "Approvers are defaulted to the Contract manager reporting line (minimum ranks to meet the policy). These can be changed to another person of the required rank."

### Note:
- "You can change the approver, and the list is already filtered for the right seniority."

### Fields:
- **Cost Commitment Approver 1**
  - Example: Lardera, Ludovica (43501188)
  - Minimum Rank: Managing Director

- **Cost Commitment Approver 2**
  - Example: Egger, Harald (00101069)
  - Minimum Rank: Managing Director

---

# Title: Business/Budget Owner outside the Contract Manager’s Segment

## Section 1: Business/Budget Owner outside the Contract Manager’s Segment
### Question:
- "Which part of UBS is the business/budget owner?"

### Fields:
- **Division:**
  - Example: Group Functions

- **Area:**
  - Example: Group Corporate Services

- **Unit:**
  - Example: Grp Human Resources & Corporate Services

- **Sector:**
  - Example: Supply Chain

- **Segment:**
  - Example: Supply Chain (sg)

## Section 2: Attachments
- Allows for adding attachments relevant to the request.

## Section 3: Additional Info
### GCRS Info:
- "The information entered here will drive the business approval."

---

# Title: Attachments

## Section 1: Attachments
### Prompt:
- "Provide supporting documents for your request."

### Fields:
- **Description:**
  - Add a brief description of what the document relates to.

- **File Upload:**
  - Drag and drop a file to attach, or browse to select a file.

## Section 2: Add Button
- Adds the attachment to the request.

---

# Title: Risk Applicability

## Section 1: Risk Applicability
### Request ID:
- Example: Test GL 1306 (Request ID: 365500)

### Guidance Links:
- ROCC, BCM, Records Management, Intermediary Service, Data Handling, 3PISA, Subcontractor

## Section 2: Subsection: Outsourcing
### Regulatory Outsourcing Control Check (ROCC)
- "Because you have picked the categories noted below, you are required to complete a risk assessment for Regulatory Outsourcing Control Check."

### Table:
#### Columns:
- L1
- L2
- L3
- L4
- Outsourcing Relevant

#### Example Entry:
- IT Software, Application Service Providers, Yes

### Questions:
- "Does the service fall under any of the following categories that are typically not considered as outsourcing services?"

#### Options:
- Third Party staff augmentation, staff operating on UBS premises under UBS’s direct supervision and control
- Relationships with correspondent banks, agents, and custodians (internal and external)
- Clearing and settlement arrangements between clearing houses, central counterparties, and settlement institutions and their members
- Market information services (e.g., Bloomberg, Moody’s, Standard & Poor’s) and common network infrastructure (e.g., Visa, Mastercard)
- Functions that are legally required to be performed by external providers (e.g., statutory audit)
- Purchasing of goods; facilities management (consisting of the following services: cleaning, gardening, catering, vending, clerical, travel, and premises maintenance, design, and build-out)
- Law firms and consultants providing advice; health insurance
- Telecommunication services and public utilities
- None of the above

### Additional Questions:
- "Does the service fall under any of the types of activities that are considered as ineligible for outsourcing as per the TPRM Guideline?"

#### Options:
- Yes
- No

## Section 3: Data Inconsistencies Popup
### Message:
- "While the category selected is considered outsourcing relevant, your response indicates that the request includes activities ineligible for outsourcing. Please reach out to the ROCC Support Team for guidance on the inconsistency."

### Buttons:
- ROCC Support Team, Close

#### Tooltip:
- "This is a double check; if you flag ‘Yes,’ this pop-up appears."

---

# Title: Regulated Activity / Internal Control Function / Risk Function

## Section 1: Regulated Activity / Internal Control Function / Risk Function
### Question:
- "Does the outsourcing include a regulated activity, parts of a UBS control function or parts of a UBS risk function?"

#### Options:
- Yes
- No

#### Tooltip:
- Following questions appear if “No” is selected.

## Section 2: Complexity of the outsourced activities
### Instruction:
- "To comply with regulatory requirements, we need to assess the complexity of the outsourced services. As such, please provide responses to the following questions to support the determination of complexity of the outsourcing."

### Question:
- "Does your initiative involve outsourcing of UBS employees/resources to the vendor only or does it involve also other elements (e.g., IT infrastructure)?"

#### Options:
- Mainly outsourcing of employees
- Outsourcing includes other elements as well

### Question:
- "What is the estimated percentage of employees/resources outsourced vs. the total number of employees managing the process and/or retained internally at UBS?"

#### Options:
- ≥ 50%
- 30-50%
- < 30%

#### Tooltip:
- This question is a follow-up to the previous one.

# Title: Additional Outsourcing Questions

## Section 1: Questions
### Question:
- "Does the outsourcing involve managed services including transfer of knowledge and/or core capabilities to the service provider?"

#### Options:
- Yes
- No
- Other

### Question:
- "Will the cost to run the outsourced process and service become a barrier to exit the relationship with the vendor and internalize?"

#### Options:
- Very likely
- Likely
- Unlikely

### Question:
- "Is the estimated cost to insource the service/process (transition/change-the-bank cost) expected to supersede the amount we will pay to the vendor to run the service/process?"

#### Options:
- Transition cost to insource will be ≥ 3 times the annual vendor fees to provide the service
- Transition cost to insource will be 1-3 times the annual vendor fees to provide the service
- Transition cost to insource will be < 1 times the annual vendor fees to provide the service

### Question:
- "How long will it take to internalize the process/service covered by this sourcing request or to transition it to another service provider once it has been outsourced?"

#### Options:
- ≥ 12 months
- 7-11 months
- 6 months or less

---

# Title: Business Continuity Management (BCM)

## Section 1: Business Continuity Management (BCM)
### Fields:
- **BCM Critical:** Yes/No
- **BCM Tier:** NA

## Section 2: Business Activity and DRP Dependency
### Instruction:
- "Please select all the UBS Business Activities and DRPs that the third party contract will support."

### Note:
- DRP = Departmental Recovery Plan
- Users will need help from the BCM team to get clarifications to fill this part of the questionnaire.

### Fields:
- **Region**
- **Country**
- **City**
- **Division**
  - Example: Group Functions
- **Unit**
  - Example: Grp Human Resources & Corporate Services
- **Sector**
  - Example: Supply Chain
- **Area**
  - Example: Group Corporate Services
- **Business Activities in Scope**
  - Example: GCS - Real Estate & Services
- **Applicable UBS DRP**
  - Example: 19255-DRP-Group Functions-Americas-Grp Human Resources & Corporate Services

## Section 3: Table
### Columns:
- BA ID
- Business Activities in Scope
- UBS DRP ID
- Applicable UBS DRP
- Tier
- IBS Relevant
- Action

### Example Entry:
- **BA ID:** 5332
- **Business Activities in Scope:** GCS - Real Estate & Services
- **UBS DRP ID:** 19255
- **Applicable UBS DRP:** Unknown
- **Tier:** Tier 3
- **IBS Relevant:** No

## Section 4: Additional Information
### Instruction:
- Use the GCRS hierarchy filters (Division/Unit/Area, etc.) that the third-party contract supports to find the correct Business Activity (BA) and Departmental Recovery Plan (DRP) as per the UBS Business Continuity Application (BCA) in BCM that the third-party contract supports.

### Note:
- You do not have to select all filters, and the filter data will not be stored. However, being more specific will reduce the number of potential BAs and DRPs to choose from.

---

# Title: Data Handling

## Section 1: Data Handling
### Instruction:
- "Select the category of UBS data that the vendor/third party is supposed to process, use or otherwise come into possession of."

### Dropdown Options:
- Strictly Confidential
- Confidential
- Internal
- Public/None

### Note:
- Different flags appear below depending on the selected item.

## Section 2: Questions
### Question:
- "Select all applicable categories of data which the third party will process (incl. access, handle and/or storage) outside of UBS premises/systems:"

#### Options:
- **Client Identifiable Data (CID)**
  - Yes
  - No

#### If Yes:
- **Type of clients the CID relates to:**
  - Individual/Natural person clients
  - Institutional/Corporate clients
  - Prospective clients

- **Business Division Owning the data:**
  - Group Functions
  - Wealth Management
  - Wealth Management Americas
  - Personal & Corporate Banking
  - Investment Bank
  - Asset Management

- **CID Type:**
  - Category A: Direct CID
  - Category B: Indirect sensitive IDs for CID
  - Category C: Combination of multiple attributes which may result to CID
  - Category D: Non-sensitive identifiers (NSI) substituting Category A and/or Category B

- **Employee Identifiable Data (EID)**
  - Yes
  - No

- **Unpublished Price Sensitive Information (UPSI)**
  - Yes
  - No

## Section 3: Additional Information
### Note:
- Guidance in infoboxes and additional links to deep dive.
- Provided indicative assessments on the above data points, to the best of your understanding of the scope of your proposed engagement. These data points can be updated once the engagement is final.

---

# Title: Data Handling (Public/None)

## Section 1: Data Handling
### Instruction:
- "Select the category of UBS data that the vendor/third party is supposed to process, use or otherwise come into possession of."

### Dropdown Options:
- Strictly Confidential
- Confidential
- Internal
- Public/None

### Note:
- If “Public/None” is selected, the checkboxes for selecting data categories are disabled.

## Section 2: Questions
### Question:
- "Select all applicable categories of data which the third party will process (incl. access, handle and/or storage) outside of UBS premises/systems:"

#### Options:
- **Client Identifiable Data (CID)**
  - Yes (Disabled if “Public/None” is selected)
  - No (Disabled if “Public/None” is selected)

- **Employee Identifiable Data (EID)**
  - Yes (Disabled if “Public/None” is selected)
  - No (Disabled if “Public/None” is selected)

- **Unpublished Price Sensitive Information (UPSI)**
  - Yes (Disabled if “Public/None” is selected)
  - No (Disabled if “Public/None” is selected)

## Section 3: Additional Information
### Note:
- Provided indicative assessments on the above data points, to the best of your understanding of the scope of your proposed engagement. These data points can be updated once the engagement is final.

---

# Title: Information Security (3PISA)

## Section 1: Information Security (3PISA)
### Note:
- 3PISA = Old name of OCRA.

### Instruction:
- Explanation about data accessibility based on environment control.

## Section 2: Questions
### Question:
- "Is the service or product provided by the third party supplied solely from UBS premises or an approved Vendor ODC?"

#### Options:
- Yes
- No

### Question:
- "Will the third party access, transport, store, archive, process or destroy UBS data?"

#### Options:
- Yes
- No

### Question:
- "Will the service or product involve the use of a third party application or permanent network connectivity to UBS?"

#### Options:
- Yes
- No

### Question:
- "Does the service involve XaaS?"

#### Options:
- Yes
- No

#### Tooltip:
- XaaS: Anything as a Service (e.g., Software as a Service, Infrastructure as a Service).

# Title: Records Management (RM)

## Section 1: Records Management (RM)
### Instruction:
- "Please evaluate whether specific records management requirements must be followed when engaging with the vendor by selecting the correct scenario."

### Questions:
- "What is the purpose of the contract and will records be processed?"
- "Will the request contain the purchase of solely physical goods or supply of a service where no UBS records will be processed?"

#### Options:
- Yes
- No

#### Note:
- If "No" is selected, additional questions appear.

## Section 2: Additional Questions (if "No" is selected)
### Question:
- "Please select the applicable option:"

#### Options:
- Final work product from the service (e.g., office files, PDF document) qualifies as a record and will be provided to a UBS person.
- Supply of a service using UBS infrastructure where UBS records will be created, processed or stored on UBS infrastructure/using UBS software.
- Supply of a service using vendor infrastructure. UBS records will be created, processed or stored using vendor’s software.

## Section 3: Additional Information
### Support:
- For further assistance, consult the Records Management Guidelines or watch the video.

### What qualifies as a Record?
- Records are a subset of information that memorialize and provide objective evidence of activities and transactions performed, events that occurred, results achieved, or statements made.

### How to identify Records?
- CASIR is your digital companion for assessing your information asset for mandatory policy requirements. The outcome of CASIR, in combination with your knowledge about the purpose of the contract/service to be provided, will enable you to determine the appropriate scenario.

### Note:
- RM is not segmentation relevant - within UBS, we segment contracts and the result of the segmentation is (critical - high - medium - low - very low risk).

---

# Title: Intermediary Service

## Section 1: Intermediary Service
### Question:
- "Will the vendor act as an Intermediary or provide any Intermediary services on behalf of UBS?"

### Definition:
- Intermediaries are individuals or entities that provide services which involve interacting, on UBS’ behalf, with an external party (e.g., a client, public official), for UBS’ benefit or business advantage.

#### Options:
- Yes
- No

#### Note:
- This section is not segmentation relevant.

---

# Title: Risk Applicability Summary

## Section 1: Risk Applicability Summary
### Details:
- Request ID and Test GL number.

### Instructions:
- Review the data before submitting to avoid repeating steps.

## Section 2: Risk Assessments to Trigger
### Regulatory Outsourcing Control Check (ROCC)
#### Status:
- Yes

#### Instructions:
- Raise a ROCC request or link an existing ROCC to this sourcing request in ServiceNow.
- Additional guidance provided through a link.

### Complexity of the Service/Contract
#### Status:
- Medium

### Regulated Activity/Internal Control Function/Risk Function
#### Status:
- Yes

### BCM Critical (BCM Tier)
#### Status:
- No

### 3PISA Required
#### Status:
- Yes

#### Instructions:
- Raise a 3PISA request as soon as the vendor is selected.
- If there is an existing 3PISA assessment covering the requested service, link it to the request later in the process.
- Further guidance provided through a link.

### Other Service-related Risks to be Considered
#### Instructions:
- Ensure all applicable activities are performed and relevant clauses are included in the contract.

### CID Access
#### Status:
- Yes

#### Instructions:
- Applicable clauses/exhibits will be included in the contract by Chain IQ. If Chain IQ is not involved, include them yourself.
- Additional advice provided through guidelines link.

### EID Access
#### Status:
- Yes

#### Instructions:
- Applicable clauses/exhibits will be included in the contract by Chain IQ. If Chain IQ is not involved, include them yourself. Additional advice provided through a link.

### Personal Data
#### Status:
- Yes

### UPSI (Unpublished Price Sensitive Information)
#### Status:
- Yes

#### Instructions:
- Applicable clauses/exhibits will be included in the contract by Chain IQ. If Chain IQ is not involved, include them yourself. Additional advice provided through a link.

### Data Classification
#### Status:
- Internal

### Records Management
#### Status:
- No

### Intermediary Service
#### Status:
- No

### SLA Required
#### Status:
- Yes

#### Instructions:
- An SLA is required and must be included in the contract by Chain IQ. If Chain IQ is not involved, include them yourself. Refer to the SLA Framework to ensure compliance.

### Subcontractor Assessment Required
#### Status:
- Yes

#### Instructions:
- If Chain IQ is not involved, ask the vendor to fill out the subcontractor questionnaire provided later in the process and upload it.

## Section 3: Actions
### Buttons:
- Save & Close
- Edit
- Submit

---

# Title: Risk Applicability Summary (Explanation)

## Purpose:
This screen provides a summary of the risk assessments required for a specific sourcing request (Test GL 1306 with Request ID: 365500). It outlines the different risk checks that need to be initiated and ensures that all relevant clauses are included in the contract.

## Sections:
### Risk Assessments to Trigger

#### Regulatory Outsourcing Control Check (ROCC)
##### Status:
- Yes

##### Action:
- Raise a ROCC request or link an existing ROCC to this sourcing request in ServiceNow.
- Additional Guidance: A link is provided for further guidance on the ROCC process.

#### Complexity of the Service/Contract
##### Complexity Level:
- Medium

#### Regulated Activity/Internal Control Function/Risk Function
##### Status:
- Yes

#### BCM Critical (BCM Tier)
##### Status:
- No

#### 3PISA Required
##### Status:
- Yes

##### Action:
- Raise a 3PISA request as soon as the vendor is selected.
- If there is already an existing 3PISA assessment covering the requested service, link it to the request later in the process.
- Additional Guidance: A link is provided for further guidance on the 3PISA process.

#### Other Service-Related Risks to Be Considered

##### CID Access
###### Status:
- Yes

###### Guidance:
- The applicable clauses/exhibits will be included in the contract by Chain IQ. If Chain IQ is not involved, you need to include them yourself.

##### Personal Data
###### Status:
- Yes

##### UPSI (Unpublished Price Sensitive Information)
###### Status:
- Yes

###### Guidance:
- The applicable clauses/exhibits will be included in the contract by Chain IQ. If Chain IQ is not involved, you need to include them yourself.

##### Data Classification
###### Status:
- Internal

##### Records Management
###### Status:
- No

##### Intermediary Service
###### Status:
- No

##### SLA Required
###### Status:
- Yes

###### Guidance:
- An SLA is required and must be included in the contract by Chain IQ. If Chain IQ is not involved, you need to include them yourself.

##### Subcontractor Assessment Required
###### Status:
- Yes

###### Guidance:
- If Chain IQ is not involved, you need to ask the vendor to fill out the subcontractor questionnaire provided later in the process and upload it.

### Insights:
- Comprehensive Risk Assessment: This summary ensures that all necessary risk assessments are identified and actions are outlined to mitigate potential risks.
- Guidance and Links: The inclusion of links and additional guidance provides users with easy access to more detailed information and helps ensure compliance with internal policies.
- Status Indications: The status (Yes/No) clearly indicates which risk assessments are required, helping users prioritize their actions.

This summary is crucial for ensuring that all relevant risk assessments are completed and that the sourcing request complies with regulatory and internal standards. By following the outlined actions and guidance, users can efficiently manage the risk assessment process.

---

# Title: Approver Side - Demand Approval Process

## Purpose:
This screen shows the steps in the demand approval process and the status of each step.

## Sections:
### Submit Request:
- This is the initial submission of the request.

### Cost Commitment Approvals by Finance Policy:
- The first cost commitment approver reviews and either approves or returns the request.

### Form Change:
- This indicates any necessary changes or corrections to the form.

### Supply Chain Steps:
- Subsequent steps handled by the supply chain team.

## Details:
### Process Step:
- Describes the current step in the process.

### Activity:
- Specific actions taken in each process step.

### Owner:
- Person responsible for the action.

### Completion Date:
- Date when the action was completed.

### Status:
- Current status of the action, such as "Returned" or "Pending".

### Days:
- Number of days taken for the step.

### Returned Status:
- Indicates that the request was returned by the approver for further edits. The requester can make the necessary changes and resubmit.

### Pending Status:
- Indicates that the request is currently awaiting action.

The information provided in this step-by-step guide details the submission, approval, and correction process for a sourcing request. Each step is documented with its purpose, action required, and relevant fields, making it easier to understand the workflow and ensure all necessary information is included for a successful submission.

---

# Title: Approver Dashboard - Overview

## Purpose:
This screen shows the approver's dashboard where they can view and manage requests for approval.

## Sections:
### Pending:
- Requests awaiting approval.

### Approved:
- Requests that have been approved.

### Rejected:
- Requests that have been rejected.

## Details:
### Search Bar:
- Allows the approver to search for specific requests using various filters such as Request ID, Requestor, Type, Category, Approval Step, and Region.

### Download Table:
- Provides an option

# Title: Approver View - Cost Commitment Approval

## Purpose:
This screen shows the detailed view for cost commitment approval within the approver dashboard.

## Sections:
### Cost Commitment:
- Section where the cost commitment approvals are managed.

### First Cost Commitment Approver:
- Displays the first approver's name, status, and decision options.

### Second Cost Commitment Approver:
- Displays the second approver's name, status, and decision options.

### Business Approvers:
- Section for business role-based approvers.

## Details:
### Approval Type:
- Indicates the type of approval required (Cost Commitment, Business, etc.).

### Approver:
- Shows the name and ID of the approver.

### Decision:
- Dropdown menu for the approver to choose between "Approve" and "Return to Requestor".

### General Comment:
- A field for the approver to provide additional comments or feedback related to the approval decision.

## Insights:
### Parallel Approvals:
- Multiple approvers can review and approve the request in parallel, streamlining the approval process.

### Decision Options:
- Approvers can either approve the request or return it to the requestor for further modifications.

### Stage Control:
- Depending on the stage of the process, a returned request can either go back one step or to the beginning, ensuring thorough review and compliance.

This detailed view for cost commitment approval allows approvers to efficiently manage and track their assigned approvals. By having the option to approve or return requests with comments, approvers can ensure that all necessary information and compliance measures are met before proceeding.

---

# Title: Overview - Approval Process

## Purpose:
This screen provides an overview of the approval process for a sourcing request, detailing each step, the responsible owner, status, and completion dates.

## Sections:
### Demand Approval:
#### Submit Request:
- **Owner:** Requestor (Locci, Glemo)
- **Completion Date:** 13.06.2024
- **Status:** Submitted

#### Cost Commitment Approvals by Finance Policy:
- **First Cost Commitment Approver:** Lardera, Ludovica
- **Second Cost Commitment Approver:** Kamm, Adrian
- **Status:** Pending

### Contracting:
#### Draft Contract (Supply Chain):
- **Draft Contract Upload by Sourcer:** Multiple owners, status: Upcoming
- **Contract Manager Confirmation:** Locci, Glemo, status: Upcoming

### Risk Assessments:
#### Pre-contract Risk Checks as Required by TPRM:
- **Operational Consolidated Risk Assessment:** sh-ocra@ubs.com, status: Not Passed
- **Legal Contract Check:** Multiple owners, status: Upcoming
- **Pre-Signature Compliance Check:** Multiple owners, status: Upcoming

### Contract Approvals:
#### Final Contract Reviews and Approvals:
- **GSAM Approval:** Multiple owners, status: Upcoming
- **Commercial Approval:** Multiple owners, status: Upcoming
- **Commercial Approval Forum (CAF):** Multiple owners, status: Upcoming

## Details:
### Process Step:
- Each major phase of the approval process (Demand approval, Contracting, Risk assessments, Contract approvals).

### Activity:
- Specific actions or tasks within each process step.

### Owner:
- The individual(s) responsible for completing the activity.

### Completion Date:
- The date by which the activity should be completed.

### Status:
- The current state of the activity (Submitted, Pending, Upcoming, Not Passed).

### Days:
- Number of days spent or required for the activity.

## Insights:
### Sequential and Parallel Approvals:
- The process includes both sequential steps and tasks that can be managed in parallel by different owners.

### Clear Responsibilities:
- Each task is assigned to specific individuals or groups, ensuring accountability and clear workflow.

### Status Tracking:
- The dashboard allows easy tracking of the progress and current status of each task, aiding in timely follow-ups and completion.

This overview provides a comprehensive snapshot of the entire approval process, from the initial request submission to final contract reviews. By detailing the responsible parties and status of each task, it ensures transparency and efficient management of the sourcing request.

---

# Title: Approver Process Summary

The approver process in the UBS sourcing system involves multiple steps and roles to ensure that sourcing requests are thoroughly reviewed and approved in compliance with internal policies and regulatory requirements. Here is a detailed summary of the process:

## 1. Submit Request
### Initiator:
- Requestor

### Activity:
- Submitting the sourcing request.

### Completion:
- Requestor completes and submits the initial request form.

### Status:
- Submitted

## 2. Cost Commitment Approvals
### First Cost Commitment Approver
#### Role:
- First-level approver responsible for reviewing the financial aspects of the request.

#### Approver Example:
- Ludovica Lardera

#### Activity:
- Reviewing and approving the cost commitment.

#### Status:
- Pending or Approved

### Second Cost Commitment Approver
#### Role:
- Second-level approver, typically with a higher authority or different focus.

#### Approver Example:
- Adrian Kamm

#### Activity:
- Further review and approval of the cost commitment.

#### Status:
- Pending or Approved

## 3. Contracting
### Draft Contract Upload by Sourcer
#### Initiator:
- Sourcer

#### Activity:
- Uploading the draft contract for the sourcing request.

#### Status:
- Upcoming or Completed

### Contract Manager Confirmation
#### Role:
- Contract Manager

#### Activity:
- Confirming the uploaded contract.

#### Status:
- Upcoming or Confirmed

## 4. Risk Assessments
### Pre-contract Risk Checks (TPRM)
#### Role:
- Multiple roles, including operational, legal, and compliance teams.

#### Activities:
- **Operational Consolidated Risk Assessment:** Performed by operational risk team.
- **Legal Contract Check:** Performed by legal team.
- **Pre-Signature Compliance Check:** Performed by compliance team.

#### Status:
- Not Passed, Upcoming, or Passed

## 5. Contract Approvals
### Final Contract Reviews and Approvals
#### Role:
- Multiple approvers, including GSAM, commercial teams, and other relevant stakeholders.

#### Activities:
- **GSAM Approval:** Review by GSAM team.
- **Commercial Approval:** Review by commercial team.
- **CAF (Commercial Approval Forum) Greater than $100K:** Review for high-value contracts.
- **Other Stakeholders:** As required.

#### Status:
- Upcoming, Approved, or Rejected

## 6. Sourcing Overview
### Assigned Sourcer
#### Role:
- Sourcer

#### Activity:
- Managing the sourcing project following the standard sourcing process.

#### Status:
- Ongoing

### Project Reference Number
#### Example:
- WS2036130211

#### Activity:
- Tracking the project in the UBS Sourcing Platform.

## 7. Final Submission and Approval
### Review of Risk Applicability Summary
#### Activity:
- Ensuring all risk assessments are completed and relevant clauses are included in the contract.

### Submission of Final Request
#### Role:
- Requestor

#### Activity:
- Submitting the final request for final approval.

#### Status:
- Submitted

## Key Considerations for Approvers:
### Parallel Approvals:
- Approvers can work in parallel, especially in the cost commitment approval stage, to expedite the process.

### Returning Requests:
- Approvers can return requests to the requestor for additional information or corrections. This step allows for iterative refinement before final approval.

### Compliance and Risk Management:
- Each approval step includes checks for compliance with internal policies and regulatory requirements, ensuring all necessary risk assessments are completed.

## Notes and Tips for Faster Approval:
### Complete Documentation:
- Ensure all required documents and information are included before submission.

### Clear Communication:
- Provide clear and concise information to avoid unnecessary returns and delays.

### Follow Guidance:
- Utilize provided links and additional guidance to ensure compliance and proper completion of each step.

### Monitor Status:
- Regularly check the status of the request and follow up with approvers if necessary to keep the process moving.

This detailed overview provides a comprehensive understanding of the approver process, ensuring all steps and requirements are clear for efficient and compliant processing of sourcing requests.

---

# Summary of All Steps:

## 1. Initiate a Sourcing Request
### Questions:
- Do you want to make changes to an existing Contract? (Yes/No)
- Select the contract to work with.

### Additional Info:
- Contract expiration, extension, and amendment details.

## 2. Initiative Description
### Fields:
- Title
- Objectives & Deliverables

### Additional Info:
- UBS Naming Convention.

## 3. What is the type of Good or Service?
### Instructions:
- Select the appropriate Category.
- Seek advice if needed.

## 4. Category Selection Confirmation
### Popup Message:
- Importance of correct category choice.

## 5. Deal Financials and Duration
### Fields:
- Deal Presenter
- Start Date, End Date
- Expected Amount
- Funding Type, Cost Center, PPM Program Code

### Additional Info:
- Details on amount splitting and date selection.

## 6. Cost Breakdown
### Instructions:
- Select spend type, date, and cost.
- Click "Add."

### Fields:
- Spend Type
- Expected Delivery Date
- Cost

### Additional Info:
- Frozen amount information.

## 7. Integration Budget
### Questions:
- Is the spend funded out of the integration budget? (Yes/No)
- Do we intend to replace existing technology? (Yes/No)

### Fields:
- Duration for Decommission.

## 8. AppDir: Application, UBS Products, and Vendor Products
### Questions:
- Do you know the software you are buying? (Yes/No)

### Instructions:
- Select the software and register it in the Application directory.

### Fields:
- GUID, NAME, or ShortName
- Apps or UBS Products
- Vendor Product

## 9. Chain IQ Involvement
### Instructions:
- Refer to the Countries in scope and Category overview.

### Questions:
- Confirm Chain IQ involvement? (Yes/No)

### Additional Field if No:
- Reason for not involving Chain IQ.

### Expandable Sections:
- Different Contract Manager
- Cost Commitment Approvers
- Business/Budget Owner outside the Contract Manager's Segment
- Attachments

## 10. Confirm/Change the Cost Commitment Approvers
### Fields:
- Cost Commitment Approver 1
- Cost Commitment Approver 2

## 11. Business/Budget Owner outside the Contract Manager's Segment
### Fields:
- Division
- Area
- Unit
- Sector
- Segment

## 12. Attachments
### Fields:
- Description
- File Upload

## 13. Risk Applicability
### Subsections:
- Outsourcing
- Regulatory Outsourcing Control Check (ROCC)
- Questions on outsourcing categories.
- Regulated Activity / Internal Control Function / Risk Function
- Complexity of outsourced activities.
- Questions on managed services, cost, and transition time.

## 14. Business Continuity Management (BCM)
### Fields:
- BCM Critical
- BCM Tier

### Subsections:
- Business Activity and DRP Dependency
- **Fields:** Region, Country, City, Division, Unit, Sector, Area, Business Activities in Scope, Applicable UBS DRP.
- **Table with BA ID, Business Activities in Scope, UBS DRP ID, Applicable UBS DRP, Tier, IBS Relevant, Action.

## 15. Data Handling
### Fields:
- Category of UBS data (Strictly Confidential, Confidential, Internal, Public/None)
- Applicable categories of data: CID, EID, UPSI.

## 16. Information Security (3PISA)
### Questions:
- Is the service or product provided by the third party supplied solely from UBS premises or an approved Vendor ODC? (Yes/No)
- Will the third party access, transport, store, archive, process or destroy UBS data? (Yes/No)
- Will the service or product involve the use of a third party application or permanent network connectivity to UBS? (Yes/No)
- Does the service involve XaaS? (Yes/No)

## 17. Records Management (RM)
### Questions:
- What is the purpose of the contract and will records be processed?
- Will the request contain the purchase of solely physical goods or supply of a service where no UBS records will be processed? (Yes/No)

### Additional Questions (if "No" is selected):
- Select the applicable option:
  - Final work product qualifies as record.
  - Supply of a service using UBS infrastructure.
  - Supply of a service using vendor infrastructure.

### Additional Info:
- Support and guidelines for records management.

## 18. Intermediary Service
### Questions:
- Will the vendor act as an Intermediary or provide any Intermediary services on behalf of UBS? (Yes/No)

### Definition:
- Intermediaries are individuals or entities that provide services which involve interacting, on UBS' behalf, with an external party (e.g., a client, public official), for UBS' benefit or business advantage.

### Note:
- This section is not segmentation relevant.

## 19. Risk Applicability Summary
### Details:
- Request ID and Test GL number.

### Instructions:
- Review the data before submitting to avoid repeating steps.

### Risk Assessments to Trigger:
- **Regulatory Outsourcing Control Check (ROCC):**
  - **Status:** Yes
  - **Instructions:** Raise a ROCC request or link an existing ROCC to this sourcing request in ServiceNow. Additional guidance provided through a link.

- **Complexity of the Service/Contract:**
  - **Status:** Medium

- **Regulated Activity/Internal Control Function/Risk Function:**
  - **Status:** Yes

- **BCM Critical (BCM Tier):**
  - **Status:** No

- **3PISA Required:**
  - **Status:** Yes
  - **Instructions:** Raise a 3PISA request as soon as the vendor is selected. If there is an existing 3PISA assessment covering the requested service, link it to the request later in the process. Further guidance provided through a link.

- **Other Service-related Risks to be Considered:**
  - **Instructions:** Ensure all applicable activities are performed and relevant clauses are included in the contract.

- **CID Access:**
  - **Status:** Yes
  - **Instructions:** Applicable clauses/exhibits will be included in the contract by Chain IQ. If Chain IQ is not involved, include them yourself. Additional advice provided through guidelines link.

### 20. Requester Dashboard
### Purpose:
- View and manage requests.

### Fields:
- Request ID
- Details
- Category
- Status
- Approval steps

## 21. Sourcing Overview
### Purpose:
- Provide an overview of the sourcing process.

### Fields:
- Sourcing project ID
- Assigned sourcer
- Sourcing gates

## 22. Approver Side - Demand Approval Process
### Explanation:
- This screen shows the steps in the demand approval process and the status of each step.

### Sections:
- **Submit Request:** This is the initial submission of the request.
- **Cost Commitment Approvals by Finance Policy:** The first cost commitment approver reviews and either approves or returns the request.
- **Form Change:** This indicates any necessary changes or corrections to the form.
- **Supply Chain Steps:** Subsequent steps handled by the supply chain team.

### Details:
- **Process Step:** Describes the current step in the process.
- **Activity:** Specific actions taken in each process step.
- **Owner:** Person responsible for the action.
- **Completion Date:** Date when the action was completed.
- **Status:** Current status of the action, such as "Returned" or "Pending".
- **Days:** Number of days taken for the step.
- **Returned Status:** Indicates that the request was returned by the approver for further edits. The requester can make the necessary changes and resubmit.
- **Pending Status:** Indicates that the request is currently awaiting action.

The information provided in this step-by-step guide details the submission, approval, and correction process for a sourcing request. Each step is documented with its purpose, action required, and relevant fields, making it easier to understand the workflow and ensure all necessary information is included for a successful submission.

---

# Title: Detailed Process Breakdown

## 1. Initiation:
- User initiates a request through the chatbot.
- Chatbot asks for initial details such as project name, category, and description.

## 2. Vendor Product Selection:
- Chatbot prompts the user to select vendor products.
- User provides vendor product details.

## 3. Chain IQ Involvement:
- Chatbot asks if Chain IQ will be involved.
- Based on the user's response, additional questions may be asked or certain steps skipped.
- **If "No":** Chatbot asks for the reason for not involving Chain IQ.
- **If "Yes":** Chatbot proceeds to ask about the contract manager.

## 4. Cost Commitment Approvers:
- Chatbot requests cost commitment approvers’ details.
- User provides approver details.

## 5. Business/Budget Owner:
- Chatbot asks for details about the business/budget owner.
- User provides the necessary information.
- **If "Yes" to outside contract manager's segment:** Chatbot asks for the specific business/budget owner.
- **If "No":** Chatbot proceeds to ask for attachments.

## 6. Attachments:
- Chatbot prompts the user to attach any relevant documents.
- User uploads the documents or provides links.

## 7. Risk Applicability:
- Chatbot guides the user through a series of risk-related questions to determine applicable risk assessments.
- User responds to questions about outsourcing, data handling, intermediary services, etc.

## 8. Review and Submit:
- Chatbot reviews all collected information with the user.
- User confirms and submits the request.

## 9. Exception Handling:
- If the request is returned or a risk assessment fails, the chatbot notifies the user and provides options to correct and resubmit the request.
- User makes the necessary changes based on the feedback and resubmits.

## User Guidance and Edge Case Handling
### Uncertain Responses:
- For questions where the user might be unsure, the chatbot offers options to select "I don't know" and provides additional context or instructions.

### Yes/No Decision Points:
- Each Yes/No question is followed by tailored prompts to gather additional necessary information or skip irrelevant steps.

### Document Uploads:
- If the user has documents to upload, the chatbot guides them through the process and confirms successful uploads.

### Risk Assessments:
- The chatbot asks detailed questions about different risk aspects, ensuring all necessary information is captured for each assessment.

### Review and Confirmation:
- Before submission, the chatbot provides a summary of all inputs for the user to review and confirm.

### Exception Handling:
- In case of exceptions, such as missing information or returned requests, the chatbot clearly communicates the issue, provides instructions for corrections, and allows resubmission.
