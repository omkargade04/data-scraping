from pydantic import BaseModel
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

# Search results
class SearchResultData(BaseModel):
    case_no: str
    date_of_decision: str
    petitioner: str
    respondent: str
    case_type: str
    case_status: str
    case_stage: str

# Case details
class CaseDetails(BaseModel):
    registration_no: str
    case_no: str
    filing_date: str
    petitioner: str
    respondent: str
    advocates: List[str]
    judges: List[str]
    bench: str
    hearing_history: List[Dict[str, str]]
    applicable_acts: List[str]
    orders: List[Dict[str, str]]
    case_stage: str
    attached_cases: str
    applications_filed: str
    date_of_destruction: str

class ConciseJson(BaseModel):
    case_details: CaseDetails

# Scrape search results
def scrape_search_results(url: str) -> List[SearchResultData]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    cases = []
    
    # for row in soup.select('tr'):
    #     cols = row.find_all('td')
    #     if len(cols) > 4:
    #         case = SearchResultData(
    #             case_no=cols[0].text.strip(),
    #             date_of_decision=cols[1].text.strip(),
    #             petitioner=cols[2].text.strip(),
    #             respondent=cols[3].text.strip(),
    #             case_type=cols[4].text.strip(),
    #             case_status=cols[5].text.strip()
    #         )
    #         cases.append(case)

    case = SearchResultData(
        case_no=soup.find(id='lblh0').text.strip(),
        date_of_decision=soup.find(id='lblh9').text.strip(),
        petitioner=soup.find(id='lblh3').text.strip(),
        respondent=soup.find(id='lblh4').text.strip(),
        case_type=soup.find(id='lblh7').text.strip(),
        case_status=soup.find(id='lblh6').text.strip(),
        case_stage=soup.find(id='lblh6').text.strip(),
    )
    cases.append(case)
    return cases

# Scrape case details
def scrape_case_details(case_number: str) -> ConciseJson:
    case_details_url = f"https://cms.nic.in/ncdrcusersWeb/login.do?method=caseStatus&caseNo={case_number}"
    response = requests.get(case_details_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    registration_no = soup.find(id='registrationNumber').text.strip()
    case_no=soup.find(id='lblh0').text.strip(),
    filing_date=soup.find(id='lblh1').text.strip(),
    petitioner=soup.find(id='lblh3').text.strip(),
    respondent=soup.find(id='lblh4').text.strip(),
    advocates = [advocate.text.strip() for advocate in soup.find_all(class_='advocate')]
    judges = [judge.text.strip() for judge in soup.find_all(class_='judge')]
    bench = soup.find(id='bench').text.strip()
    hearing_history=soup.find(id='lblh5').text.strip(),
    applicable_acts = [act.text.strip() for act in soup.find_all(class_='applicableAct')]
    orders = []
    for row in soup.select('.orderHistory tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            orders.append({
                'date': cols[0].text.strip(),
                'order': cols[1].text.strip()
            })
    case_stage=soup.find(id='lblh6').text.strip(),
    attached_cases=soup.find(id='lblh7').text.strip(),
    applications_filed=soup.find(id='lblh8').text.strip(),
    date_of_destruction=soup.find(id='lblh9').text.strip()

    case_details = CaseDetails(
        registration_no=registration_no,
        case_no=case_no,
        filing_date=filing_date,
        petitioner=petitioner,
        respondent=respondent,
        advocates=advocates,
        judges=judges,
        bench=bench,
        hearing_history=hearing_history,
        applicable_acts=applicable_acts,
        orders=orders,
        case_stage=case_stage,
        attached_cases=attached_cases,
        applications_filed=applications_filed,
        date_of_destruction=date_of_destruction
    )
    
    return ConciseJson(case_details=case_details)


search_results_url = 'https://cms.nic.in/ncdrcusersWeb/search.do?method=loadSearchPub'
case_details_url_template = 'https://cms.nic.in/ncdrcusersWeb/login.do?method=caseStatus&caseNo={case_number}'

# Scrape search results
search_results = scrape_search_results(search_results_url)

for result in search_results:
    print(result.model_dump_json())

if search_results:
    case_details = scrape_case_details(search_results[0].case_no)
    print(case_details.model_dump_json())

