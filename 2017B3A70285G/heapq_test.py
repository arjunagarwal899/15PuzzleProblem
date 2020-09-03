from heapq import *

## See the following link:
##              https://docs.python.org/3/library/heapq.html

h = []

heappush(h,[13,'Bhutan'])
heappush(h,[25,'Nepal'])
heappush(h,[11,'Sri Lanka'])
heappush(h,[22,'Maldives'])
heappush(h,[5,'South Korea'])
heappush(h,[30,'New Zealand'])
heappush(h,[8,'Kenya'])

print(heappop(h))
print(heappop(h))
print(heappop(h))
print(heappop(h))
print(heappop(h))
print(heappop(h))
print(heappop(h))
