import csv
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
from matplotlib.ticker import StrMethodFormatter

#reading in the csv file 

with open("Data-Oscilloscope.csv") as csv_file: 

	csv_reader = csv.reader(csv_file, delimiter=",")
	time =[]
	voltage_raw = [] 

	for row in csv_reader:
		time.append(float(row[3]))
		voltage_raw.append(float(row[4]))
		print("voltage:", row[4])

#trimming the data 

trim_lower_index = 980
trim_upper_index = 1170

time_trim = time[trim_lower_index:trim_upper_index]
voltage_trim = voltage_raw[trim_lower_index:trim_upper_index]

#error bar arrays. These are the error bars for a select 10, evenly spaced points from the dataset

errorbar_x_vals = []
errorbar_y_vals = []
for i in range(0,2500,250): 
	errorbar_y_vals.append(voltage_raw[i])
	errorbar_x_vals.append(time[i])

#error on the data points 

yerr = np.std(voltage_raw)

#this function plots the data 

def baseGraph():
	plt.title("Voltage vs. Time")
	plt.xlabel("Time (s) ")
	plt.ylabel("Voltage (V) ")
	plt.plot(time, voltage_raw, '-r', time_trim,voltage_trim, '-b')
	plt.errorbar(errorbar_x_vals, errorbar_y_vals, yerr= yerr, markersize =4,linestyle = "None", fmt="-o", capsize=5, elinewidth=1, markeredgewidth=1)

#plotting the baseGraph(), without any changes to the axes as a subplot

plt.figure(1)
plt.subplot(211)
baseGraph()


# this plots the graph from the function, but adds changes to the axes labels and scales, plotting the graph with these changes 
#as a subplot

plt.subplot(212)
baseGraph()
plt.ylim([0, 0.15])
plt.yticks(np.arange(0, 0.16, 0.014))
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))

plt.xlim([0, 0.1])
plt.xticks(np.arange(0, 0.11, 0.01))
plt.tight_layout()
plt.show()

#fitting the gaussian function 

def gauss_function(x, a, x0, sigma):
	return a*np.exp(-(x-x0)**2/(2*sigma**2))


popt, pcov = curve_fit(gauss_function, time_trim, voltage_trim, p0=[1,.4,0.1])
perr = np.sqrt(np.diag(pcov))

#plot of the gaussian fit 

plt.figure(2)
plt.plot(time_trim, gauss_function(time_trim, *popt), label = "fit")
plt.plot(time_trim, voltage_trim, "-b")
plt.title("Gaussian Fit")
plt.xlabel("Time (s) ")
plt.ylabel("Voltage (V) ")
plt.show()

print(pcov)
print(perr)

#parsing pcov and perr

''' 
#1) PCOV is the parameter covariance of the POPT elements. The parameter covariance of the optimal values is used to determine the uncertainty 
and the correlation of two random parameters (in this case, the time and voltage). The PERR is the uncertainty 
calculated using the PCOV.
 
#2) The POPT are optimal values such that, when the differences between gauss_function(POPT) and the y values of the data points, 
 are squared and then added together, this sum is minimized.

#3) The second last line of code prints the correlation and covariance matrix representing the chosen parameters. The last line of code
prints the error estimated using the covariance matrix.'''



#trimming the data to the right most peak 

trim_lower_index = 2000
trim_upper_index = 2500

time_trim = time[trim_lower_index:trim_upper_index]
voltage_trim = voltage_raw[trim_lower_index:trim_upper_index]


#fitting the lorentz to the right most peak

#cleaning the data a little 

voltage_trim_lorentz=[]
min_trim_voltage = min(voltage_raw)

for index, value in enumerate(voltage_trim):
	voltage_trim_lorentz.append(value-min_trim_voltage)



#lorentz fit function

#x is just the x values, a is the amplitude, x0 is the central value, and f is the full width at half max

def lorentz(x,a,x0,f):
	return (0.5*a*f)/((x-x0)**2+(0.5*f)**2)

popt, pcov = curve_fit(lorentz, time_trim, voltage_trim_lorentz, p0=[0.0172, 0.0898, 0.005])
perr = np.sqrt(np.diag(pcov))

plt.figure(3)

plt.plot(time_trim, lorentz(time_trim, *popt), label = "fit")
plt.plot(time_trim, voltage_trim_lorentz, "-b")
plt.title("Lorentz fit")
plt.xlabel("Time (s) ")
plt.ylabel("Voltage (V) ")
plt.show()
