'''
Definition of each segment

'''
from typing import List
from datetime import datetime

class MSH:
    def __init__(self, text):
        self.text = text
    
    def validate(self) -> List[List[str]]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[List[str]]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')
        fields.insert(0, '') # handle index off by 1
        fields_count = len(fields) - 1

        # check MSH-4 Sending Facility
        if 4 > fields_count or not fields[4]:
            errors.append("Missing Sending Facility (MSH-4).")
        else:
            components = fields[4].split('^')
            components_count = len(components) - 1

            # check MSH-4-1 Reporting Facility Name (must not exceed 20 characters)
            if not components[0]:
                errors.append("Missing Reporting Facility Name (MSH-4-1).")
            else:
                if len(components[0]) > 20:
                    warnings.append("Invalid Reporting Facility Name (MSH-4-1): {components[0]}, must not exceed 20 characters.")

            # check MSH-4-2 Facility CLIA
            if 1 > components_count or not components[1]:
                errors.append("Missing Facility CLIA (MSH-4-2).")
            else:
                pass # add more checking later

        
        # check MSH-7 Date and Time of Message: YYYYMMDDHHMMSS (GMT-offset is optional: -7000)
        if 7 > fields_count or not fields[7]:
            errors.append("Missing Date and Time of Message (MSH-7).")
        else:
            isValid = False
            for format in ["%Y%m%d%H%M%S", "%Y%m%d%H%M%S%z"]:
                try:
                    datetime.strptime(fields[7], format)
                    isValid = True
                    break
                except:
                    continue
            if not isValid:
                errors.append(f"Invalid Date and Time of Message (MSH-7): {fields[7]}, should be in the format of YYYYMMDDHHMMSS (GMT-offset is optional).")
        

        # check MSH-10 Message Control ID
        if 10 > fields_count or not fields[10]:
            errors.append("Missing Message Control ID (MSH-10).")
        else:
            pass # add more checking later


        # check MSH-12 Version ID
        if 12 > fields_count or not fields[12]:
            errors.append("Missing Message Version ID (MSH-12).")
        else:
            components = fields[12].split('^')
            components_count = len(components) - 1

            # check MSH-12-1 HL7 version number (2.5.1 or higher)
            if not components[0]:
                errors.append("Missing HL7 version number (MSH-12-1).")
            else:
                # check if version number is 2.5.1 or higher
                version_list = components[0].split('.')
                try:
                    if ((len(version_list) == 2 and version_list[0] == "2" and int(version_list[1]) > 5)
                        or (len(version_list) == 3 and version_list[0] == "2" and int(version_list[1]) == 5 and int(version_list[2]) >= 1)
                        or (len(version_list) == 3 and version_list[0] == "2" and int(version_list[1]) > 5) ):
                        pass 
                    else:
                        errors.append("Invalid HL7 version number (MSH-12-1): {components[0]}, should be 2.5.1 or higher.")
                except:
                    errors.append("Invalid HL7 version number (MSH-12-1): {components[0]}, should be 2.5.1 or higher.")

        return output

class SFT:
    def __init__(self, text):
        self.text = text
    
    def validate(self) -> List[List[str]]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[List[str]]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')
        fields_count = len(fields) - 1

        # check SFT-1 Software Vendor Organiation
        if 1 > fields_count or not fields[1]:
            errors.append("Missing Software Vendor Organiation (SFT-1).")
        else:
            pass # add more checking later

        # check SFT-3 Software Product Name
        if 3 > fields_count or not fields[3]:
            errors.append("Missing Software Product Name (SFT-3).")
        else:
            pass # add more checking later

        return output

