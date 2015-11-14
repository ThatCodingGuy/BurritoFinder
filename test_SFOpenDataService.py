import unittest

import SFOpenDataService

class SFOpenDataServiceTestCase(unittest.TestCase):

	def setUp(self):
		self.service = SFOpenDataService.SFOpenDataService()

	def tearDown(self):
		pass

	def test_parseDaySegment_invalid_day(self):
		self.assertRaises(SFOpenDataService.ScheduleParseException, self.service.parseDaySegment, "sdli")

	def test_parseDaySegment_valid_single_day(self):
		result = self.service.parseDaySegment("Mo")
		self.assertEqual(["Mo"], result)

	def test_parseDaySegment_valid_day_range(self):
		result = self.service.parseDaySegment("Tu-Su")
		self.assertIn("Tu", result)
		self.assertIn("We", result)
		self.assertIn("Th", result)
		self.assertIn("Fr", result)
		self.assertIn("Sa", result)
		self.assertIn("Su", result)
		self.assertEqual(6, len(result))

	def test_parseSchedule_invalid_format(self):
		self.assertRaises(SFOpenDataService.ScheduleParseException, self.service.parseSchedule, "sd:fse:esr")
		self.assertRaises(SFOpenDataService.ScheduleParseException, self.service.parseSchedule, "sdfseesr")
		self.assertRaises(SFOpenDataService.ScheduleParseException, self.service.parseSchedule, "s:d:fs;e:esr")

	def test_parseSchedule_valid_single_segment(self):
		result = self.service.parseSchedule("Tu/We:6am-8pm")
		self.assertEqual(7, len(result))
		self.assertEqual(result[1], "Not open")
		self.assertEqual(result[2], "6am-8pm")
		self.assertEqual(result[3], "6am-8pm")
		self.assertEqual(result[4], "Not open")

	def test_parseSchedule_valid_multi_segment(self):
		result = self.service.parseSchedule("Tu/We:6am-8pm;Fr:9am-12pm")
		self.assertEqual(7, len(result))
		self.assertEqual(result[1], "Not open")
		self.assertEqual(result[2], "6am-8pm")
		self.assertEqual(result[3], "6am-8pm")
		self.assertEqual(result[4], "Not open")	
		self.assertEqual(result[5], "9am-12pm")	
		self.assertEqual(result[6], "Not open")	

if __name__ == '__main__':
	unittest.main()