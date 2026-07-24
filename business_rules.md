## Business Decision Rules

The law firm follows the following business rules when evaluating and assigning client cases:

### Rule 1 – Urgency & Missing Documents
- If the deadline is **7 days or less** and only **secondary documents** are missing, the case is **provisionally accepted**, and the client is asked to submit the missing documents.
- If any **critical document** is missing, the system requests additional information before proceeding.

### Rule 2 – Evidence & Conflict
- If a conflict of interest is **only suspected** and the available evidence is **strong**, the case continues with a warning.
- If the evidence is **weak**, a suspected conflict results in **rejection** or **senior review**.

### Rule 3 – Specialist Availability
- If no exact specialist is available and the deadline is **3 days or less**, the case is assigned to a **related specialist**.
- Otherwise, the case is **escalated**.

### Rule 4 – Client History
- If the client is **returning** and the required document already exists in the firm's records, the existing valid documen t is  **reused** instead of requesting it again.




## Business Decision Priority

When multiple conditions apply to the same case, the agent evaluates them in the following priority order and stops at the first matching rule:

1. **Confirmed Conflict of Interest** → Reject the case.
2. **Suspected Conflict of Interest + Weak Evidence** → Reject the case or escalate it for senior review.
3. **Missing Critical Documents** → Request more information before proceeding.
4. **Missing Secondary Documents + Urgent Deadline** → Provisionally accept the case and request the missing documents.
5. **No Exact Specialist + Related Specialist Available + Urgent Deadline** → Assign the case to a related specialist.
6. **No Suitable Specialist Available** → Escalate the case.
7. **Otherwise** → Accept the case.



### Input Fields

- **Case ID** – Unique identifier for the case.
- **Case Type** – The legal category of the case (e.g., commercial, employment, family).
- **Days Until Deadline** – Number of days remaining before the legal deadline.
- **Document Status** – Indicates whether the required documents are complete, missing secondary documents, or missing critical documents.
- **Evidence Strength** – The quality of the available evidence (Strong, Medium, or Weak).
- **Conflict Status** – Indicates whether there is no conflict, a suspected conflict, or a confirmed conflict of interest.
- **Exact Specialist Available** – Whether a lawyer with the required specialization is available.
- **Related Specialist Available** – Whether a lawyer with a related specialization is available.
- **Returning Client** – Indicates whether the client has previously worked with the firm.
- **Document Available in Archive** – Indicates whether a missing document already exists in the firm's records.


### Possible Decisions

- Accept Case
- Provisionally Accept and Request Missing Documents
- Request More Information
- Reject Due to Conflict of Interest
- Escalate for Senior Review
- Escalate Due to No Available Specialist
