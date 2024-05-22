• Scrape Search Results: Scrape the first page of search results from the
provided website. This should include information for each case like:
• Case Number (e.g., CINO for NCDRC)
• Date of Decision
• Petitioner Name
• Respondent Name
• Case Type

2. Model Search Results: I have Modeled the scraped data for each case according
to the SearchResultData Pydantic model provided.
3. Scrape Case Details: I have scraped detailed information
for a specific case by following a link or using a case number. This should
include details like:
• Case details (registration number, filing date, etc.)
• Parties involved (petitioner, respondent, advocates)
• Judges and bench
• Hearing history with dates and purposes
• Applicable acts and sections
• Orders (interim, final, and order history)
4. Model Case Details: I have modeled the data according to the ConciseJson Pydantic model provided.