class PID:
    def __init__(self, text):
        self.text = text  
    
    def validate(self) -> List[List[str]]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[List[str]]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')
        fields_count = len(fields) - 1

        # check PID-5 Patient Name existence
        if 5 > fields_count or not fields[5]:
            errors.append("Missing Patient Name (PID-5).")
        else:
            components = fields[5].split('^')
            components_count = len(components) - 1
            # check PID-5.1 Last Name
            if not components[0]:
                errors.append("Missing Patient Last Name (PID-5-1).")
            elif not components[0].isalpha():
                warnings.append("Patient Last Name contains non-ASCII characters.")
            # check PID-5.2 First Name
            if 1 > components_count or not components[1]:
                errors.append("Missing Patient First Name (PID-5-2).")
            elif not components[1].isalpha():
                warnings.append("Patient First Name contains non-ASCII characters.")
            # check PID-5.3 Middle Name (don't care for now)


        # check PID-7 Patient Date of Birth (YYYYMMDD)
        if 7 > fields_count or not fields[7]:
            errors.append("Missing Patient Date of Birth (PID-7).")
        else:
            try:
                datetime.strptime(fields[7], "%Y%m%d")
            except:
                errors.append(f"Invalid Patient Date of Birth: {fields[7]}, should be in the format of YYYYMMDD")


        # check PID-8 Administrative Sex (F, M, O, or U)
        if 8 > fields_count or not fields[8]:
            errors.append("Missing Patient Sex (PID-8).")
        else:
            if fields[8] not in ['F', 'M', 'O', 'U']:
                errors.append(f"Invalid Patient Sex: {fields[8]}, should be either F, M, O, or U.")


        # check PID-10 Patient Race
        if 10 > fields_count or not fields[10]:
            errors.append("Missing Patient Race (PID-10).")
        else:
            pass # add more checking later

        # check PID-11 Patient Address
        if 11 > fields_count or not fields[11]:
            errors.append("Missing Patient Address (PID-11).")
        else:
            pass # add more checking later

        # check PID-13 Patient Phone Number (has area code, no dashes)
        if 13 > fields_count or not fields[13]:
            errors.append("Missing Patient Phone Number (PID-13).")
        else:
            pass # add more checking later

        # check PID-22 Patient Ethnic Group
        if 22 > fields_count or not fields[22]:
            errors.append("Missing Patient Ethnic Group (PID-22).")
        else:
            pass # add more checking later

        return output

class ORC:
    def __init__(self, text):
        self.text = text
    
    def validate(self) -> List[List[str]]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[List[str]]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')
        fields_count = len(fields) - 1

        # check ORC-21 Ordering Facility Name
        if 21 > fields_count or not fields[21]:
            errors.append("Missing Ordering Facility Name (ORC-21).")
        else:
            pass # add more checking later

        # check ORC-22 Ordering Facility Address
        if 22 > fields_count or not fields[22]:
            errors.append("Missing Ordering Facility Address (ORC-22).")
        else:
            pass # add more checking later

        # check ORC-23 Ordering Facility Phone Number
        if 23 > fields_count or not fields[23]:
            errors.append("Missing Ordering Facility Phone Number (ORC-23).")
        else:
            pass # add more checking later

        # check ORC-24 Ordering/Referring Provider Address
        if 24 > fields_count or not fields[24]:
            errors.append("Missing Ordering/Referring Provider Address (ORC-24).")
        else:
            pass # add more checking later

        return output

class OBR:
    def __init__(self, text):
        self.text = text
    
    def validate(self) -> List[List[str]]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[List[str]]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')
        fields_count = len(fields) - 1

        # check OBR-4 Lab Test Order LOINC
        if 4 > fields_count or not fields[4]:
            errors.append("Missing Lab Test Order LOINC (OBR-4).")
        else:
            pass # add more checking later

        # check OBR-13 Relevant Clinical Information: Prenatal, Not Pregnant, or Unknown Pregnancy
        if 13 > fields_count or not fields[13]:
            errors.append("Missing Relevant Clinical Information (OBR-13).")
        else:
            if fields[13] not in ['Prenatal', 'Not Pregnant', 'Unknown Pregnancy']:
                errors.append(f"Invalid Relevant Clinical Information: {fields[13]}, should be either Prenatal, Not Pregnant, or Unknown Pregnancy.")

        # check OBR-16 Ordering Provider National Provider Identifier (NPI) and Name
        if 16 > fields_count or not fields[16]:
            errors.append("Missing  Ordering Provider National Provider Identifier (NPI) and Name (OBR-16).")
        else:
            pass # add more checking later

        # check OBR-17 Ordering Provider Phone Number
        if 17 > fields_count or not fields[17]:
            errors.append("Missing Ordering Provider Phone Number (OBR-17).")
        else:
            pass # add more checking later

        # check OBR-25 Result Status: F for final, P for preliminary, and C for corrected
        if 25 > fields_count or not fields[25]:
            errors.append("Missing Result Status (OBR-25).")
        else:
            if fields[25] not in ['F', 'P', 'C']:
                errors.append(f"Invalid Result Status (OBR-25): {fields[25]}, should be either F, P, or C.")

        # # check OBR-31 Reason for Study: Use ICD-10 Diagnosis Code
        # if 31 > fields_count or not fields[31]:
        #     errors.append("Missing Reason for Study (OBR-31).")
        # else:
        #     pass # add more checking later

        return output

