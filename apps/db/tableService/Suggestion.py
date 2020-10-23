import warnings

from apps.db.tableService.TableServiceBase import TableServiceBase

class Suggestion(TableServiceBase):
    def __init__(self, name='', email='', org='', resInterests='', resIdea='', proposal=''):
        super().__init__('suggestion')

        self.Name = name
        self.Email = email
        self.Organization = org
        self.ResearchInterests = resInterests
        self.ResearchIdea = resIdea
        self.Proposal = proposal
    
    def setName(self, name):
        self.Name = name
    
    def setEmail(self, email):
        self.Email = email
    
    def setOrg(self, org):
        self.Organization = org
    
    def setResearchInterests(self, resInterests):
        self.ResearchInterests = resInterests
    
    def setResearchIdea(self, resIdea):
        self.ResearchIdea = resIdea
    
    def setProposal(self, proposal):
        self.Proposal = proposal
    
    def add(self):
        if not self.Name or not self.Email or not self.Organization or not self.Proposal:
            warnings.warn('Name, Email, Organization and Proposal must not be null, nothing to do')
        values = self.getAllField()
        return self.DB.insertDB(self.tableName, **values)
    
