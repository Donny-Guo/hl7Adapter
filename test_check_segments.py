from parser import check_segments
import unittest

class TestCheckSegments(unittest.TestCase):
    def setUp(self):
        self.complete_list = ['MSH', 'SFT', 'PID', 'ORC', 'OBR', 'OBX','SPM']
    
    def test_missing_MSH(self):
        segment_name_list = self.complete_list
        segment_name_list.remove('MSH')
        result = check_segments(segment_name_list)
        self.assertEqual(result, 0)

    
    def test_multiple_MSH(self):
        segment_name_list = self.complete_list
        segment_name_list.insert(1, "MSH")
        result = check_segments(segment_name_list)
        self.assertEqual(result, 0)


    def test_missing_SFT(self):
        segment_name_list = self.complete_list
        segment_name_list.remove('SFT')
        result = check_segments(segment_name_list)
        self.assertEqual(result, 0)

    def test_optional_segment(self):
        segment_name_list = self.complete_list
        segment_name_list.insert(3, "NTE")
        result = check_segments(segment_name_list)
        self.assertEqual(result, 1)

    

if __name__ == "__main__":
    unittest.main()