class OBX:
    def __init__(self, text):
        self.text = text
    
    def validate(self) -> List[List[str]]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[List[str]]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')
        fields_count = len(fields) - 1
        data_type = None

        # check OBX-2 Data Type: (SN, CWE, CNE, FT, ST, TX, TS, TM, DT, CE)
        '''
        SN = Structured Numeric; CWE = Coded with Exceptions; CNE = Coded no Exceptions
        FT = Formatted Text with embedded codes; ST = String for text less than 999 characters
        TX = Text more than 999 characters; TS/TM/ DT =Timestamp/Time/Date
        CE = Coded Element
        '''
        if 2 > fields_count or not fields[2]:
            errors.append("Missing Data Type (OBX-2).")
        else:
            if fields[2] not in ['SN', 'CWE', 'CNE', 'FT', 'ST', 'TX', 'TS', 'TM', 'DT', 'CE']:
                errors.append(f"Invalid Data Type (OBX-2): {fields[2]}, should be either SN, CWE, CNE, FT, ST, TX, TS, TM, DT, or CE.")
            else:
                data_type = fields[2]

        # check OBX 3 Observation Identifier
        if 3 > fields_count or not fields[3]:
            errors.append("Missing Observation Identifier (OBX-3).")
        else:
            components = fields[3].split('^')
            components_count = len(components) - 1

            # check OBX-3-1 Lab Test LOINC code
            if not components[0]:
                errors.append("Missing Lab Test LOINC code (OBX-3-1).")
            else:
                pass # add checking LOINC code with tables later

            # check OBX-3-2 Lab Test Name
            if 1 > components_count or not components[1]:
                errors.append("Missing Lab Test Name (OBX-3-2).")
            else:
                pass # add more checking later


        # check OBX-5 Observation Value
        if 5 > fields_count or not fields[5]:
            errors.append("Missing Observation Value (OBX-5).")
        else:
            components = fields[5].split('^')
            components_count = len(components) - 1

            # check OBX-5-1 Lab Result Observation Value Code
            if not components[0]:
                errors.append("Missing Lab Result Observation Value Code (OBX-5-1).")
            else:
                pass # add more checking later

            # check OBX-5-2 Lab Result Observation Value Text Description
            if 1 > components_count or not components[1]:
                errors.append("Missing Lab Result Observation Value Text Description (OBX-5-2).")
            else:
                pass # add more checking later


        # check OBX-6 Result Units
        '''
        Condition: If the data type in OBX-2 is "NM" or "SN" then OBX-6 must be populated. Else, OBX-6 is not populated.
        '''
        if data_type in ['NM', 'SN']:
            if 6 > fields_count or not fields[6]:
                errors.append("Missing Result Units (OBX-6).")
            else:
                pass # add more checking later


        # check OBX-7 Result References Range
        if 7 > fields_count or not fields[7]:
            errors.append("Missing Result References Range (OBX-7).")
        else:
            pass # add more checking later


        # check OBX-8 Abnormal Flag
        if 8 > fields_count or not fields[8]:
            errors.append("Missing Abnormal Flag (OBX-8).")
        else:
            pass # add more checking later


        # check OBX-11 Observation Result Status: F for final, P for preliminary, and C for corrected
        if 11 > fields_count or not fields[11]:
            errors.append("Missing Observation Result Status (OBX-11).")
        else:
            if fields[11] not in ['F', 'P', 'C']:
                errors.append(f"Invalid Observation Result Status (OBX-11): {fields[11]}, should be either F, P, or C.")


        # check OBX-17 Observation Method or Test Device
        if 17 > fields_count or not fields[17]:
            errors.append("Missing Observation Method or Test Device (OBX-17).")
        else:
            pass # add more checking later


        # check OBX-19 Test Resulted Date and Time: YYYYMMDDHHMMSS
        if 19 > fields_count or not fields[19]:
            errors.append("Missing Test Resulted Date and Time (OBX-19).")
        else:
            try:
                datetime.strptime(fields[19], "%Y%m%d%H%M%S")
            except:
                errors.append(f"Invalid Test Resulted Date and Time (OBX-19): {fields[19]}, should be in the format of YYYYMMDDHHMMSS.")


        # check OBX-23 Performing Organization Name
        if 23 > fields_count or not fields[23]:
            errors.append("Missing Performing Organization Name (OBX-23).")
        else:
            components = fields[23].split('^')
            components_count = len(components) - 1

            # check OBX-23-1 Performing Organization Name
            if not components[0]:
                errors.append("Missing Performing Organization Name (OBX-23-1).")
            else:
                pass # add more checking later

            # check OBX-23-10 Performing Organization CLIA
            if 9 > components_count or not components[9]:
                errors.append("Missing Performing Organization CLIA (OBX-23-10).")
            else:
                pass # add checking CLIA later
        

        # check OBX-24 Performing Organization Address
        if 24 > fields_count or not fields[24]:
            errors.append("Missing Performing Organization Address (OBX-24).")
        else:
            pass # add more checking later

        return output

