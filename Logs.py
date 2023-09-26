from dataclasses import dataclass

@dataclass
class Logs:

    service_id: str
    log_type: str
    tag: str
    message: dict

    def audit(self):

        return self.service_id, self.log_type, self.tag, self.message
        

