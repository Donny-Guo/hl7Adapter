'''
1. Define required segments
2. Split message to different segments
3. check if there's missing segments

'''
from hl7.segments import MSH, SFT, PID, ORC, OBR, OBX, SPM
import re
from typing import List, Tuple, Union
UNBOUND = -1
'''
REQUIRED_SEGMENTS = [('MSH', 1, 1),
                    ('SFT', 1, 1),
                    ('PID', 1, 1),
                    ('ORC', 1, 1),
                    ((('OBR', 1, 1), 
                      ('OBX', 1, UNBOUND), 
                      ('SPM', 1, 1)),
                        1, UNBOUND)]
'''
REQUIRED_SEGMENTS = [('MSH', 1, 1),
                    ('SFT', 1, 1),
                    ('PID', 1, 1),
                    ('PD1', 0, 1),
                    ('NTE', 0, UNBOUND),
                    ('NK1', 0, UNBOUND),
                    ((('PV1', 1, 1), ('PV2', 0, 1)), 0, 1),

                    ((('ORC', 1, 1), ('OBR', 1, 1), ('NTE', 0, UNBOUND), 
                      ((('TQ1', 1, 1), ('TQ2', 0, UNBOUND)), 0, UNBOUND),
                       ('CTD', 0, 1), ((('OBX', 1, 1), ('NTE', 0, UNBOUND)), 1, UNBOUND),
                       ('FT1', 0, UNBOUND), ('CTI', 0, UNBOUND),
                       ((('SPM', 1, 1), ('OBX', 0, UNBOUND)), 1, UNBOUND)), 1, 1),

                    ((('ORC', 0, 1), ('OBR', 1, 1), ('NTE', 0, UNBOUND), 
                      ((('TQ1', 1, 1), ('TQ2', 0, UNBOUND)), 0, UNBOUND),
                       ('CTD', 0, 1), ((('OBX', 1, 1), ('NTE', 0, UNBOUND)), 1, UNBOUND),
                       ('FT1', 0, UNBOUND), ('CTI', 0, UNBOUND),
                       ((('SPM', 1, 1), ('OBX', 0, UNBOUND)), 1, UNBOUND)), 0, UNBOUND),
                    ]

def create_regex_pattern(required_segments: List[Tuple]) -> str:
    """
    Converts the REQUIRED_SEGMENTS structure into a regex pattern.
    
    Args:
        required_segments: List of tuples containing (segment_name, min_count, max_count)
                         or nested tuples for grouped segments
    
    Returns:
        str: Regex pattern that matches valid segment sequences
    """
    def convert_count_to_quantifier(min_count: int, max_count: Union[int, float]) -> str:
        """Convert min/max counts to regex quantifier"""
        if max_count == UNBOUND:
            return f'{{{min_count},}}'
        elif min_count == max_count:
            return f'{{{min_count}}}'
        else:
            return f'{{{min_count},{max_count}}}'
    
    def process_segment_tuple(segment_tuple: Tuple) -> str:
        """Process a single segment tuple or group of segments"""
        if isinstance(segment_tuple[0], tuple):  # Group of segments
            group_segments, min_group, max_group = segment_tuple
            # Process each segment in the group
            group_pattern = ''.join(process_segment_tuple(s) for s in group_segments)
            # Wrap the group in parentheses and add quantifier
            return f'({group_pattern}){convert_count_to_quantifier(min_group, max_group)}'
        else:  # Single segment
            segment_name, min_count, max_count = segment_tuple
            # Create capturing group for each segment with its quantifier
            return f'({segment_name}){convert_count_to_quantifier(min_count, max_count)}'
    
    # Process all segments and create full pattern
    pattern_parts = [process_segment_tuple(segment) for segment in required_segments]
    full_pattern = '^' + ''.join(pattern_parts) + '$'
    return full_pattern

def check_segments(segment_list: List[str]) -> bool:
    """
    Validates if a list of segments follows the required pattern using regex.
    
    Args:
        segment_list: List of segment names in order
    
    Returns:
        bool: True if segments follow the required pattern, False otherwise
    """
    # Convert segment list to string for regex matching
    segment_string = ''.join(segment_list)
    
    # Create regex pattern
    pattern = create_regex_pattern(REQUIRED_SEGMENTS)
    # print(f"pattern: {pattern}")
    
    # Match pattern against segment string
    return bool(re.match(pattern, segment_string))

def segment_message(message: str, sep='\n') -> List[List[str]]:
    '''
    Args:
        message (str):
            input HL7 V2 message
        
        sep (str): default='\n'
            string to separate each segment in HL7 message
    
    Returns:
        List[List[str]]: [segment_list, segment_name_list]
            segment_list (List[str]): A list of segments
            segment_name_list (List[str]): A list of segment names
    '''
    segment_list = message.strip('\n\r').split(sep)
    segment_list = [segment.strip('\r') for segment in segment_list]
    segment_name_list = [segment.split('|')[0].strip() for segment in segment_list]
    return [segment_list, segment_name_list]

def parse_message(message: str) -> List[List[str]]:
    errors, warnings = [], []
    output = [errors, warnings]
    segment_list, segment_name_list = segment_message(message)
    result = check_segments(segment_name_list)

    if not result:
        errors.append("Invalid Message: Missing essential segments, should have all the following segments: MSH, SFT, PID, ORC, OBR, OBX, and SPM.")
    else:
        for segment_name, segment_text in zip(segment_name_list, segment_list):
            if segment_name in ['MSH', 'SFT', 'PID', 'ORC', 'OBR', 'OBX', 'SPM']:
                x = globals()[segment_name](segment_text)
                temp_errors, temp_warnings = x.validate()
                errors.extend(temp_errors)
                warnings.extend(temp_warnings)

    return output

def main():
    message = r'''MSH|^~\&|XL2HL7^1.10.100.1.111111.1.101^ISO|Test Lab^99999^CLIA|CalRedie|CDPH|20241030100306||ORU^R01^ORU_R01|103|P|2.5.1|||NE|NE|||||PHLabReport-NoAck^^^ISO
SFT|XL2HL7 Conversion|1.0|CalREDIE XC|1.0||20240105
PID|1||8675309||Test^Rick^A||20200202|M||2033-9|1234 Main Ln.^^Sacramento^CA^95814||^PRN^PH^^1^916^1234567|||||||||H|
ORC|RE|Gon1001^Test Lab^99999^CLIA|Doctor|||||||||NPI123456^Doctor^Doctor|||||||||Test Lab^^^^^^^^^99999|123 That Street St.^^Sacramento^CA^95814^^B|^WPN^PH^^^337^3373377|123 That Street St.^^Sacramento^CA^95814|||||||
OBR|1|Gon1001^Test Lab^99999^CLIA|Gon1001|21416-3N. gonorrhoeae DNA NAA+probe Ql (U)|||24y0229092624||||||Not Pregnant|||NPI123456^Doctor^Doctor|^WPN^PH^^1^337^3373377|||||20241030100306|||F|||||||||||||||||||||||||
OBX|1|CE|21416-3^N. gonorrhoeae DNA NAA+probe Ql (U)||260373001^Detected||NEG|A^Abnormal|||F|||20240228101533|||^Roche cobas® 8800 System||20240229092624||||ARUP^^^^^^^^^46D0523979|2023 Floyd Ave^Salt Lake City^UT^84108||||||
SPM|1|^8675309|| ^Body fluid sample|||||||||||||20240228101533|20240228110000|||||||||||
'''
    
    errors, warnings = parse_message(message)
    print(f"errors: {errors}")
    print(f"warnings: {warnings}")

if __name__ == "__main__":
    main()
    