'''
Definition of each segment

'''
from typing import List
from datetime import datetime

class PID:
    def __init__(self, text):
        self.text = text

        
    
    def validate(self) -> List[str]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[str]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')


        # check PID-5 Patient Name existence
        if not fields[5]:
            errors.append("Missing Patient Name.")
        else:
            components = fields[5].split('^')
            # check PID-5.1 Last Name
            if not components[0]:
                errors.append("Missing Patient Last Name.")
            elif not components[0].isalpha():
                warnings.append("Patient Last Name contains non-ASCII characters.")
            # check PID-5.2 First Name
            if not components[1]:
                errors.append("Missing Patient First Name.")
            elif not components[1].isalpha():
                warnings.append("Patient First Name contains non-ASCII characters.")
            # check PID-5.3 Middle Name (don't care for now)


        # check PID-7 Patient Date of Birth (YYYYMMDD)
        if not fields[7]:
            errors.append("Missing Patient Date of Birth.")
        else:
            if not datetime.strptime(fields[7], "%Y%m%d"):
                errors.append(f"Invalid Patient Date of Birth: {fields[7]}, should be in the format of YYYYMMDD")


        # check PID-8 Administrative Sex (F, M, O, or U)
        if not fields[8]:
            errors.append("Missing Patient Sex.")
        else:
            if fields[8] not in ['F', 'M', 'O', 'U']:
                errors.append(f"Invalid Patient Sex: {fields[8]}, should be either F, M, O, or U.")


        # check PID-10 Patient Race


        # check PID-11 Patient Address


        # check PID-13 Patient Phone Number (has area code, no dashes)

        # check PID-22 Patient Ethnic Group

        return output

if __name__ == "__main__":
    # test PID class
    pid_text = "PID|1||8675309||Test^Rick^A||20200202|F||2033-9|1234 Main Ln.^^Sacramento^CA^95814||^PRN^PH^^1^916^1234567|||||||||H|"
    pid = PID(pid_text)
    errors, warnings = pid.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")