import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import dateutil.parser
import csv
import sys

x = []
y = []

with open('output/nyt_ts.csv','r') as f:
  plots = csv.reader(f, delimiter=',')
  for row in plots:
    try:
      timestamp = row[4]
      state = row[5]
      if state == sys.argv[1]:
        dem_share = float(row[11])
        rep_share = float(row[10])
        y.append(dem_share / rep_share)
        x.append(dateutil.parser.parse(timestamp))
    except ZeroDivisionError:
      print('Either a header row or a divide-by-zero')


fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y)

# Format X-Axis
date_formatter = mdates.DateFormatter('%m-%d %HZ')
ax.xaxis.set_major_formatter(date_formatter)

plt.ylabel('D/R')
plt.ylim(0, 2)
plt.title(sys.argv[1])
plt.show()