class SPM:
    def __init__(self, text):
        self.text = text
    
    def validate(self) -> List[List[str]]:
        '''
        Validate the segment text and return a list of errors

        Args: None

        Returns: List[List[str]]
        '''
        errors, warnings = [], []
        output = [errors, warnings]
        # split
        fields = self.text.split('|')
        fields_count = len(fields) - 1

        # check SPM-2 Specimen ID
        if 2 > fields_count or not fields[2]:
            errors.append("Missing Specimen ID (SPM-2).")
        else:
            components = fields[2].split('^')
            components_count = len(components) - 1

            # check SPM-2-2 Filler Assigned Identifier existed
            if 1 > components_count or not components[1]:
                errors.append("Missing Filler Assigned Identifier (SPM-2-2).")
            else:
                subcomponents = components[1].split('&')
                # check SPM-2-2-1 Accession Number (required)
                if not subcomponents[0]:
                    errors.append("Missing Accession Number (SPM-2-2-1).")


        # check SPM-4 Specimen Type
        if 4 > fields_count or not fields[4]:
            errors.append("Missing Specimen Type (SPM-4).")
        else:
            components = fields[4].split('^')
            components_count = len(components) - 1

            # check SPM-4-1 Specimen Type or Material SNOMED code (CAN CHECK WITH TABLE)
            if not components[0]:
                errors.append("Missing Specimen Type or Material SNOMED code (SPM-4-1).")
            else:
                pass # add more checking later

            # check SPM-4-2 Specimen Type or Material Text Description
            if 1 > components_count or not components[1]:
                errors.append("Missing Specimen Type or Material Text Description (SPM-4-2).")
            else:
                pass # add more checking later


        # # check SPM-8 Specimen Source Site (optional)
        # if 8 > fields_count or not fields[8]:
        #     errors.append("Missing Specimen Source Site (SPM-8).")
        # else:
        #     components = fields[8].split('^')
        #     components_count = len(components) - 1

        #     # check SPM-8-1 SNOMED Code for Specimen Source Site (CAN CHECK WITH TABLE)
        #     if not components[0]:
        #         errors.append("Missing SNOMED Code for Specimen Source Site (SPM-8-1).")
        #     else:
        #         pass # add more checking later

        #     # check SPM-8-2 Speciment source site text description
        #     if 1 > components_count or not components[1]:
        #         errors.append("Missing Speciment source site text description (SPM-8-2).")
        #     else:
        #         pass # add more checking later


        # check SPM-17 Specimen Collected Date and Time: YYYYMMDDHHMMSS
        if 17 > fields_count or not fields[17]:
            errors.append("Missing Specimen Collected Date and Time (SPM-17).")
        else:
            try:
                datetime.strptime(fields[17], "%Y%m%d%H%M%S")
            except:
                errors.append(f"Invalid Specimen Collected Date and Time (SPM-17): {fields[17]}, should be in the format of YYYYMMDDHHMMSS.")

        # check SPM-18 Specimen Received Date and Time: YYYYMMDDHHMMSS
        if 18 > fields_count or not fields[18]:
            errors.append("Missing Specimen Received Date and Time (SPM-18).")
        else:
            try:
                datetime.strptime(fields[18], "%Y%m%d%H%M%S")
            except:
                errors.append(f"Invalid Specimen Received Date and Time (SPM-18): {fields[18]}, should be in the format of YYYYMMDDHHMMSS.")

        return output        

