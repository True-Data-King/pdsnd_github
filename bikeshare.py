import time
import pandas as pd


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month  - name of the month to filter by, or "all" to apply no month filter
        (str) day  - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city or washington). HINT: Use a while loop to handle invalid inputs
    while True:
        #Check if the input is valid before running the rest of the program
        city = input('Would you like to view data for chicago, new york city or washington?\n')
        if city.lower() in CITY_DATA:
            break
        else:
            print('\nYou haven\'t entered a valid city name')


    # get user input for month (all, january, february, march, april, may , june)
    month_list = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    month_prompt = 'What month would you like to view data for? (type in a choice from the list below)\n [all, january, february, march, april, may, june]\n'
   
    while True:
         #Check if the input is valid before running the rest of the program
        month = input(month_prompt)
        if month.lower() in month_list:
            break
        else:
            print('\nYou haven\'t entered a valid month')
    

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')
    day_prompt = 'What day would you like to view data for? (type in a choice from the list below)\n [all, Mon, Tue, Wed, Thu, Fri, Sat]\n'
   
    while True:
         #Check if the input is valid before running the rest of the program to ensure proper data collection
        day = input(day_prompt)
        if day.lower() in day_list:
            break
        else:
            print('\nYou haven\'t entered a valid day')
        
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #Load in the file based on the user input
    df = pd.read_csv(CITY_DATA[city])
    
    #Convert the start time columt to a datetime type before extracting the month, day and hour data into new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    #Filter the dataframe to contain only the data requested by the user
   
    if month != 'all':
        df = df[df['month'] == month.title()]
    
    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The month with the highest number of trips is ', df['month'].mode()[0])

    # display the most common day of week
    print('Of all the days in a week, people most commonly traveled on', df['day'].mode()[0])


    # display the most common start hour
    print('Of all the hours in a day, people most commonly traveled in hour', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is the ' + df['Start Station'].mode()[0] + ' station.')

    # display most commonly used end station
    print('The most commonly used end station is the ' + df['End Station'].mode()[0] + ' station.')
    
    # display most frequent combination of start station and end station trip
    #Group the dataframe by the start and end station columns, sort it in descending order and then print the values in the first index
    sorted_df_descending = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending = False)
    stations = sorted_df_descending.first_valid_index()
    print('\nTrips are most frequently taken between the ' + stations[0] + ' station and the ' +  stations[1] + ' station.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = str(df['Trip Duration'].sum())
    print('The total travel time is ' + total_travel_time + ' seconds.')

    # display mean travel time
    mean_travel_time = str(df['Trip Duration'].mean())
    print('The average travel time is ' + mean_travel_time + ' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df['User Type'].value_counts()
    print('Bike service users consist of ' + str(count_user_types[0]) + ' subscribers and ' + str(count_user_types[1]) + ' customers.')
    
    # Display counts of gender
    #The data for each city doesn't contain gender and birth year so we'll have to confirm if the columns exist before we try to count it
    if 'Gender' in df:
        count_gender_types = df['Gender'].value_counts()
        print('Bike service users consist of ' + str(count_gender_types[0]) + ' males and ' + str(count_gender_types[1]) + ' females.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        
        print('The earliest customer birth year is ' + str(earliest))
        print('The latest customer birth year is ' + str(latest))
        print('The most common customer birth year is ' + str(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        summary = input('Would you like to view a summary of the data? (Y/N)\n')
        if summary.lower() == 'y':
            print(df.head)
            print('-'*40)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
