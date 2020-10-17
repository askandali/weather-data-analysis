# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 19:34:42 2019

@author: Angeliki Skandali
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


winter_months = ('DEC', 'JAN', 'FEB')
spring_months = ('MAR', 'APR', 'MAY')
summer_months = ('JOU', 'JUL', 'AUG')
fall_months = ('SEP', 'OCT', 'NOV')


# Function that checks if value is nan and then fill the value with cubic interpolation
# based on the 3 previous and 3 next  values
def cubic_interpolate(dataframe, colname):
    for i, value in dataframe[colname].items():
        if np.isnan(value):
            dataframe[colname][i] = dataframe[colname][(i - 3):(i + 4)].interpolate(method='cubic')[i]


# Function that checks the rain status of the year
def rain_status(sum_rain):
    if sum_rain < 400:
        print('Lack of rain')
    elif 400 <= sum_rain < 600:
        print('Satisfactory amount of rain')
    else:
        print('Excessive rainfall')


def main(with_plots):
    # read data and skip spaces
    data = pd.read_csv('data/weather_data.csv', skipinitialspace=True)
    # transform our data to a dataframe
    df = pd.DataFrame(data)

    # Fill NaN with DEC in Month column
    df['MONTH'].fillna('DEC', inplace=True)

    # filled nans of HIGH and LOW columns
    cubic_interpolate(df, 'HIGH')
    cubic_interpolate(df, 'LOW')

    print('> The median of average temperature is: ' + str(df['TEMP'].median()))
    print('> The std of average temperature is: ' + str(df['TEMP'].std()))

    # Find the counts of each direction
    df['DIR'].value_counts()
    direction = df['DIR'].value_counts().index
    counts = df['DIR'].value_counts().values

    # make a pie with the counts percentages of all the days of the year
    plt.title('Percentage of wind direction throughout the year')
    plt.pie(counts, labels=direction, shadow=False, autopct='%1.0f%%')
    plt.axis('equal')

    if with_plots:
        plt.savefig('plots/pie_wind_direction.png')
        plt.show()

    # Group by high Temp and max and get the time of the 4 highest temperatures
    highest_temps = df.groupby('HIGH').max()['TIME'].tail(4)
    print('> The 4 of the highest temperature are: ')
    print(highest_temps)

    print('> Most times the wind was: ' + str(df['DIR'].value_counts()[:1]))
    print('> Max wind speed caused: ' + str(df.groupby('WINDHIGH').max()['W_SPEED'].tail(1)))

    # Create a plot with average rain per month
    month_sum_df = df.groupby('MONTH').sum().reset_index()

    month_sum_df.plot(kind='bar', x='MONTH', y='RAIN', legend=None)
    plt.title('Average Rain per month')
    plt.tight_layout()

    if with_plots:
        plt.savefig('plots/avg_rain_monthly.png')
        plt.show()

    # Predict the temperature for 25 December of the next year

    # keep avg temperatures only from December
    y = df['TEMP'][df['MONTH'] == 'DEC']

    # december days from 1 to 31
    x = np.arange(1, len(y) + 0.1, 1)

    I = np.ones((len(x),))

    A = np.c_[x, I]

    np.linalg.lstsq(A, y, rcond=-1)

    # So for 25 december of the next year
    xp = 25
    yp = -0.18048387 * xp + 14.08129032
    print('> The avg temperature predicted is: ' + str(yp) + ' celcius')

    # Create plots for seasonal temperatures

    # Return temperatures based on season
    def season_temp(col, season):
        return df[col][df['MONTH'].apply(lambda x: x in season)].values

    fig, axs = plt.subplots(2, 2)

    axs[0, 0].plot(season_temp('HIGH', winter_months), 'r-', label='High')
    axs[0, 0].plot(season_temp('TEMP', winter_months), 'g-', label='Average')
    axs[0, 0].plot(season_temp('LOW', winter_months), 'b-', label='Low')
    axs[0, 0].set_title('Winter')

    axs[0, 1].plot(season_temp('HIGH', spring_months), 'r-', label='High')
    axs[0, 1].plot(season_temp('TEMP', spring_months), 'g-', label='Average')
    axs[0, 1].plot(season_temp('LOW', spring_months), 'b-', label='Low')
    axs[0, 1].legend(loc='upper left', bbox_to_anchor=(1, 0.5))
    axs[0, 1].set_title('Spring')

    axs[1, 0].plot(season_temp('HIGH', summer_months), 'r-',
                   season_temp('TEMP', summer_months), 'g-',
                   season_temp('LOW', summer_months), 'b-')
    axs[1, 0].set_title('Summer')

    axs[1, 1].plot(season_temp('HIGH', fall_months), 'r-',
                   season_temp('TEMP', fall_months), 'g-',
                   season_temp('LOW', fall_months), 'b-')
    axs[1, 1].set_title('Fall')

    for ax in axs.flat:
        ax.set(xlabel='Days', ylabel='Temperatures')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()

    plt.suptitle('Seasonal Temperatures')
    if with_plots:
        fig.savefig('plots/temp_per_season.png', bbox_inches='tight')
        plt.show()

    # Get rain status
    print('> Rain status: ')
    rain_status(df['RAIN'].sum())


if __name__ == '__main__':
    # set with_plots=True to see the generated plots
    main(with_plots=True)
