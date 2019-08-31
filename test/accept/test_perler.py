import unittest
import hprof

class TestPerlerParsing(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.hf = hprof.open('testdata/perler.hprof.bz2')

	def test_name_record_values(self):
		for nameid, expected in (
			(0x7ff7100edd10, '(Ljava/lang/String;I[Ljava/lang/String;[Ljava/lang/String;[I[I)V'),
			(0x7ff71012c2d0, 'initialising'),
			(0x7ff7100be3b0, 'InsertUndo'),
		):
			with self.subTest(nameid):
				self.assertEqual(self.hf.names[nameid], expected)

	def test_name_record_count(self):
		self.assertEqual(len(self.hf.names), 68327)

	def test_frame_record_values(self):
		#00000000 00000001 00007ff7 55fe3ac0 00007ff7 55fd53d0 00007ff7 55fe4290 00001002 fffffffd
		self.assertEqual(self.hf.stackframes[0x01].method, 'sleep')
		self.assertEqual(self.hf.stackframes[0x01].signature, '(J)V')
		self.assertEqual(self.hf.stackframes[0x01].sourcefile, 'Thread.java')
		self.assertIs(   self.hf.stackframes[0x01].class_name, self.hf.classloads[0x1002].class_name)
		self.assertEqual(self.hf.stackframes[0x01].line, -3)

		#00000000 0000000b 00007ff7 55fd6b90 00007ff7 4c3a1fd0 00000000 00000000 00000113 ffffffff
		self.assertEqual(self.hf.stackframes[0x0b].method, 'next')
		self.assertEqual(self.hf.stackframes[0x0b].signature, '()Lse/dolkow/imagefiltering/ThreadedCacher$Task;')
		self.assertIs(   self.hf.stackframes[0x0b].sourcefile, None)
		self.assertIs(   self.hf.stackframes[0x0b].class_name, self.hf.classloads[0x113].class_name)
		self.assertEqual(self.hf.stackframes[0x0b].line, -1)

		#00000000 0000001a 00007ff7 55fd1d70 00007ff7 55fd3330 00007ff7 55fd53e0 00001043 000001f6
		self.assertEqual(self.hf.stackframes[0x1a].method, 'wait')
		self.assertEqual(self.hf.stackframes[0x1a].signature, '()V')
		self.assertEqual(self.hf.stackframes[0x1a].sourcefile, 'Object.java')
		self.assertIs(   self.hf.stackframes[0x1a].class_name, self.hf.classloads[0x1043].class_name)
		self.assertEqual(self.hf.stackframes[0x1a].line, 0x1f6)

	def test_frame_record_count(self):
		self.assertEqual(len(self.hf.stackframes), 82)

	def test_trace_record_values(self):
		#00000001 00000000 00000000
		self.assertEqual(self.hf.stacktraces[0x01].thread, None)
		self.assertEqual(len(self.hf.stacktraces[0x01]), 0)

		#00000003 00000002 00000002 00000000 00000001 00000000 00000002
		self.assertEqual(self.hf.stacktraces[0x03].thread, 'dummy thread') # TODO: real Thread
		self.assertEqual(len(self.hf.stacktraces[0x03]), 2)
		self.assertIs(self.hf.stacktraces[0x03][0], self.hf.stackframes[0x01])
		self.assertIs(self.hf.stacktraces[0x03][1], self.hf.stackframes[0x02])

		#00000009 00000008 00000004 00000000 00000015
		#00000000 00000016 00000000 00000017 00000000 00000018
		self.assertEqual(self.hf.stacktraces[0x09].thread, 'dummy thread') # TODO: real Thread
		self.assertEqual(len(self.hf.stacktraces[0x09]), 4)
		self.assertIs(self.hf.stacktraces[0x09][0], self.hf.stackframes[0x15])
		self.assertIs(self.hf.stacktraces[0x09][1], self.hf.stackframes[0x16])
		self.assertIs(self.hf.stacktraces[0x09][2], self.hf.stackframes[0x17])
		self.assertIs(self.hf.stacktraces[0x09][3], self.hf.stackframes[0x18])

	def test_trace_record_count(self):
		self.assertEqual(len(self.hf.stacktraces), 23)

	def test_class_load_values(self):
		#00000001 00000000 cbc32588 00000001 00007ff6 d80d8a50
		self.assertEqual(self.hf.classloads[1].class_id, 0xcbc32588)
		self.assertEqual(self.hf.classloads[1].class_name, self.hf.names[0x7ff6d80d8a50])
		self.assertEqual(self.hf.classloads[1].stacktrace, self.hf.stacktraces[1])

		#00000404 00000000 cb172d80 00000001 00007ff7 10219230
		self.assertEqual(self.hf.classloads[0x404].class_id, 0xcb172d80)
		self.assertEqual(self.hf.classloads[0x404].class_name, self.hf.names[0x7ff710219230])
		self.assertEqual(self.hf.classloads[0x404].stacktrace, self.hf.stacktraces[1])

		#00001066 00000000 cb1e28e0 00000001 00007ff7 10148740
		self.assertEqual(self.hf.classloads[0x1066].class_id, 0xcb1e28e0)
		self.assertEqual(self.hf.classloads[0x1066].class_name, self.hf.names[0x7ff710148740])
		self.assertEqual(self.hf.classloads[0x1066].stacktrace, self.hf.stacktraces[1])

	def test_class_load_count(self):
		self.assertEqual(len(self.hf.classloads), 4198)

	def test_num_unhandled(self):
		# TODO: update expected count as more types are handled.
		self.assertEqual(sum(self.hf.unhandled.values()), 1)
