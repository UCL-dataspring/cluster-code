# An example analysis, for determining average pages per book

from bluclobber.archive import Archive
from bluclobber.sparkrods import get_streams

import yaml

streams = get_streams(downsample = 4096)
issues = streams.map(Archive)
books = issues.flatMap(lambda x: list(x))
word_counts = books.map(lambda x: len(list(x.words())))

result = [books.count(), word_counts.reduce(lambda x,y: x+y)]

with open('result.yml','w') as result_file:
    result_file.write(yaml.safe_dump(result))