if __name__ == "__main__":

    # test MSH class
    print("test MSH class")
    msh_text = "MSH|^~\&|XL2HL7^1.10.100.1.111111.1.101^ISO|Test Lab^99999^CLIA|CalRedie|CDPH|20241030100306||ORU^R01^ORU_R01|103|P|2.5.1|||NE|NE|||||PHLabReport-NoAck^^^ISO"
    msh = MSH(msh_text)
    errors, warnings = msh.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")
    print('-' * 100)

    # test SFT class
    print("test SFT class")
    sft_text = "SFT|XL2HL7 Conversion|1.0|CalREDIE XC|1.0||20240105"
    sft = SFT(sft_text)
    errors, warnings = sft.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")
    print('-' * 100)

    # test PID class
    print("test PID class")
    pid_text = "PID|1||8675309||Test^Rick^A||20200202|F||2033-9|1234 Main Ln.^^Sacramento^CA^95814||^PRN^PH^^1^916^1234567|||||||||H|"
    # pid_text = "PID|1||8675309||Test^|"
    pid = PID(pid_text)
    errors, warnings = pid.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")
    print('-' * 100)

    # test ORC class
    print("test ORC class")
    orc_text = "ORC|RE|Gon1001^Test Lab^99999^CLIA|Doctor|||||||||NPI123456^Doctor^Doctor|||||||||Test Lab^^^^^^^^^99999|123 That Street St.^^Sacramento^CA^95814^^B|^WPN^PH^^^337^3373377|123 That Street St.^^Sacramento^CA^95814|||||||"
    orc = ORC(orc_text)
    errors, warnings = orc.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")
    print('-' * 100)

    # test OBR class
    print("test OBR class")
    obr_text = "OBR|1|Gon1001^Test Lab^99999^CLIA|Gon1001|21416-3N. gonorrhoeae DNA NAA+probe Ql (U)|||24y0229092624||||||Not Pregnant|||NPI123456^Doctor^Doctor|^WPN^PH^^1^337^3373377|||||20241030100306|||F|||||||||||||||||||||||||"
    obr = OBR(obr_text)
    errors, warnings = obr.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")
    print('-' * 100)

    # test OBX class
    print("test OBX class")
    obx_text = "OBX|1|CE|21416-3^N. gonorrhoeae DNA NAA+probe Ql (U)||260373001^Detected||NEG|A^Abnormal|||F|||20240228101533|||^Roche cobas® 8800 System||20240229092624||||ARUP^^^^^^^^^46D0523979|2023 Floyd Ave^Salt Lake City^UT^84108||||||"
    obx = OBX(obx_text)
    errors, warnings = obx.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")
    print('-' * 100)

    # test SPM class
    print("test SPM class")
    spm_text = "SPM|1|^8675309|| ^Body fluid sample|||||||||||||20240228101533|20240228110000|||||||||||"
    spm = SPM(spm_text)
    errors, warnings = spm.validate()
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")
    print('-' * 100)