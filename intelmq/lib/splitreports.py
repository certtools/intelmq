# -*- coding: utf-8 -*-
"""
Support for splitting large raw reports into smaller ones.

The main intention of this module is to help work around limitations in
Redis which limits strings to 512MB. Collector bots can use the
functions in this module to split the incoming data into smaller pieces
which can be sent as separate reports.

Collectors usually don't really know anything about the data they
collect, so the data cannot be reliably split into pieces in all cases.
This module can be used for those cases, though, where users know that
the data is actually a line-based format and can easily be split into
pieces as newline characters. For this to work, some assumptions are
made:

 - The data can be split at any newline character

   This would not work, for e.g. a CSV based formats which allow
   newlines in values as long as they're within quotes.

 - The lines are much shorter than the maximum chunk size

   Obviously, if this condition does not hold, it may not be possible to
   split the data into small enough chunks at newline characters.

Other considerations:

 - To accommodate CSV formats, the code can optionally replicate the
   first line of the file at the start of all chunks.

 - The redis limit applies to the entire IntelMQ report, not just the
   raw data. The report has some meta data in addition to the raw data
   and the raw data is encoded as base64 in the report. The maximum
   chunk size must take this into account, but multiplying the actual
   limit by 3/4 and subtracting a generous amount for the meta data.
"""
from typing import BinaryIO, Generator, Optional, List

from intelmq.lib.message import Report


def split_chunks(chunk: bytes, chunk_size: int) -> List[bytes]:
    """Split a bytestring into chunk_size pieces at ASCII newlines characters.

    The return value is a list of bytestring objects. Appending all of
    them yields a bytestring equal to the input string. All items in the
    list except the last item end in newline. The items are shorter than
    chunk_size if possible, but may be longer if the input data has
    places where the distance between two neline characters is too long.

    Note in particular, that the last item may not end in a newline!

    Params:
        chunk: The string to be splitted
        chunk_size: maximum size of each chunk

    Returns:
        chunks: List of resulting chunks
    """
    chunks = []

    while len(chunk) > chunk_size:
        newline_pos = chunk.rfind(b"\n", 0, chunk_size)
        if newline_pos == -1:
            # no newline available to make chunk smaller than
            # chunk_size. Search forward to get a minimum chunk longer
            # than chunk_size
            newline_pos = chunk.find(b"\n", chunk_size)

        if newline_pos == -1:
            # no newline in chunk, so this is a leftover that may have
            # to be combined with the next data read.
            chunks.append(chunk)
            chunk = b""
        else:
            split_pos = newline_pos + 1
            chunks.append(chunk[:split_pos])
            chunk = chunk[split_pos:]
    if chunk:
        chunks.append(chunk)

    return chunks


def read_delimited_chunks(infile: BinaryIO, chunk_size: int) -> Generator[bytes, None, None]:
    """Yield the contents of infile in chunk_size pieces ending at newlines.
    The individual pieces, except for the last one, end in newlines and
    are smaller than chunk_size if possible.

    Params:
        infile: stream to read from
        chunk_size: maximum size of each chunk

    Yields:
        chunk: chunk with maximum size of chunk_size if possible
    """
    leftover = b""

    while True:
        new_chunk = infile.read(chunk_size)
        chunks = split_chunks(leftover + new_chunk, chunk_size)
        leftover = b""
        # the last item in chunks has to be combined with the next chunk
        # read from the file because it may not actually stop at a
        # newline and to avoid very small chunks.
        if chunks:
            leftover = chunks[-1]
            chunks = chunks[:-1]
        for chunk in chunks:
            yield chunk

        if not new_chunk:
            if leftover:
                yield leftover
            break


def generate_reports(report_template: Report, infile: BinaryIO, chunk_size: Optional[int],
                     copy_header_line: bool) -> Generator[Report, None, None]:
    """Generate reports from a template and input file, optionally split into chunks.

    If chunk_size is None, a single report is generated with the entire
    contents of infile as the raw data. Otherwise chunk_size should be
    an integer giving the maximum number of bytes in a chunk. The data
    read from infile is then split into chunks of this size at newline
    characters (see read_delimited_chunks). For each of the chunks, this
    function yields a copy of the report_template with that chunk as the
    value of the raw attribute.

    When splitting the data into chunks, if copy_header_line is true,
    the first line the file is read before chunking and then prepended
    to each of the chunks. This is particularly useful when splitting
    CSV files.

    The infile should be a file-like object. generate_reports uses only
    two methods, readline and read, with readline only called once and
    only if copy_header_line is true. Both methods should return bytes
    objects.

    Params:
        report_template: report used as template for all yielded copies
        infile: stream to read from
        chunk_size: maximum size of each chunk
        copy_header_line: copy the first line of the infile to each chunk

    Yields:
        report: a Report object holding the chunk in the raw field
    """
    if chunk_size is None:
        report = report_template.copy()
        data = infile.read()
        if data:
            report.add("raw", data, overwrite=True)
            yield report
    else:
        header = b""
        if copy_header_line:
            header = infile.readline()
        for chunk in read_delimited_chunks(infile, chunk_size):
            report = report_template.copy()
            report.add("raw", header + chunk, overwrite=True)
            yield report
