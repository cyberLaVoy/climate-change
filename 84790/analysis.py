import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import math
import datetime

def fetchData(fileName):
    return pd.read_csv(fileName)

def getAverageMaxTemp(dataFrame):
    stations = dataFrame.STATION.unique()
    averageMaxTemp = 0 
    stationCount = 0
    for i in range(len(stations)):
        stationMaxAvg = dataFrame[dataFrame.STATION == stations[i]].TMAX.mean()
        if not math.isnan(stationMaxAvg):
            averageMaxTemp += stationMaxAvg
            stationCount += 1
    return averageMaxTemp/stationCount

def plotRegressionLine(X, Y, color):
    slope, intercept, rvalue, pvalue, stderr = stats.linregress(X, Y)
    plt.plot(X, [slope*x+intercept for x in X], color=color, linestyle="dashed")

def displayAveragePrecipitationPeryear(dataFrame):
    dataFrame.DATE = pd.to_datetime(dataFrame.DATE)
    stations = dataFrame.STATION.unique()
    year = dataFrame.DATE.min().year
    years = []
    precAvgs = []
    skewedYears = [1918, 1919, 1920, 1921] # data apears to be skewed these years (instrument malfunction?)
    for _ in range(dataFrame.DATE.max().year-dataFrame.DATE.min().year):
        if year in skewedYears: # skip any skewed years
            year += 1
            continue
        totalYearPrecAvg = 0
        stationRecordedCount = 0
        for i in range(len(stations)):
            subset = dataFrame[ (dataFrame.STATION == stations[i]) & (dataFrame.DATE >= pd.Timestamp(year, 1, 1)) & (dataFrame.DATE < pd.Timestamp(year+1, 1, 1)) ]
            yearPrecAvg = subset.PRCP.mean()
            if not math.isnan(yearPrecAvg):
                totalYearPrecAvg += yearPrecAvg
                stationRecordedCount += 1
        years.append(year)
        precAvgs.append(totalYearPrecAvg/stationRecordedCount)
        year += 1
    plt.plot(years, precAvgs, color="blue", label="Overall Avg")
    plotRegressionLine(years, precAvgs, "blue")
    plt.title("Yearly Precipitation Averages for 84770 from " + str(dataFrame.DATE.min().year) + '-' + str(dataFrame.DATE.max().year-1))
    plt.legend()
    plt.grid()
    plt.show()

 
def displayAverageTempsPerYear(dataFrame):
    dataFrame.DATE = pd.to_datetime(dataFrame.DATE)
    stations = dataFrame.STATION.unique()
    year = dataFrame.DATE.min().year
    years = []
    tempMaxAvgs = []
    tempMinAvgs = []
    for _ in range(dataFrame.DATE.max().year-dataFrame.DATE.min().year):
        totalYearMaxAvg = 0
        totalYearMinAvg = 0
        stationRecordedCount = 0
        for i in range(len(stations)):
            subset = dataFrame[ (dataFrame.STATION == stations[i]) & (dataFrame.DATE >= pd.Timestamp(year, 1, 1)) & (dataFrame.DATE < pd.Timestamp(year+1, 1, 1)) ]
            yearMaxAvg = subset.TMAX.mean()
            yearMinAvg = subset.TMIN.mean()
            if not math.isnan(yearMaxAvg) and not math.isnan(yearMinAvg):
                totalYearMaxAvg += yearMaxAvg
                totalYearMinAvg += yearMinAvg
                stationRecordedCount += 1
        years.append(year)
        tempMaxAvgs.append(totalYearMaxAvg/stationRecordedCount)
        tempMinAvgs.append(totalYearMinAvg/stationRecordedCount)
        year += 1
    overallAvgTemps = [sum(x)/2 for x in zip(tempMaxAvgs, tempMinAvgs)]
    plt.plot(years, tempMaxAvgs, color="red", label="Max Avg")
    plotRegressionLine(years, tempMaxAvgs, "red")
    plt.plot(years, tempMinAvgs, color="blue", label="Min Avg")
    plotRegressionLine(years, tempMinAvgs, "blue")
    plt.plot(years, overallAvgTemps, color="orange", label="Overall Avg")
    plotRegressionLine(years, overallAvgTemps, "orange")
    plt.title("Yearly Temperature Averages for 84770 from " + str(dataFrame.DATE.min().year) + '-' + str(dataFrame.DATE.max().year-1))
    plt.legend()
    plt.grid()
    plt.show()

def main():
    dataFrame = fetchData("1767926.csv")
    #displayAveragePrecipitationPeryear(dataFrame)
    displayAverageTempsPerYear(dataFrame)

if __name__ == "__main__":
    main()