"""
Tests for intelmq.lib.splitreports
"""

import io
import os
import tempfile
import unittest
import itertools
import base64

from intelmq.lib.splitreports import read_delimited_chunks, generate_reports
from intelmq.lib.message import Report

csv_test_data = b"\n".join(b",".join(line) for line in
                           [[bytes("header-%d" % (col,), "ascii")
                             for col in range(10)]]
                           + [[bytes("value-%d-%d" % (row, col), "ascii")
                               for col in range(10)]
                              for row in range(1000)])


class TestSplitChunks(unittest.TestCase):

    def test_read_delimited_chunks_short_lines(self):
        """Test lines shorter than chunksize, data longer than chunk_size."""
        chunk_size = 500

        # Make sure the test data fits the testcase:
        #
        # 1. The lines must be shorter than the chunk_size, so that all
        # chunks can be shorter than chunk_size
        self.assertTrue(max(map(len, csv_test_data.splitlines())) < chunk_size)
        # 2. The data must be longer than chunk_size so that chunking is
        # useful
        self.assertTrue(len(csv_test_data) > chunk_size)

        # The actual test
        chunked = list(read_delimited_chunks(io.BytesIO(csv_test_data),
                                             chunk_size))

        # Appending all chunks yields the original unchunked data
        self.assertEqual(csv_test_data, b"".join(chunked))

        # All chunks are shorter than chunk_size
        self.assertTrue(max(map(len, chunked)) <= chunk_size)

        # All chunks were split at line separators
        self.assertEqual(csv_test_data.splitlines(),
                         list(itertools.chain.from_iterable(
                             chunk.splitlines() for chunk in chunked)))

    def test_read_delimited_chunks_long_lines(self):
        """Test lines longer than chunksize, data longer than chunk_size."""
        chunk_size = 100

        # Make sure the test data fits the testcase:
        #
        # 1. At least one lines must be longer than the chunk_size, so
        # that at least one chunk has to be longer as well
        self.assertTrue(max(map(len, csv_test_data.splitlines())) > chunk_size)

        # The actual test
        chunked = list(read_delimited_chunks(io.BytesIO(csv_test_data),
                                             chunk_size))

        # Appending all chunks yields the original unchunked data
        self.assertEqual(csv_test_data, b"".join(chunked))

        # Chunks longer than chunk_size have newlines only at the end.
        long_chunks = list(filter(lambda chunk: len(chunk) > chunk_size,
                                  chunked))
        self.assertTrue(len(long_chunks) > 0)
        for chunk in long_chunks:
            if chunk.endswith(b"\n"):
                chunk = chunk[:-1]
            self.assertFalse(b"\n" in chunk)

    def test_read_delimited_chunks_empty_input(self):
        """Test empty input for read_delimited_chunks."""
        # splittign an empty file yields no chunks at all, similar to
        # how a string's readline method yields an empty list for an
        # empty string.
        self.assertEqual(list(read_delimited_chunks(io.BytesIO(b""),
                                                    1000)),
                         [])


class TestGenerateReports(unittest.TestCase):

    def test_generate_reports_no_chunking(self):
        """Test generate_reports with chunking disabled"""
        template = Report()
        template.add("feed.name", "test_generate_reports_no_chunking")
        [report] = list(generate_reports(template, io.BytesIO(csv_test_data),
                                         chunk_size=None,
                                         copy_header_line=False))
        self.assertEqual(report["feed.name"],
                         "test_generate_reports_no_chunking")
        self.assertEqual(base64.b64decode(report["raw"]), csv_test_data)


    def test_generate_reports_with_chunking_no_header(self):
        """Test generate_reports with chunking and not copying the header"""
        template = Report()
        template.add("feed.name", "test_generate_reports_with_chunking")

        chunk_size = 1000

        # This test only makes sense if the test data actually is longer
        # than the chunk size
        self.assertTrue(chunk_size < len(csv_test_data))

        decoded_chunks = []
        for report in generate_reports(template, io.BytesIO(csv_test_data),
                                       chunk_size=chunk_size,
                                       copy_header_line=False):
            self.assertEqual(report["feed.name"],
                             "test_generate_reports_with_chunking")
            decoded_chunks.append(base64.b64decode(report["raw"]))

        self.assertEqual(b"".join(decoded_chunks), csv_test_data)


    def test_generate_reports_with_chunking_and_copying_header(self):
        """Test generate_reports with chunking and copying the header"""
        chunk_size = 1000

        # This test only makes sense if the test data actually is longer
        # than the chunk size
        self.assertTrue(chunk_size < len(csv_test_data))

        template = Report()
        template.add("feed.name",
                     "test_generate_reports_with_chunking_and_header")
        observation_time = template["time.observation"]

        original_header = io.BytesIO(csv_test_data).readline()

        decoded_chunks = [original_header]
        for report in generate_reports(template, io.BytesIO(csv_test_data),
                                       chunk_size=chunk_size,
                                       copy_header_line=True):
            self.assertEqual(report["feed.name"],
                             "test_generate_reports_with_chunking_and_header")
            self.assertEqual(report["time.observation"], observation_time)
            report_data = io.BytesIO(base64.b64decode(report["raw"]))
            header = report_data.readline()
            chunk = report_data.read()

            self.assertEqual(original_header, header)
            decoded_chunks.append(chunk)

        self.assertEqual(b"".join(decoded_chunks), csv_test_data)


if __name__ == "__main__":
    unittest.main()
