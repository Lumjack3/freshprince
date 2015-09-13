import matplotlib.pyplot as plt
import collections
import scipy.stats as stats


x = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
c = collections.Counter(x)

print "Frequencies:"

count_sum = sum(c.values())
for k,v in c.iteritems():
	print str(k) + ": " + str(v) + " times"

plt.figure()
plt.hist(x, histtype='bar')
plt.savefig("histogram.png")

plt.figure()
plt.boxplot(x)
plt.savefig("boxplot.png")

plt.figure()
graph1 = stats.probplot(x, dist='norm', plot = plt)
plt.savefig("qq.png")
plt.show()
